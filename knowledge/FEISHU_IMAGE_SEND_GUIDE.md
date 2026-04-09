# 飞书直接发图片 — 永久解决方案（2026-04-07 已验证）

## 问题历史
飞书发图片一直失败，报 `LocalMediaAccessError: Local media path is not under an allowed directory`
施欢反复强调：必须直接把图片插在飞书里，不能发链接。

## 根本原因
飞书发送本地图片有安全限制，必须配置 `mediaLocalRoots` 允许读取的目录。

## 解决方案（已永久配置）

### 配置文件位置
`~/.openclaw/openclaw.json` → `channels.feishu.accounts.neirong.mediaLocalRoots`

### 已添加的允许目录
```json
"mediaLocalRoots": [
  "/Users/huanxi/.openclaw/workspace-neirong/images/",
  "/Users/huanxi/.openclaw/workspace-neirong/",
  "/tmp/"
]
```

### 发图片标准流程
1. **生图** → 豆包 API 生成，保存到 `/tmp/原图.jpg`
2. **压缩** → 用 PIL 压缩到 800x800，约 45KB
3. **复制到工作空间** → `~/.openclaw/workspace-neirong/images/输出.jpg`
4. **发送** → `message action=send` + `filePath=工作空间/images/输出.jpg`

### Python 压缩代码
```python
from PIL import Image
img = Image.open('/tmp/原图.jpg')
img = img.resize((800, 800), Image.Resampling.LANCZOS)
img.save('/Users/huanxi/.openclaw/workspace-neirong/images/输出.jpg', quality=85)
```

### message 工具调用
```
message action=send channel=feishu accountId=neirong filePath=/Users/huanxi/.openclaw/workspace-neirong/images/xxx.jpg
```

## 绝对禁止
- ❌ 不要发桌面路径（Desktop 不在允许目录中）
- ❌ 不要发链接代替图片
- ❌ 不要跳过压缩步骤（原图太大）
- ❌ 不要静默失败（必须确认图片发送成功）

## 验证记录
- 2026-04-07 20:50 配置完成并重启网关
- 2026-04-07 21:50 施欢确认："我可以看见了"

---
*此文件永久保留，每次生图发飞书时必须遵守此流程*
*修改配置后必须执行 `openclaw gateway restart`*

---

## 完整交付链条（2026-04-07 确立）

### 施欢要求的交付标准流程

当施欢说"做图"、"生成图片"、"给我看图"时：

**Step 1：生成图片**
- 用豆包/火山引擎 API 生成

**Step 2：保存到正确位置**
- 先保存到 `/tmp/`
- PIL 压缩到 800x800，约 45KB
- 复制到 `~/.openclaw/workspace-neirong/images/`

**Step 3：飞书对话直接显示**
- 用 `message action=send channel=feishu accountId=neirong filePath=工作空间路径`
- **必须直接发图片，不发链接**
- 施欢在飞书对话里直接看到图片

**Step 4：飞书云文档归档**
- 创建/更新飞书文档
- 把图片上传到文档里
- 确保文档链接可以正常打开

### 禁止事项
- ❌ 不发链接代替图片
- ❌ 不让施欢去桌面找
- ❌ 不跳过压缩
- ❌ 不发失败后不告知

### 验证
- 2026-04-07 22:28 施欢确认："在那个飞书云文档打开，我也可以看，是一样的逻辑路径"
