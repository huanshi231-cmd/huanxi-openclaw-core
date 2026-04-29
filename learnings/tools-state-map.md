# 工具状态地图

> 盘点时间：2026-04-22

---

## 已验证可用 ✅

| 工具 | 状态 | 验证情况 |
|------|------|---------|
| 公众号草稿箱 | ✅ 可用 | wechat-draft skill 已验证 |
| PPT生成 | ✅ 可用 | ppt-generator 刚测试通过 |
| 灵感记录 | ✅ 可用 | linggangshenghuo inspiration_skill |

---

## 理论可用，需实测 ⚠️

| 工具 | 状态 | 说明 |
|------|------|------|
| TTS语音生成 | ⚠️ 需测 | lh-edge-tts skill 存在，edge-tts是成熟库 |
| 小红书发布 | ⚠️ 需测 | xiaohongshu-all-in-one skill 存在（macOS验证过） |
| 剪映自动化 | ⚠️ 需测 | jianying-editor skill 存在，文档完整 |

---

## 技能包已就位，待整条链路打通 🔧

| 工具 | Skill文件 | 说明 |
|------|----------|------|
| 文案创作 | neirong/ppt-strategist | 刚建好 |
| 图片设计 | shejiguan/design_skill.md | 描述存在，实际工具需确认 |
| 视频剪辑 | neirong/jianying | 文档完整 |
| 新媒体运营 | xinmeiyunying | 小红书skill存在 |

---

## 当前最大卡点

**jianying + tts 都没有实测验证**

- jianying skill 文档很完整，但不知道实际能不能跑
- tts 理论可用，但没测过效果

---

## 建议解锁顺序

1. **tts**（10分钟测完）→ 配音问题解决
2. **公众号**（已通）→ 立即可用
3. **小红书发布**（1小时测完）→ 立即可用
4. **jianying**（最复杂）→ 放最后
5. **PPT**（已通）→ 沙龙随时用

---

## 待测试清单

- [ ] edge-tts 是否能生成可用音频
- [ ] xiaohongshu-all-in-one 实际发布是否正常
- [ ] jianying-editor 剪映自动化能否跑通
- [ ] 设计skill实际调用的是哪个图片生成工具

