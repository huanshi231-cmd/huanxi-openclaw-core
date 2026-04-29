#!/usr/bin/env python3
"""
基金数据获取模板（基于东财 API）
来源：鳌拜教程 · 2026-04-20

使用方式：
    from fund_api_template import get_estimate, get_history, calc_week_pnl

API 限制：
    - 每只基金间隔 ≥0.5s（建议值，0.25s 为边界值）
    - 东财 API 随时可能变更，需预留容错
"""

import urllib.request
import urllib.error
import json
import ssl
import time
from datetime import datetime

# ============ SSL 上下文（东财 API 需要）===========
def _make_ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# ============ 获取实时估算净值 ============
def get_estimate(code: str) -> dict | None:
    """
    返回：{ code, name, dwjz, gsz, gszzl, gztime } 或 None
    """
    url = f"https://fundgz.1234567.com.cn/js/{code}.js?rt={int(time.time()*1000)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10, context=_make_ssl_ctx()) as resp:
            text = resp.read().decode("utf-8")
        # 格式: jsonpgz({...})
        json_str = text.replace("jsonpgz(", "").rstrip(")")
        data = json.loads(json_str)
        return {
            "code": data.get("fundcode"),
            "name": data.get("name"),
            "dwjz": float(data["dwjz"]),
            "gsz": float(data["gsz"]),
            "gszzl": float(data["gszzl"]),  # 估算涨跌幅 %
            "gztime": data.get("gztime"),
        }
    except Exception as e:
        print(f"[WARN] get_estimate {code} failed: {e}")
        return None

# ============ 获取历史净值 ============
def get_history(code: str, days: int = 7) -> list | None:
    """
    返回：[{ DWJZ, FSRQ, ... }, ...] 或 None
    """
    url = f"https://api.fund.eastmoney.com/f10/lsjz?fundCode={code}&pageIndex=1&pageSize={days}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "https://fund.eastmoney.com/",
        })
        with urllib.request.urlopen(req, timeout=10, context=_make_ssl_ctx()) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("Data", {}).get("LSJZList", [])
    except Exception as e:
        print(f"[WARN] get_history {code} failed: {e}")
        return None

# ============ 计算周期涨跌幅 ============
def calc_pnl(history: list, days: int = 7) -> float | None:
    """
    基于历史净值计算涨跌幅 %
    """
    if not history or len(history) < days:
        return None
    try:
        latest = float(history[0]["DWJZ"])
        old = float(history[days - 1]["DWJZ"])
        return round((latest / old - 1) * 100, 3)
    except Exception:
        return None

# ============ 批量获取（带间隔） ============
def fetch_all(fund_list: list, interval: float = 0.5) -> dict:
    """
    fund_list: [("名称", "代码", 金额, "类型"), ...]
    interval: 每只基金间隔秒数（建议 ≥0.5）
    返回: { code: { estimate, history, week_pnl, amount, type }, ... }
    """
    results = {}
    for name, code, amount, ftype in fund_list:
        est = get_estimate(code)
        time.sleep(interval)  # 留余量，不压边界
        hist = get_history(code)
        pnl = calc_pnl(hist) if hist else None
        results[code] = {
            "name": name,
            "amount": amount,
            "type": ftype,
            "estimate": est,
            "history": hist,
            "week_pnl": pnl,
        }
    return results

if __name__ == "__main__":
    # 快速测试
    test_code = "159770"
    est = get_estimate(test_code)
    print(f"实时: {est}")
    hist = get_history(test_code)
    print(f"历史({len(hist) if hist else 0}条): {hist[:2] if hist else None}")
