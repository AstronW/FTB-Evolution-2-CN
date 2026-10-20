---
navigation:
  parent: lua-api/index.md
  title: HandleList
  icon: minecraft:red_bundle
categories:
  - api_types
description: a fan-out list of cards or variables returned by getAll
---

# <a name="HandleList" /> <a name="handlelist" /> HandleList

`HandleList<T>`是卡片或变量的列表, **将写入方法广播
给每个成员**. 可通过
[`network:getAll(type)`](network.md#getAll)或
[`Channel:getAll(type)`](network.md#channel-getall).

对列表调用写入方法, 会按顺序将相同方法与参数
用于各个成员. 列表不提供读取方法, 因为
返回值正是读取的目的, 若对N个成员调用后悄悄丢弃
返回值, 很容易出错. 如需逐项读取, 请调用`:list()`
再遍历.

<LuaCode>
```lua
-- 一次启用全部红色频道活塞.
network:channel("red"):getAll("redstone"):set(true)
-- 用一行代码给全部侦测卡注册相同的onChange处理器.
network:getAll("observer"):onChange(function(block, state)
    if block == "nodeworks:celestine_cluster" then
        -- ...
    end
end)
```
</LuaCode>

## <a name="which-methods-broadcast" /> 哪些方法会广播调用

仅广播 **写入方法** , 即调用方不依赖返回值的方法.
刻意不提供`:powered()`, `:count()`, `:get()`等读取方法,
以及`:block()`, 避免N个成员的返回值被静默丢弃.
如需逐项读取, 调用`:list()`, 再分别检查
各个成员.

各类型自己的页面, 如[RedstoneCard](card-handle.md#redstone-card),
[VariableHandle](variable-handle.md), 是区分该类型
哪些方法属于读取或写入的依据.

## <a name="list" /> list

逐项操作的出口. 返回底层数组, 可遍历各成员,
读取单独的值, 或执行不适合广播的
逐成员逻辑.

<LuaCode>
```lua
local pistons = network:channel("red"):getAll("redstone")
for _, p in pistons:list() do
    if p:powered() then
        print(p.name, "is currently powered")
    end
end
```
</LuaCode>

## <a name="count" /> count

返回列表成员数量. 比`#list:list()`开销小, 因为不需要
创建数组.

<LuaCode>
```lua
local watchers = network:getAll("observer")
print(watchers:count(), "observer cards on the network")
```
</LuaCode>

## <a name="face" /> face

返回新的HandleList, 将其中卡片成员的访问面
覆盖为`name`. 原列表不变, 仅
返回副本受影响. 非[CardHandle](card-handle.md)成员, 如变量,
破坏器和放置器, 原样保留, 这些句柄类型忽略侧面设置.

将列表传入预设时也会保留此覆盖设置,
如[Importer](importer.md)/[Stocker](stocker.md), 因而一个通配表达式
就能读写全部匹配卡片的非默认侧面.

<LuaCode>
```lua
-- 从所有io_*卡片的底面抽取熔炉产物, 送入输出箱
importer:from(network:cards("io_*"):face("bottom")):to("output"):start()
```
</LuaCode>

形式与[`CardHandle:face`](card-handle.md#face)相同, 但同时应用于
整个列表.
