#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送公众号草稿前：把「假汉字」还原成真 UTF-8。

常见病因：
- 模型把 JSON 里的 \\uXXXX 当成正文，反斜杠丢失 → 大写显示成 U53CC，小写则连成 u8bbau9a6c（如「论马」）
- 正文里混有 U+53CC、裸 U53CC（连续多个）

用法：
  python3 sanitize_wechat_html.py <输入.html> <输出.html>
  python3 sanitize_wechat_html.py <输入.html>   # 覆盖写回输入文件
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def _decode_u4(m: re.Match[str]) -> str:
    return chr(int(m.group(1), 16))


def _decode_u8(m: re.Match[str]) -> str:
    return chr(int(m.group(1), 16))


def _is_cjk_or_ext(cp: int) -> bool:
    if 0x4E00 <= cp <= 0x9FFF:
        return True
    if 0x3400 <= cp <= 0x4DBF:
        return True
    if 0x20000 <= cp <= 0x2A6DF:
        return True
    if 0x3000 <= cp <= 0x303F:  # CJK 标点
        return True
    if 0xFF00 <= cp <= 0xFFEF:  # 全角
        return True
    return False


def _decode_lower_u4_cjk(m: re.Match[str]) -> str:
    """反斜杠丢失后的 u8bba（小写 u），仅替换为常见中日韩码位，避免误伤英文。"""
    cp = int(m.group(1), 16)
    if _is_cjk_or_ext(cp):
        return chr(cp)
    return m.group(0)


def sanitize_text(s: str) -> str:
    if not s:
        return s

    # 标准 JSON 风格 \uXXXX \UXXXXXXXX
    s = re.sub(r"\\u([0-9a-fA-F]{4})", _decode_u4, s)
    s = re.sub(r"\\U([0-9a-fA-F]{8})", _decode_u8, s)

    # U+53CC
    s = re.sub(r"U\+([0-9a-fA-F]{4,6})\b", _decode_u4, s)

    # 裸 U53CC（4 位十六进制，前后不是十六进制字母数字，避免误伤极少见英文）
    for _ in range(20):  # 多轮：连续 U53CCU5B50…
        ns = re.sub(
            r"(?<![0-9A-Fa-f])U([0-9a-fA-F]{4})(?![0-9A-Fa-f])",
            _decode_u4,
            s,
        )
        if ns == s:
            break
        s = ns

    # 裸 u8bbau9a6c（小写 u + 4 位 hex，\\u 丢反斜杠后极常见，如「论马」）
    for _ in range(40):
        ns = re.sub(
            r"(?<![0-9A-Fa-f\\])u([0-9a-fA-F]{4})(?![0-9a-fA-F])",
            _decode_lower_u4_cjk,
            s,
        )
        if ns == s:
            break
        s = ns

    return s


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else inp

    raw = inp.read_text(encoding="utf-8")
    cleaned = sanitize_text(raw)
    out.write_text(cleaned, encoding="utf-8")
    print(f"OK: {inp} -> {out} ({len(cleaned)} chars)", file=sys.stderr)


if __name__ == "__main__":
    main()
