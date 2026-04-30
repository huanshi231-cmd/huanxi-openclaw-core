# SOP_IMAGE_WORKFLOW.md - 图片生成与归档流程

## 铁律：免费图库优先

**顺序：Pexels免费图 → AI生图兜底**

1. 先从 Pexels 搜免费图片，下载保存
2. 搜不到合适的，再用 AI 生成
3. 不浪费付费 API 额度

Pexels 下载方式：
```bash
curl -s -L "https://images.pexels.com/photos/照片ID/pexels-photo-照片ID.jpeg?auto=compress&cs=tinysrgb&w=1080&h=1920&dpr=1" -o /tmp/slide_xx.jpg
```

## 完整流程

### 第1步：配图选择
- 先搜 Pexels 免费图
- 搜不到再 AI 生成
- 保存到本地：/Users/huanxi/.openclaw/workspace/images/

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
- 生成后直接贴图片到对话框
- 不写文档记录就结束
- 不告诉用户本地路径
- 优先使用付费AI生图
