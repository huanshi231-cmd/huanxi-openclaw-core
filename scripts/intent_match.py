#!/usr/bin/env python3
"""Intent matching script - matches user message against SKILL_DISPATCH triggers."""
import sys
import re
import os

DISPATCH = '/Users/huanxi/.openclaw/workspace-system/SKILL_DISPATCH.md'

def main():
    if len(sys.argv) < 2:
        print("INTENT: none")
        return
    
    user_msg = sys.argv[1]
    lower = user_msg.lower()
    
    triggers = [
        (re.compile(r'(值不值得做|点子|brainstorm|产品规划|需求分析|帮我理清|这个想法|新功能|产品想法)'), 'office-hours'),
        (re.compile(r'(规划|今天做什么|今日计划|今日安排|日程|时间块|to do)'), 'plan-my-day'),
        (re.compile(r'(每日复盘|今天总结|今日复盘|工作复盘|晚间复盘)'), 'daily-review-ritual'),
        (re.compile(r'(自我检查|自己哪里不对|自查|自我审视)'), 'self-review'),
        (re.compile(r'(发布前检查|质量验收|qa|测试|质量巡检)'), 'qa-patrol'),
        (re.compile(r'(配图|排版|视觉|用什么图|设计建议)'), 'graphic-design'),
        (re.compile(r'(朗读|读出来|read aloud|读这篇)'), 'x-article-reader'),
        (re.compile(r'(搜索|全网搜索|综合搜索|帮我查)'), 'multi-search-engine'),
        (re.compile(r'(通知.*分身|@内容|@系统|派给.*执行|转给|分发给)'), 'feishu-multi-agent-messaging'),
        (re.compile(r'(反复失败|卡住了|想放弃|摆烂|没进展)'), 'pua-skill'),
        (re.compile(r'(创建.*技能|新建 skill|写个技能|author.*skill)'), 'skill-creator'),
        (re.compile(r'(找.*技能|有没有.*技能|什么技能能|install.*skill)'), 'find-skill'),
        (re.compile(r'(知识库.*健康|矛盾|过时|sop.*检查)'), 'SOP_LLM_COMPILE'),
        (re.compile(r'(生成.*总结|工作总结|日报)'), 'daily-summary'),
    ]
    
    for pattern, skill in triggers:
        if pattern.search(lower):
            print(f"INTENT: {skill}")
            return
    
    print("INTENT: none")

if __name__ == "__main__":
    main()
