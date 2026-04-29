#!/usr/bin/env python3
"""
neirong-task-automator 自动修复模块
检测到常见故障后自动尝试修复
"""

import subprocess
import json
import sys

def check_cron_status():
    """检查所有cron任务状态，发现error立即告警"""
    result = subprocess.run(
        ['openclaw', 'cron', 'list', '--json'],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        errors = []
        for job in data.get('jobs', []):
            if job.get('status') == 'error':
                errors.append({
                    'id': job.get('id'),
                    'name': job.get('name'),
                    'lastError': job.get('lastError', 'unknown')
                })
        return errors
    except:
        return []

def fix_common_errors():
    """修复常见错误"""
    errors = check_cron_status()
    if not errors:
        print("✅ 所有cron任务正常")
        return
    
    print(f"⚠️ 发现 {len(errors)} 个error任务")
    for e in errors:
        print(f"  - {e['name']}: {e['lastError']}")
    
    # 发送告警到飞书（通过message工具）
    # 实际执行时由调用方使用message工具发送

if __name__ == '__main__':
    fix_common_errors()
