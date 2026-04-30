# 全局知识库索引

> 所有分身共用，自动维护

## 目录结构

```
knowledge/
├── raw/           # 原始素材（各分身分类）
│   ├── system/     # 系统 SOP / 规范文档
│   ├── neirong/    # 内容创作素材
│   ├── linggangshenghuo/  # 灵感生活
│   └── liaoyuyewu/ # 疗愈业务
├── compiled/       # LLM 编译后的结构化 wiki
└── health_check/   # 健康检查记录
```

## 健康检查

- 频率：每周日 23:30 自动执行
- 内容：检测矛盾、过时、补充缺失、更新索引

## 最近更新

| 日期 | 分身 | 内容 |
|------|------|------|
| 2026-04-05 | system | 初始化全局知识库：raw目录结构、SOP_QA_ARCHIVE、每周健康检查cron | 待首次检查 |
