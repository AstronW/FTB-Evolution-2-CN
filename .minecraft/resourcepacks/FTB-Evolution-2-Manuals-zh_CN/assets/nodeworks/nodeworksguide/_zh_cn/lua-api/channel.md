---
navigation:
  parent: lua-api/index.md
  title: Channel
  icon: io_card
categories:
  - api_types
description: a dye-color-scoped view of the network
---

# <a name="Channel" /> <a name="channel" /> Channel

`Channel`是按染料颜色限定范围的网络视图, 通过
[`network:channel(color)`](network.md#channel)取得. 通过频道查询时, 只能
看到频道颜色匹配的卡片, 变量和设备. 频道
在每张卡片或设备自身界面中设置, 因此多个子系统可以共享
同一网络, 不会因卡片别名相同而互相干扰.

<LuaCode>
```lua
local red = network:channel("red")
local blue = network:channel("blue")
red:getAll("redstone"):set(true)   -- 仅红色频道的活塞动作
blue:getAll("redstone"):set(true)  -- 仅蓝色频道的活塞动作
```
</LuaCode>

颜色名必须是16种原版染料颜色之一, 如`white`, `red`,
`blue`, `light_blue`, `light_gray`等. 未知颜色会报错.

## <a name="choosing-a-channel" /> 选择频道

所有[卡片](../nodeworks-mechanics/cards.md)和[设备](../nodeworks-mechanics/devices.md)都有选择频道的方式. 默认所有
设备与卡片均使用`white`. 点击后可展开颜色列表,
选择所需颜色.

![](../assets/images/choose_channel.png)

## <a name="get" /> get

仅在此频道中按别名查询, 返回[CardHandle](card-handle.md),
[VariableHandle](variable-handle.md), Breaker或Placer; 使用的名称
空间与[`network:get`](network.md#get)相同. 频道中没有
匹配别名的成员时会报错.

<LuaCode>
```lua
local red = network:channel("red")
local counter = red:get("counter")  -- 红色频道上名为"counter"的变量
local door = red:get("door")     -- 红色频道上名为"door"的卡片
```
</LuaCode>

## <a name="getAll" /> <a name="getall" /> getAll

返回此频道中所有匹配类型成员的[HandleList](handle-list.md).
类型字符串与其他查询方法相同, 包括
[`network:getAll`](network.md#getAll), `"io"`, `"storage"`, `"redstone"`,
`"observer"`, `"variable"`, `"breaker"`, `"placer"`. 不传类型时,
返回频道中全部成员, 不限类型.

<LuaCode>
```lua
local red = network:channel("red")
red:getAll("observer"):onChange(function(block, state)
  print("red-channel observer fired:", block)
end)
```
</LuaCode>

## <a name="getFirst" /> <a name="getfirst" /> getFirst

返回此频道中第一个指定类型的成员, 无匹配时为`nil`.
适合每个频道中某种成员始终只有一个, 且不希望
再从HandleList中取值的情况.

<LuaCode>
```lua
local sensor = network:channel("blue"):getFirst("observer")
if sensor then
  print(sensor.name, "is the blue-channel observer")
end
```
</LuaCode>
