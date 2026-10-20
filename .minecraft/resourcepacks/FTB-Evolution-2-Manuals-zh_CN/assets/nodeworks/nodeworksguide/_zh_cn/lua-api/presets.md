---
navigation:
  parent: lua-api/index.md
  title: 预设
  icon: terminal
categories:
  - api_builtin
description: declarative builders (importer, stocker) for common item movement and stocking patterns
---

# <a name="Presets" /> <a name="presets" /> 预设

预设是声明式构建器, 用于最常见的两种脚本模式:
**把物品从A移到B** 和 **维持目标库存** . 每个
预设由一串方法调用组成, 从左到右如同一句话,
最后调用`:start()`启动.

预设建立在现有脚本API之上, 仍然是Lua, 使用
相同卡片与过滤器, 脚本停止时也会
一起清理. 区别在于一行预设可替代约15行
自行维护状态的调度循环.

<LuaCode>
```lua
-- 每秒将刷石箱中的圆石移入网络存储.
importer:from("mobFarm"):filter("$item:cobblestone"):to(network):start()
-- 在发射器中维持64支箭, 不足时自动合成.
stocker:ensure("minecraft:arrow"):to("dispenser"):keep(64):start()
```
</LuaCode>

## <a name="current-presets" /> 当前预设

* [Importer](importer.md)将物品从一个或多个来源移至一个或多个
  目标. 默认依次填充, 填满一个目标再处理下一个.
  调用`:roundrobin()`则在目标间轮询.
* [Stocker](stocker.md)通过从存储拉取, 合成或两者结合, 将目标库存维持在`:keep(n)`
  指定水平. 达到目标后不会反向抽取
  多余物品.

## <a name="source-and-target-references" /> 来源与目标引用

预设中凡接受来源或目标的位置, 均支持三种形式:

1. **字符串** 卡片别名: `"bufferChest"`.
2. 由`network:get(...)`取得的 **CardHandle** .
3. 全局对象 **`network`** 本身, 表示"整个网络存储池".

<LuaCode>
```lua
-- 三种形式都有效, 也可混用.
importer:from("farm", network:get("secondary"), network)
  :to("output")
  :start()
```
</LuaCode>

每当网络拓扑变化, 都会重新按名称解析卡片, 因此
卡片拆除后以相同名称放回, 无需重启预设
也能继续工作. 缺失卡片会静默跳过, 直至其重新出现.

## <a name="shared-methods" /> 共用方法

所有`ImporterBuilder`和`StockerBuilder`都支持相同的生命周期
与控制方法.

### <a name="every" /> every

<LuaCode>
```lua
ImporterBuilder:every(ticks: number): ImporterBuilder
StockerBuilder:every(ticks: number): StockerBuilder
```
</LuaCode>

设置预设重新检查的间隔. 默认为20游戏刻, 即每秒一次.
运行中更改间隔, 会取消当前调度任务并按新间隔
重新注册, 因此`imp:every(5)`立即生效.

### <a name="start-/-stop-/-isrunning" /> <a name="start-stop-isrunning" /> start / stop / isRunning

<LuaCode>
```lua
ImporterBuilder:start()
ImporterBuilder:stop()
ImporterBuilder:isRunning(): boolean
```
</LuaCode>

`:start()`验证调用链并开始定时运行. 构建器已在运行时
不会重复启动, 因此可安全地反复调用. `:stop()`停止定时运行,
但保留全部配置, 之后调用`:start()`会恢复同一调用链,
包括轮询游标的位置.

<LuaCode>
```lua
local imp = importer:from("src"):to("dst")
scheduler:second(function()
  if someCondition() and not imp:isRunning() then
    imp:start()
  elseif imp:isRunning() and not someCondition() then
    imp:stop()
  end
end)
```
</LuaCode>

## <a name="cleanup-on-script-stop" /> 脚本停止时的清理

脚本终端停止时, 无论手动停止还是网络断开,
该次脚本运行中注册的所有预设都会自动停止.
已创建却从未`:start()`的悬空构建器也会被清理.
再次启动脚本会从头重建所有预设, 因此可以自由
修改调用链, 无需担心遗留任务.
