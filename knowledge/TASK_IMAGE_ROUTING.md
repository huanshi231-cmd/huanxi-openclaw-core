# 图片路由稳定性问题 - 待系统分身排查

## 问题描述
`agents.defaults.imageModel` 配置的 fallback 链不稳定，有时能看图，有时不能。

## 已确认的情况
1. 当前配置：
   - primary: `volcano/ep-20260329111539-b7w2r`
   - fallbacks: [豆包, Gemini, MiniMax]
2. 显式指定 `doubao/doubao-1.5-vision-pro-32k-250115` 可以正常看图
3. 但依赖自动 fallback 时，有时成功有时失败

## 需要排查的问题
1. gateway 重启后 imageModel 配置是否稳定生效？
2. image 工具调用时是否真的使用了 `agents.defaults.imageModel` 配置，还是用了对话模型？
3. 为什么 fallback 链不可靠——是配置问题还是调用逻辑问题？

## 要求
1. 排查根因
2. 给出修复方案
3. 修复后验证稳定性
4. 回传给主控和施欢

## 参考
- SOP_IMAGE_READ.md 已在三个分身同步
- 临时方案：每次显式指定豆包模型，不依赖自动路由
