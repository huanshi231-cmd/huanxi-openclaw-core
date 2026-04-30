#!/usr/bin/env python3
"""
执行力+记忆力计分追踪器
自动记录每日扣分情况，分析趋势
"""
import json, os, datetime
from pathlib import Path

SCORE_FILE = Path("~/.openclaw/workspace/skills/self-improving/score_log.json").expanduser()
SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)

def load():
    if SCORE_FILE.exists():
        with open(SCORE_FILE) as f:
            return json.load(f)
    return {"execution": {"total":0, "docked":0, "last_dock":None, "last_dock_reason":None},
            "memory": {"total":0, "missed":0, "last_miss":None, "last_miss_reason":None},
            "daily_log": {}}

def save(data):
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def dock(type_, reason=""):
    d = load()
    today = datetime.date.today().isoformat()
    if today not in d["daily_log"]:
        d["daily_log"][today] = {"execution_docked":0, "memory_missed":0}
    d[type_]["total"] += 1
    if type_ == "execution":
        d[type_]["docked"] += 1
        d[type_]["last_dock"] = today
        d[type_]["last_dock_reason"] = reason
        d["daily_log"][today]["execution_docked"] += 1
    else:
        d[type_]["missed"] += 1
        d[type_]["last_miss"] = today
        d[type_]["last_miss_reason"] = reason
        d["daily_log"][today]["memory_missed"] += 1
    save(d)
    score = d[type_]
    pct = round((score["total"] - score.get("docked",0) - score.get("missed",0)) / max(score["total"],1) * 100)
    print(f"⏳ {type_} score: {pct}/100 (total actions: {score['total']}, docked: {score.get('docked',0)+score.get('missed',0)})")

def show():
    d = load()
    print("=== 执行力+记忆力计分 ===")
    print(f"执行力: {round((d['execution']['total']-d['execution']['docked'])/max(d['execution']['total'],1)*100)}/100 (总动作:{d['execution']['total']} 被扣:{d['execution']['docked']})")
    print(f"记忆力: {round((d['memory']['total']-d['memory']['missed'])/max(d['memory']['total'],1)*100)}/100 (总动作:{d['memory']['total']} 失误:{d['memory']['missed']})")
    print("最近7天:")
    today = datetime.date.today()
    for i in range(7):
        day = (today - datetime.timedelta(days=i)).isoformat()
        if day in d["daily_log"]:
            log = d["daily_log"][day]
            print(f"  {day}: 执行力扣{log['execution_docked']}次 记忆力失误{log['memory_missed']}次")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        show()
    elif sys.argv[1] == "dock" and len(sys.argv) >= 3:
        dock(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    elif sys.argv[1] == "show":
        show()
