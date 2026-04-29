# 基金监控脚本库

## 文件说明
| 文件 | 用途 |
|------|------|
| `fund_api_template.py` | 核心 API 模板（可直接 import） |
| `README.md` | 本文件 |

## 快速使用
```python
from fund_api_template import get_estimate, get_history, calc_pnl, fetch_all

# 单只基金测试
est = get_estimate("159770")
hist = get_history("159770", days=7)
week_pnl = calc_pnl(hist)

# 批量获取
funds = [
    ("汇添富机器人", "159770", 42927, "ETF"),
    ("富国资源精选", "022167", 33500, "混合"),
]
data = fetch_all(funds)
```

## 数据源
- 实时：`fundgz.1234567.com.cn`（无需登录）
- 历史：`api.fund.eastmoney.com`（需 SSL 绕过）

## 安全提示
- `CERT_NONE` 仅限内网/可控环境使用
- 东财 API 可能随时变更，需预留监控

## 来源
鳌拜 · 基金监控系统教程 · 2026-04-20
