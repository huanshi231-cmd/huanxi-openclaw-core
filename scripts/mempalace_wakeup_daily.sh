#!/bin/bash
echo "MemPalace Wake-up 更新 — $(date)"

# neirong palace路径修复
mkdir -p ~/.openclaw/workspace-neirong/.mempalace
mkdir -p ~/.openclaw/workspace-linggangshenghuo/.mempalace
mkdir -p ~/.openclaw/workspace-liaoyuyewu/.mempalace

# 全局记忆库（system）
OUT_SYSTEM=~/.openclaw/workspace-system/memory/mempalace_wakeup.md
echo "# MemPalace Wake-up — $(date '+%Y-%m-%d %H:%M')" > $OUT_SYSTEM
mempalace wake-up >> $OUT_SYSTEM 2>/dev/null
echo "  system: $(wc -l < $OUT_SYSTEM) lines"

# neirong私有记忆库
OUT_NEIRONG=~/.openclaw/workspace-neirong/memory/mempalace_wakeup.md
echo "# MemPalace Wake-up — $(date '+%Y-%m-%d %H:%M')" > $OUT_NEIRONG
mempalace --palace ~/.openclaw/workspace-neirong/.mempalace wake-up >> $OUT_NEIRONG 2>/dev/null
echo "  neirong: $(wc -l < $OUT_NEIRONG) lines"

# linggang私有记忆库
OUT_LINGGANG=~/.openclaw/workspace-linggangshenghuo/memory/mempalace_wakeup.md
echo "# MemPalace Wake-up — $(date '+%Y-%m-%d %H:%M')" > $OUT_LINGGANG
mempalace --palace ~/.openclaw/workspace-linggangshenghuo/.mempalace wake-up >> $OUT_LINGGANG 2>/dev/null
echo "  linggang: $(wc -l < $OUT_LINGGANG) lines"

# liaoyuyewu私有记忆库
OUT_LIAO=~/.openclaw/workspace-liaoyuyewu/memory/mempalace_wakeup.md
echo "# MemPalace Wake-up — $(date '+%Y-%m-%d %H:%M')" > $OUT_LIAO
mempalace --palace ~/.openclaw/workspace-liaoyuyewu/.mempalace wake-up >> $OUT_LIAO 2>/dev/null
echo "  liaoyuyewu: $(wc -l < $OUT_LIAO) lines"

echo "✅ 完成"
