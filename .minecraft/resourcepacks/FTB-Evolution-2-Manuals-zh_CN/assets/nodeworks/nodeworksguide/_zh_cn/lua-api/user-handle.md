---
navigation:
  parent: lua-api/index.md
  title: UserHandle
  icon: user
categories:
  - api_types
description: a device that right-clicks with an item in front of it
---

# <a name="UserHandle" /> <a name="userhandle" /> UserHandle

`UserHandle`引用网络中的<ItemLink id="user" />,
由[`network:get(name)`](network.md#get)返回. 从
[网络存储](../nodeworks-mechanics/network-storage.md)取出一个物品,
并用它右击方块正前方的目标.

<BlockImage scale="6" id="user" />

使用器有两种模式. **立即** 模式下, 每次
`:use()`调用执行一次右击. **按住** 模式会持续
按住右键, 直至调用`:stop()`, 物品完成操作, 或
30秒超时. 过滤器语法与
<ItemLink id="storage_card" />规则相同.

## <a name="Properties" /> <a name="properties" /> 属性

- **`.name`**
  - 使用器别名, 与终端侧栏的名称相同
- **`.kind`**
  - 始终为`"user"`

## <a name="use" /> use

启动使用器. **立即** 模式执行一次右击, 返回
操作是否成功. **按住** 模式开始持续使用, 返回
是否成功进入按住状态.

以下情况返回`false`且不会启动: 使用器已在使用, 正在
冷却, 被过滤器阻止, 存储中无匹配物品, 或
网络中没有控制器.

<LuaCode>
```lua
local farmer = network:get("crop_farmer")
farmer:use()
```
</LuaCode>

要重新开始按住操作, 应先调用`:stop()`.

## <a name="stop" /> stop

取消尚未执行的单次使用, 或释放正在进行的按住操作. 空闲时
调用安全, 不报错并返回`false`. 将预留物品返还网络存储的
收回动画不可取消.

<LuaCode>
```lua
local user = network:get("user_1")
local watcher = network:get("observ_1")
user:setMode("hold")
user:use() -- 开始在可疑方块上使用刷子
-- 方块变为普通沙子或沙砾时, 停止使用器
watcher:onChange(function(block: BlockId, state: any)
    if block == "minecraft:gravel" or block == "minecraft:sand" then
        user:stop()
    end
end)
```
</LuaCode>

## <a name="isUsing" /> <a name="isusing" /> isUsing

正在按住使用时返回`true`, 否则返回`false`.

<LuaCode>
```lua
local user = network:get("user_1")
if not user:isUsing() then
  user:use()
end
```
</LuaCode>

## <a name="mode" /> mode

以字符串返回当前模式, 为`"instant"`或`"hold"`.

<LuaCode>
```lua
local user = network:get("user_1")
print(user:mode()) -- "instant"
```
</LuaCode>

## <a name="setMode" /> <a name="setmode" /> setMode

设置使用器模式, 接受`"instant"`或`"hold"`, 不区分大小写.

<LuaCode>
```lua
local user = network:get("crop_farmer")
user:setMode("hold")
```
</LuaCode>

## <a name="filter" /> filter

返回当前过滤规则字符串, 未设置时为空.

<LuaCode>
```lua
local user = network:get("user_1")
print(user:filter()) -- "minecraft:bone_meal"
```
</LuaCode>

## <a name="setFilter" /> <a name="setfilter" /> setFilter

设置使用器过滤规则. 使用与
<ItemLink id="storage_card" />相同的语法, 因此普通物品ID,
`#namespace:tag`, `minecraft:*`, `/regex/`, 以及`$item:`/`$fluid:`
前缀均有效.

<LuaCode>
```lua
local user = network:get("crop_farmer")
user:setFilter("minecraft:bone_meal")
```
</LuaCode>

## <a name="facing" /> facing

以小写字符串返回使用器朝向.
(`"north"`, `"south"`, `"east"`, `"west"`, `"up"`, `"down"`).

<LuaCode>
```lua
local user = network:get("user_1")
print(user:facing()) -- "north"
```
</LuaCode>
