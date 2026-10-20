---
navigation:
  parent: lua-api/index.md
  title: Scheduler
  icon: minecraft:repeater
categories:
  - api_builtin
description: tick/second/delay callbacks
---

# <a name="Scheduler" /> <a name="scheduler" /> Scheduler

`scheduler`模块注册周期或延迟回调, 在
服务器游戏刻中运行, 频率20 TPS. 每次注册都返回任务ID, 可传给
`:cancel`停止任务.

> **提示:** 建议开启["自动运行"](../items-blocks/scripting_terminal.md#autorun), 对应设备为<ItemLink id="terminal" />; 希望持续运行[`scheduler:tick`](scheduler.md#tick)或[`scheduler:second`](scheduler.md#second)时尤其适用.

![](../assets/images/autorun.png)

## <a name="tick" /> tick

每个服务器游戏刻运行一次指定回调.

<LuaCode>
```lua
scheduler:tick(function()
  -- 每秒运行20次
end)
```
</LuaCode>

## <a name="second" /> second

每秒, 即20游戏刻, 运行一次指定回调.

<LuaCode>
```lua
scheduler:second(function()
  -- 每秒运行一次
end)
```
</LuaCode>

## <a name="delay" /> delay

将回调延迟指定数量的游戏刻后执行.

<LuaCode>
```lua
scheduler:delay(20, function()
  -- 经过一秒后运行
end)
```
</LuaCode>

## <a name="cancel" /> cancel

按任务ID停止任务. 对已取消或已到期ID调用也安全.

<LuaCode>
```lua
local task = scheduler:tick(function()
  print("hello")
end)
-- 一秒后取消scheduler:tick任务
scheduler:delay(20, function()
  scheduler:cancel(task)
end)
-- "hello" (x20)
```
</LuaCode>
