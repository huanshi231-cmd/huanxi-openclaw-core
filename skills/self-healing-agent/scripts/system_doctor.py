#!/usr/bin/env python3
"""系统诊断器 - 一键生成健康报告"""
import os, json, subprocess
from datetime import datetime

LEARNINGS = os.path.expanduser("~/.openclaw/workspace-main/.learnings/")
COOLDOWN = os.path.expanduser("~/.openclaw/workspace-main/skills/self-healing-agent/scripts/cron_cooldown_manager.py")
JOBS = os.path.expanduser("~/.openclaw/cron/jobs.json")

def get_cooldown_jobs():
    r = subprocess.run(['python3', COOLDOWN, 'list'], capture_output=True, text=True)
    return r.stdout

def get_recent_errors():
    """从learnings找最近的相关错误"""
    keywords = ['timeout', 'error', 'fail', 'crash']
    results = []
    for kw in keywords:
        r = subprocess.run(['python3', 
            os.path.expanduser("~/.openclaw/workspace-main/skills/self-healing-agent/scripts/learnings_search.py"), 
            kw], capture_output=True, text=True, timeout=5)
        if '未找到' not in r.stdout and r.stdout.strip():
            results.append((kw, r.stdout))
    return results

def get_cron_status():
    """获取cron任务状态"""
    try:
        with open(JOBS) as f:
            data = json.load(f)
        jobs = data.get('jobs', [])
        total = len(jobs)
        error_jobs = [j for j in jobs if j.get('state', {}).get('lastStatus') == 'error']
        ok_jobs = [j for j in jobs if j.get('state', {}).get('lastStatus') == 'ok']
        return total, len(error_jobs), len(ok_jobs), error_jobs
    except:
        return 0, 0, 0, []

def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total, err_count, ok_count, err_jobs = get_cron_status()
    cooldown = get_cooldown_jobs()
    
    print("=" * 50)
    print(f"🏥 系统诊断报告 | {ts}")
    print("=" * 50)
    
    print(f"\n📊 Cron任务状态")
    print(f"  总任务: {total} | ✅正常: {ok_count} | ❌异常: {err_count}")
    
    if err_jobs:
        print(f"\n⚠️ 异常任务:")
        for j in err_jobs[:5]:
            name = j.get('name', 'unnamed')
            err = j.get('state', {}).get('lastError', 'unknown')
            consecutive = j.get('state', {}).get('consecutiveErrors', 0)
            print(f"  - {name}")
            print(f"    错误: {err[:60]}")
            print(f"    连续失败: {consecutive}次")
    
    print(f"\n⏳ 冷却状态:")
    if '没有任务在冷却中' in cooldown:
        print("  ✅ 所有任务正常，无冷却")
    else:
        for line in cooldown.strip().split('\n')[1:]:
            if line.strip():
                print(f"  {line}")
    
    recent = get_recent_errors()
    if recent:
        print(f"\n📜 相关历史经验:")
        for kw, content in recent[:3]:
            lines = [l for l in content.strip().split('\n') if l.strip()]
            print(f"  [{kw}] 找到 {len(lines)//4} 条记录")
    
    print("\n" + "=" * 50)
    
    # 给出建议
    if err_count > 0:
        print("💡 建议: 运行 `python3 cron_cooldown_manager.py auto-check` 检查是否需要冷却")
    else:
        print("✅ 系统状态正常")
    
    print()

if __name__ == "__main__":
    main()
