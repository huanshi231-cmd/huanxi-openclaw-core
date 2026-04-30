# SOP_PUBLIC_ACCOUNT_PUSH.md - 微信公众号推送流程

## 前提条件
1. IP白名单已配置（当前IP：112.43.8.28）
2. 微信公众号 AppID：wx5d5a624cfde49bd3
3. 微信公众号 AppSecret：已配置

## 完整流程

### 第1步：获取Access Token
接口：https://api.weixin.qq.com/cgi-bin/token

### 第2步：上传封面图（必须）
接口：https://api.weixin.qq.com/cgi-bin/material/add_material
需要 thumb_media_id，草稿不能为空

### 第3步：构建HTML内容
使用清新春天风格排版：
- 背景色：#FFF5F0, #E8F5E9, #F3E5F5（浅粉浅绿浅紫）
- 文字色：#4A4A4A（深灰）
- 居中排版

### 第4步：推送草稿
接口：https://api.weixin.qq.com/cgi-bin/draft/add

### 第5步：同步更新飞书文档
- 文章标题、链接
- 推送时间
- 状态

## 禁止行为
- 不写进MEMORY.md当草稿
- 不告知用户去后台操作

## 当前状态
- 推送功能：✅ 正常
- IP白名单：112.43.8.28（如被拒需更新）
- 草稿标题规则：64字节以内
