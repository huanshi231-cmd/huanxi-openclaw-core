# SOP_PUBLIC_ACCOUNT_PUSH.md - 微信公众号推送流程

## 配图原则（铁律）

**免费图库优先 → 付费AI生图兜底**

1. 先从 Pexels 搜免费图片：`https://images.pexels.com/photos/xxx`
2. 搜不到合适素材，再用 AI 生成
3. 不浪费付费 API 额度做能免费找到的图片

## 完整流程

### 第1步：配图选择
- 先搜 Pexels 免费图
- 搜不到再 AI 生成
- 保存到本地：/Users/huanxi/.openclaw/workspace/images/

### 第2步：获取Access Token
接口：https://api.weixin.qq.com/cgi-bin/token

### 第3步：上传封面图（必须）
接口：https://api.weixin.qq.com/cgi-bin/material/add_material
需要 thumb_media_id，草稿不能为空

### 第4步：构建HTML内容
使用清新春天风格排版：
- 背景色：#FFF5F0, #E8F5E9, #F3E5F5（浅粉浅绿浅紫）
- 文字色：#4A4A4A（深灰）
- 居中排版

### 第5步：推送草稿
接口：https://api.weixin.qq.com/cgi-bin/draft/add

### 第6步：同步更新飞书文档
- 文章标题、链接
- 推送时间
- 状态

## 禁止行为
- 不写进MEMORY.md当草稿
- 不告知用户去后台操作
- 不优先使用付费AI生图

## 当前状态
- 推送功能：✅ 正常
- IP白名单：112.43.8.28（如被拒需更新）
- 草稿标题规则：64字节以内
