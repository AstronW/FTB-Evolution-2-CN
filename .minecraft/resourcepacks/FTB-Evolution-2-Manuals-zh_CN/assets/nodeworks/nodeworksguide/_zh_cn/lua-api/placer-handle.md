---
navigation:
  parent: lua-api/index.md
  title: PlacerHandle
  icon: placer
categories:
  - api_types
description: a device to place blocks in front of it
---

# <a name="PlacerHandle" /> <a name="placerhandle" /> PlacerHandle

`PlacerHandle`引用网络中的<ItemLink id="placer" />,
由[`network:get(name)`](network.md#get)返回. 它从
[网络存储](../nodeworks-mechanics/network-storage.md)取出一个指定物品,
作为方块放在放置器正前方.

<BlockImage scale="6" id="placer" />

`:place(...)`同步执行, 在脚本调用的同一刻返回`true`/`false`.
没有跨刻进度, 构建器或回调. 仅支持
`BlockItem`, 即具有可放置方块形态的物品; 工具, 食物
等不可放置物品会立即失败.

## <a name="Properties" /> <a name="properties" /> 属性

- **`.name`**
  - 放置器别名, 与终端侧栏显示的名称相同

## <a name="place" /> place

从网络存储取出一个指定物品, 放到
放置器正前方. 成功时返回`true`.

参数可为物品ID字符串或[ItemsHandle](./items-handle.md).
传入句柄时, 放置器读取`.id`, 从网络池取出 *该物品*
一个, 与直接传入字符串相同. 不会从句柄自身的
来源抽取, 而是从网络存储卡取出.

<LuaCode>
```lua
local placer = network:get("placer_1")
placer:place("minecraft:cobblestone")
```
</LuaCode>

以下情况返回`false`, 且不放置物品:
- 网络中没有可用的匹配物品
- 目标位置不是空气
- 物品不是可放置方块, 如`minecraft:diamond`, `minecraft:stick`

<LuaCode>
```lua
local placer = network:get("bridge_builder")
local ok = placer:place("minecraft:oak_planks")
if not ok then
  print("nothing placed, no planks in storage or target blocked")
end
```
</LuaCode>

## <a name="block" /> block

返回放置器正前方方块的ID, 形式与
[`ObserverCard:block`](./card-handle.md#observer-card)相同. 调用前可检查
"位置是否仍为空/是否为预期方块", 然后再调用`:place`.

<LuaCode>
```lua
local placer = network:get("placer_1")
if placer:block() == "minecraft:air" then
  placer:place("minecraft:torch")
end
```
</LuaCode>

## <a name="isBlocked" /> <a name="isblocked" /> isBlocked

目标位置不可替换时返回`true`, 即既非空气, 也不是
草或雪等可替换方块; 能成功放置时返回`false`. 如果只想
判断位置是否空闲, 比调用`:place`再检查
返回值开销更小.

<LuaCode>
```lua
local placer = network:get("placer_1")
if not placer:isBlocked() then
  placer:place("minecraft:cobblestone")
end
```
</LuaCode>
