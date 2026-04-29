# TEAM_OPENIDS.md · 分身飞书 open_id 映射表

> 用于系统协作群 @mention，格式：<at user_id="open_id">名称</at>
> 群ID：oc_6c409c73f6d1bc540d0e54d472ea6bf2

## 分身 open_id 列表

| 分身 | agentId | 飞书 open_id |
|------|---------|-------------|
| 太阳（COO/自己） | main | ou_26ef2adfee37cf61503ee6b6cdc2b581 |
| 系统官 | system | ou_1724f0025d51c97fb7fde880ebbb6ae5 |
| 内容官 | neirong | ou_13de9a82ab69491c4de1a3db0cd1c7d5 |
| 新媒体运营官 | xinmeiyunying | ou_1c9b3d78a919c2d8e6248aed8483c5ae |
| 设计官 | shejiguansheji | ou_72c126be119e94177c40730ef4316278 |
| 疗愈业务官 | liaoyuyewu | ou_6be411e6ee853b75368c0ec9c3f8d920 |
| 课程策划官 | kechengcehua | ou_c979ab5116b603e283faed7d9eeb87f3 |
| 培训官 | peixun | ou_e8eadd401949415fad1c1a29b3d3e12a |
| 赋能官 | funeng | ou_a06804f5275d07b32c7ca1fbde64ef96 |
| 服务官 | fuwu | ou_76901ef6b7880a05981cb1a8d31d648d |
| 灵感官 | linggangshenghuo | ou_fbed00a36686879ac6f83cb5622cf7e0 |
| 记忆官 | memory | ou_44b845b99943a85b7ee327597b397ce4 |

## @mention 使用示例

```
<at user_id="ou_a06804f5275d07b32c7ca1fbde64ef96">赋能官</at> 请你整理本周培训材料
```

## 发消息到协作群的完整格式

```
message action=send channel=feishu accountId="main" target="oc_6c409c73f6d1bc540d0e54d472ea6bf2" message="<at user_id=\"ou_xxx\">分身名</at> 任务内容"
```
