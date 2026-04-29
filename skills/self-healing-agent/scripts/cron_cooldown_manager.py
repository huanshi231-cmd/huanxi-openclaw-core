#!/usr/bin/env python3
"""
Cron任务冷却管理器
功能：当job连续失败>=2次时，自动进入6小时冷却

使用方式：
  python3 cron_cooldown_manager.py check <job_id>    # 检查是否在冷却中
  python3 cron_cooldown_manager.py set <job_id>      # 为job设置冷却
  python3 cron_cooldown_manager.py list              # 列出所有冷却中的job
  python3 cron_cooldown_manager.py clear <job_id>    # 清除冷却
"""

import json
import os
import sys
from datetime import datetime

JOBS_FILE = os.path.expanduser("~/.openclaw/cron/jobs.json")
COOLDOWN_HOURS = 6

def load_jobs():
    with open(JOBS_FILE, 'r') as f:
        return json.load(f)

def save_jobs(data):
    with open(JOBS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def now_ms():
    return int(datetime.now().timestamp() * 1000)

def check_cooldown(job_state):
    """检查是否在冷却中"""
    cooldown_until = job_state.get('cooldownUntilMs', 0)
    if cooldown_until == 0:
        return False, 0
    current = now_ms()
    if current < cooldown_until:
        remaining_sec = (cooldown_until - current) // 1000
        return True, remaining_sec
    return False, 0

def set_cooldown(state):
    """为job设置6小时冷却"""
    current = now_ms()
    cooldown_until = current + (COOLDOWN_HOURS * 60 * 60 * 1000)
    state['cooldownUntilMs'] = cooldown_until
    state['cooldownSetAt'] = current
    state['cooldownHours'] = COOLDOWN_HOURS
    return state

def clear_cooldown(state):
    """清除冷却"""
    state.pop('cooldownUntilMs', None)
    state.pop('cooldownSetAt', None)
    state.pop('cooldownHours', None)
    return state

def cmd_check(job_id):
    """检查单个job的冷却状态"""
    data = load_jobs()
    for job in data.get('jobs', []):
        if job.get('id') == job_id:
            state = job.get('state', {})
            in_cooldown, remaining = check_cooldown(state)
            if in_cooldown:
                hrs = remaining // 3600
                mins = (remaining % 3600) // 60
                print(f"⏳ 在冷却中 | 剩余: {hrs}小时{mins}分钟")
                return
            else:
                consecutive = state.get('consecutiveErrors', 0)
                print(f"✅ 无冷却 | 连续失败: {consecutive}")
                return
    print(f"❌ 未找到job: {job_id}")

def cmd_set(job_id):
    """为job设置冷却"""
    data = load_jobs()
    for job in data.get('jobs', []):
        if job.get('id') == job_id:
            state = job.get('state', {})
            set_cooldown(state)
            job['state'] = state
            save_jobs(data)
            print(f"✅ 已设置{COOLDOWN_HOURS}小时冷却 | job: {job.get('name', job_id)}")
            return
    print(f"❓ 未找到job: {job_id}")

def cmd_list():
    """列出所有在冷却中的job"""
    data = load_jobs()
    in_cooldown = []
    for job in data.get('jobs', []):
        state = job.get('state', {})
        is_in, remaining = check_cooldown(state)
        if is_in:
            hrs = remaining // 3600
            mins = (remaining % 3600) // 60
            in_cooldown.append(f"  ⏳ {job.get('name','unnamed')} | 剩余{hrs}h{mins}m | 连续失败{state.get('consecutiveErrors',0)}次")
    
    if in_cooldown:
        print(f"当前 {len(in_cooldown)} 个任务在冷却中：")
        for item in in_cooldown:
            print(item)
    else:
        print("✅ 目前没有任务在冷却中")

def cmd_clear(job_id):
    """清除job的冷却"""
    data = load_jobs()
    for job in data.get('jobs', []):
        if job.get('id') == job_id:
            state = job.get('state', {})
            clear_cooldown(state)
            job['state'] = state
            save_jobs(data)
            print(f"✅ 已清除冷却 | job: {job.get('name', job_id)}")
            return
    print(f"❓ 未找到job: {job_id}")

def cmd_auto_check():
    """自动检查所有job，对连续失败>=2的自动设置冷却"""
    data = load_jobs()
    updated = 0
    for job in data.get('jobs', []):
        state = job.get('state', {})
        consecutive = state.get('consecutiveErrors', 0)
        in_cooldown, _ = check_cooldown(state)
        
        if consecutive >= 2 and not in_cooldown:
            set_cooldown(state)
            job['state'] = state
            updated += 1
            print(f"⚠️ 自动进入冷却: {job.get('name','unnamed')} | 连续失败{consecutive}次")
    
    if updated > 0:
        save_jobs(data)
        print(f"\n✅ 已为{updated}个任务设置冷却")
    else:
        print("✅ 所有任务正常，无需设置冷却")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check" and len(sys.argv) >= 3:
        cmd_check(sys.argv[2])
    elif cmd == "set" and len(sys.argv) >= 3:
        cmd_set(sys.argv[2])
    elif cmd == "list":
        cmd_list()
    elif cmd == "clear" and len(sys.argv) >= 3:
        cmd_clear(sys.argv[2])
    elif cmd == "auto-check":
        cmd_auto_check()
    else:
        print(__doc__)
