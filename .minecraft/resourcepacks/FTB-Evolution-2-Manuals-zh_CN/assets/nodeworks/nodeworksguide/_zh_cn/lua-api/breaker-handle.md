---
navigation:
  parent: lua-api/index.md
  title: BreakerHandle
  icon: breaker
categories:
  - api_types
description: a device used to break blocks in front of it
---

# <a name="BreakerHandle" /> <a name="breakerhandle" /> BreakerHandle

`BreakerHandle`引用网络上的一个<ItemLink id="breaker" />,
由[`network:get(name)`](network.md#get)返回. 它会开始一个跨游戏刻的破坏
操作, 破坏正前方方块, 将掉落物送回网络
或交给自定义处理器.

<BlockImage scale="6" id="breaker" />

破坏器的开采等级相当于钻石镐, 耗时使用木镐
公式, 因此较硬方块的破坏时间明显更长.
每台破坏器同时只能执行一次破坏, 运行中再次调用`:mine()`
不会产生作用.

## <a name="Properties" /> <a name="properties" /> 属性

- **`.name`**
  - 破坏器别名, 与终端侧栏显示的名称相同

## <a name="mine" /> mine

开始破坏正前方的方块, 过程跨越多个游戏刻.
返回[BreakBuilder](./breaker-handle.md#breakbuilder), 脚本可
链式调用`:connect(fn)`重定向掉落物. 不继续链式调用时, 掉落物
会进入[网络存储](../nodeworks-mechanics/network-storage.md), 使用
标准[存储卡](../items-blocks/storage_card.md)优先级规则.

<LuaCode>
```lua
local breaker = network:get("quarry_1")
breaker:mine() -- 掉落物进入网络存储
```
</LuaCode>

目标为空气, 无法破坏或超过开采等级时, `:mine()`
返回空操作构建器, 以免后续链式调用崩溃.

## <a name="cancel" /> cancel

中止正在进行的破坏操作. 空闲时调用也安全, 方块不会
被破坏, 也不产生掉落物.

<LuaCode>
```lua
local breaker = network:get("breaker_1")
breaker:mine()
if dangerous() then
  breaker:cancel() -- 在完成前停止
end
```
</LuaCode>

## <a name="block" /> block

返回破坏器正前方方块的ID, 形式与
[`ObserverCard:block`](./card-handle.md#observer-card)相同, 适合根据
方块种类决定是否破坏.

<LuaCode>
```lua
local breaker = network:get("breaker_1")
if breaker:block() == "minecraft:stone" then
  breaker:mine()
end
```
</LuaCode>

## <a name="state" /> state

返回破坏器正前方方块的属性表, 形式与
[`ObserverCard:state`](./card-handle.md#observer-card)相同. 方块的每个
`BlockState`属性, 如生长`age`, `facing`, `lit`,
`waterlogged`等, 都会成为一个字段.

<LuaCode>
```lua
local breaker = network:get("crop_breaker")
local state = breaker:state()
if state.age == 7 then
  breaker:mine() -- 仅破坏完全成熟的作物
end
```
</LuaCode>

## <a name="isMining" /> <a name="ismining" /> isMining

正在破坏时返回`true`, 空闲时返回`false`. 可用来
避免破坏过程中再次调用`:mine()`; 虽然再次调用本就无效,
但`:isMining()`可使脚本分支更加清楚.

<LuaCode>
```lua
local breaker = network:get("breaker_1")
if not breaker:isMining() then
  breaker:mine()
end
```
</LuaCode>

## <a name="progress" /> progress

返回`0`至`1`之间的比例, 表示当前破坏操作的
完成进度. 空闲时为`0`, 适合驱动进度显示或安排
后续操作.

<LuaCode>
```lua
local breaker = network:get("breaker_1")
print(string.format("%.0f%%", breaker:progress() * 100))
```
</LuaCode>

---

## <a name="BreakBuilder" /> <a name="breakbuilder" /> BreakBuilder

由[`Breaker:mine()`](./breaker-handle.md#mine)返回, 配置破坏完成后的
掉落物去向. 没有链式调用时, 掉落物会自动进入网络
存储; 链式调用`:connect(fn)`则会将其转交给脚本
处理器.

### <a name="connect" /> connect

将本次破坏的掉落物重定向至回调. 每组掉落物都会向处理器传入一个
[ItemsHandle](./items-handle.md)形式的值, 因此一个
多掉落方块(如受时运影响的矿石)被破坏时, 可能
多次调用处理器.

处理器可读取掉落物的`.id`, `.name`, `.count`和`.kind`
以决定如何处理. 处理器未取走的物品会按默认路由
回到网络存储.

<LuaCode>
```lua
local breaker = network:get("breaker_1")
local chest = network:get("ore_chest")
breaker:mine():connect(function(item: ItemsHandle)
  if item.id == "minecraft:diamond" then
    chest:insert(item) -- 将钻石送入专用箱子
  end
  -- 其余物品按默认路径进入网络存储
end)
```
</LuaCode>

> **注意:** 破坏器的`:connect`处理器在破坏完成时运行, 不会
> 每刻运行. 处理器内的错误会被捕获, 因此异常回调不会
> 卡住破坏器.
