# SOP_IMAGE_WORKFLOW.md - 图片生成与归档流程

## 完整流程

### 第1步：生成图片
- 按用户需求生成图片
- 保存到本地路径：/Users/huanxi/.openclaw/workspace/images/

### 第2步：上传到飞书云文档（配图库）
- 用 feishu_doc action=upload_image 把图片插入到对应的配图库文档
- 图片自动存到飞书云盘，可下载

### 第3步：更新配图库文档
在配图库文档里写清楚：
- 文件名
- 图片描述
- 本地存储路径
- 用途
- 状态（待裁剪/已完成等）

### 第4步：返回结果给用户
- 只返回：配图库文档链接 + 一句说明
- 不直接贴图片到对话框

## 当前配图库文档

| 主题 | 文档链接 |
|------|----------|
| 父母和解祈祷文 | https://feishu.cn/docx/VloHdrg21oO5SJxSIxDcATmhnib |
| 星座运势配图 | https://feishu.cn/docx/FARid2jLpoIDgQx66Vvc1r3unpc |

## 禁止行为

-  生成后直接贴图片到对话框
-  不写文档记录就结束
-  不告诉用户本地路径
