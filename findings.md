# findings.md

## 2026-04-27 仓库盘点
- workspace-main 此前不是 Git 仓库，已完成首次初始化。
- 已提交核心团队文件：AGENTS/SOUL/IDENTITY/USER/TOOLS/MEMORY/HEARTBEAT/TEAM_ROLES/.gitignore。
- 当前根目录存在大量未跟踪文件，包含：
  - 业务文档、制度文档
  - 图片/JPG/ZIP/PDF/PPTX
  - 转录输出（json/srt/tsv/txt/vtt）
  - 若干目录：docs、skills、reports、outputs、daily_summary 等
- 当前最合理策略不是一次性全部纳管，而是：
  1. 先保留核心治理文件为主干
  2. 增加 README 说明仓库用途与边界
  3. 扩展 .gitignore 忽略明显缓存/产物/临时文件
  4. 未来再按主题分批纳管业务资产
