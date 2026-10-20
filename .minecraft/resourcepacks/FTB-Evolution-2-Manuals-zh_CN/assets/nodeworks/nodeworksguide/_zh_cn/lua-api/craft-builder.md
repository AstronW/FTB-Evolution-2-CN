---
navigation:
  parent: lua-api/index.md
  title: CraftBuilder
  icon: minecraft:crafting_table
categories:
  - api_types
description: returned by [`network:craft`](network.md#craft) and configures how the craft result is delivered once it completes
---

# <a name="CraftBuilder" /> <a name="craftbuilder" /> CraftBuilder

`CraftBuilder`由[`network:craft`](network.md#craft)返回,
表示网络已规划但尚未交付的合成任务. 默认情况下,
合成完成时产物会进入[网络存储](../nodeworks-mechanics/network-storage.md).
如需改用回调, 请链式调用`:connect(fn)`.

合成可能在同一游戏刻内完成, 如用存储原料执行原版配方,
也可能需要许多游戏刻, 如经由
[`network:handle`](network.md#handle)加工处理器, 或多阶段
合成树. 两种情况的构建器API相同.

> **注意:** `network:craft`始终返回构建器, 即使
> 无法规划任务, 例如无配方, 缺原料或无合成CPU.
> 失败会通过`:connect`回调中的`nil`传达.

## <a name="default-stores-the-result" /> <a name="default:-stores-the-result" /> 默认: 存储产物

不进行链式调用时, 成品自动送入网络
存储, 遵守正常[存储卡](../items-blocks/storage_card.md)
优先级与[`network:route`](network.md#route)规则. 随后可像存储池中
其他物品一样通过`network:find`查询.

<LuaCode>
```lua
-- 发起后无需处理: 合成16支火把, 产物自动入库
network:craft("minecraft:torch", 16)
```
</LuaCode>

## <a name="connect" /> connect

将成品交给回调, **替代** 自动存储.
调用`:connect`会取消构建器的默认行为,
运行时不会自动入库, 回调负责处理产物.

回调参数为`ItemsHandle?`: 成功时为[ItemsHandle](items-handle.md),
失败时为`nil`. 使用前务必检查.

<LuaCode>
```lua
local oven = network:get("oven")
network:craft("minecraft:bread", 4):connect(function(items: ItemsHandle?)
  if not items then
    print("bread craft failed")
    return
  end
  oven:insert(items) -- 成品面包直接送入烤箱
end)
```
</LuaCode>

任务结束时回调执行一次. 以下失败情况会以
`nil`表示:

- 规划失败: 无配方, 缺少原料或网络中没有合成CPU.
- 异步超时: 加工处理器始终未交付产物.
- CPU离线: 合成过程中合成CPU被破坏或移除.

所有失败情况都会将CPU缓存中已有的部分物品返还
网络存储, 避免物品滞留.

### <a name="you&#x27;re-responsible-for-moving-the-items" /> <a name="youre-responsible-for-moving-the-items" /> 你负责移走物品

回调收到的句柄是 **仍留在合成CPU缓存中的
物品的实时引用**. 调用`card:insert(items)`/
`network:insert(items)`才会将物品从缓存移入目标.

回调返回时仍留在缓存中的物品会 **掉落在
CPU位置**, 同时向终端记录错误. 此接口的约定是:
"接收句柄后就负责移动物品". 未取走物品
不会悄无声息地被忽略.

<LuaCode>
```lua
local chest = network:get("ore_chest")
network:craft("minecraft:iron_ingot", 8):connect(function(items: ItemsHandle?)
  if not items then return end
  if not chest:insert(items) then
    -- 箱子已满: 改为存入网络, 避免掉落
    network:insert(items)
  end
end)
```
</LuaCode>

这与自动存储刻意区分. 自动存储始终经由
网络存储卡路由, 只有所有存储卡都拒收时才掉落到世界.
使用`:connect`时, 回调决定物品去向,
运行时假定你会真正移动这些物品.

> **注意:** 回调中抛出的错误会记录到终端, 但
> 不会使脚本的其他部分停止.

## <a name="when-connect-runs-synchronously" /> connect同步运行的情况

原料已在存储中的原版配方会在同一
游戏刻内完成. 回调仍使用同一套机制, 仅比
`:craft`调用晚一刻, 以便`:connect`在任务结算前完成
注册. 无需特殊处理, 同步与异步合成的API
行为相同.

<LuaCode>
```lua
-- 无论立即合成完成, 还是需要烧炼30s, 用法都相同
network:craft("minecraft:iron_ingot", 8):connect(function(items: ItemsHandle?)
  if items then chest:insert(items) end
end)
```
</LuaCode>
