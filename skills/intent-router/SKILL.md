---
name: intent-router
description: >
  Intent routing skill that matches user messages against trigger keywords
  and routes to the appropriate skill. Fires on every user message via
  UserPromptSubmit hook. Auto-loaded by all agents.
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: |
            python3 -c "
import sys, re, os

USER_MSG = sys.argv[1] if len(sys.argv) > 1 else ''
DISPATCH = '/Users/huanxi/.openclaw/workspace-system/SKILL_DISPATCH.md'

if not USER_MSG or not os.path.exists(DISPATCH):
    print('INTENT: none'); sys.exit(0)

LOWER = USER_MSG.lower()

# Trigger → Skill mapping (checked in priority order)
triggers = [
    (re.compile(r'(值不值得做|点子|brainstorm|产品规划|需求分析|帮我理清|这个想法|新功能|产品想法)'), 'office-hours'),
    (re.compile(r'(规划今天|今日计划|今天做什么|日程|时间块|to do)'), 'plan-my-day'),
    (re.compile(r'(每日复盘|今天总结|今日复盘|工作复盘|晚间复盘)'), 'daily-review-ritual'),
    (re.compile(r'(自我检查|自己哪里不对|自查|自我审视)'), 'self-review'),
    (re.compile(r'(发布前检查|质量验收|qa|测试|冒烟测试)'), 'qa-patrol'),
    (re.compile(r'(配图|排版|视觉|用什么图|设计建议)'), 'graphic-design'),
    (re.compile(r'(朗读|读出来|read aloud|读这篇)'), 'x-article-reader'),
    (re.compile(r'(搜索|全网搜索|综合搜索|帮我查)'), 'multi-search-engine'),
    (re.compile(r'(通知.*分身|@内容|@系统|派给.*执行|转给)'), 'feishu-multi-agent-messaging'),
    (re.compile(r'(反复失败|卡住了|想放弃|摆烂)'), 'pua-skill'),
    (re.compile(r'(创建.*技能|新建 skill|写个技能)'), 'skill-creator'),
    (re.compile(r'(找.*技能|有没有.*技能|什么技能能)'), 'find-skill'),
]

for pattern, skill in triggers:
    if pattern.search(LOWER):
        print(f'INTENT: {skill}')
        sys.exit(0)

print('INTENT: none')
" "$1"
