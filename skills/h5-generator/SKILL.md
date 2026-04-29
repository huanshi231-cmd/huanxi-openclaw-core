# H5Generator · H5页面生成与GitHub部署技能

> 创建时间：2026-04-13
> 来源：从system分身记忆提取

---

## 技能描述

将H5页面生成为静态HTML，部署到GitHub Pages，并通过微信域名申诉实现微信内直接访问。

---

## 触发关键词

- "生成H5"
- "做个H5页面"
- "H5网页"
- "部署到GitHub"
- "微信里打不开"

---

## 前置要求

- [ ] GitHub账号已配置（huanshi231-cmd）
- [ ] gh CLI已登录（`gh auth status`）
- [ ] 目标仓库已存在（liaoyu-h5）
- [ ] 桌面有H5设计稿或内容需求

---

## 执行流程

### 第一步：生成H5页面

**工具**：Claude Code

**命令**：
```bash
cd ~/Desktop && claude-code --print --permission-mode bypassPermissions
```

**提示词模板**：
```
帮我生成一个H5课程咨询页面。

要求：
1. 移动端适配（375px宽度基准）
2. 简洁大气的设计风格
3. 包含：课程介绍、联系方式、预约按钮
4. 保存为：~/Desktop/h5-课程咨询_v最新.html

设计稿/需求：[粘贴施欢给的内容]
```

**输出位置**：`~/Desktop/h5-课程咨询_v最新.html`

---

### 第二步：GitHub备份

**仓库信息**：
| 项目 | 内容 |
|------|------|
| GitHub账号 | huanshi231-cmd |
| 仓库名 | liaoyu-h5 |
| 仓库地址 | github.com/huanshi231-cmd/liaoyu-h5 |
| Pages链接 | https://huanshi231-cmd.github.io/liaoyu-h5/ |

**操作步骤**：

```bash
# 1. 克隆仓库（如没有本地副本）
cd ~/Desktop
git clone https://github.com/huanshi231-cmd/liaoyu-h5.git

# 2. 进入仓库目录
cd ~/Desktop/liaoyu-h5

# 3. 复制新H5文件覆盖
cp ~/Desktop/h5-课程咨询_v最新.html index.html

# 4. 提交并推送
git add .
git commit -m "更新H5页面 - $(date '+%Y-%m-%d %H:%M')"
git push origin main

# 5. 确认推送成功
gh run list
```

**验证**：访问 https://huanshi231-cmd.github.io/liaoyu-h5/

---

### 第三步：微信域名申诉（如需要）

**问题**：GitHub Pages域名被微信屏蔽，微信内打开显示"网页停止访问"

**申诉地址**：urlsec.qq.com/complain.html

**申诉步骤**：

1. 打开 urlsec.qq.com/complain.html
2. 填入域名：`huanshi231-cmd.github.io`
3. 选择场景：**微信**
4. 提交备案/资质证明（如有）
5. 等待1-3天

**验证文件要求**：
- 文件名：`github-hosted-page-verification.html`（具体名称看申诉页面提示）
- 放置位置：**仓库根目录**（不是子目录）
- 格式：通常是空文件或包含特定字符串

**验证通过后**：微信内可直接打开GitHub Pages链接

---

## 经验教训（来自system分身）

### 教训
1. **H5改版前先确认需求再动手** — 不要边改边确认
2. **操作前先问清楚"改哪里+改成什么样"** — 不明确就不动
3. **每次commit前截图确认效果** — 不要连续多次commit改同一个东西
4. **遇到问题先确认是不是"原版就这样"再改回去**

### GitHub认证问题排查
```bash
# 检查是否已登录
gh auth status

# 认证失败时排查
security find-internet-password -s github.com -w

# 重新登录
gh auth login
```

### 微信申诉注意事项
- 验证文件必须放**根目录**，不是子目录
- 申诉通过后域名有效期需关注
- 如被永久封禁，考虑使用国内Gitee Pages作为替代

---

## 文件位置参考

| 文件 | 路径 |
|------|------|
| 最新H5 | ~/Desktop/h5-课程咨询_v最新.html |
| GitHub本地副本 | ~/Desktop/liaoyu-h5/index.html |
| GitHub仓库 | github.com/huanshi231-cmd/liaoyu-h5 |

---

## 常见问题

**Q：微信里打不开但浏览器可以？**
A：域名被微信拦截，执行第三步申诉流程

**Q：GitHub推送失败？**
A：检查gh auth status，确认已登录

**Q：H5在微信里显示异常？**
A：检查是否使用了微信不支持的CSS属性（如flexbox某些写法）

---

*技能创建：2026-04-13*
*基于system分身2026-04-11的实战经验*
