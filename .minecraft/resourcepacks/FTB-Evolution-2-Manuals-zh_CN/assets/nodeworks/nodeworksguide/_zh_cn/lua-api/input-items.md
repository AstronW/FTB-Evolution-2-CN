---
navigation:
  parent: lua-api/index.md
  title: InputItems
  icon: minecraft:cobblestone
categories:
  - api_types
description: the second argument passed to [network:handle callbacks](network.md#handle) a per-recipe bag of [`ItemsHandle`](items-handle.md) fields keyed by the recipe's input slot names
---

# <a name="InputItems" /> <a name="inputitems" /> InputItems

`InputItems`是你的[`network:handle`](network.md#handle)
函数收到的第二个参数. 网络已替你将配方原料
从存储中取出, 放在这张表中, 每个输入
槽对应一个字段. 你的任务是把这些原料送入实际机器.

每个字段都是完整的[ItemsHandle](items-handle.md), 可像其他句柄一样调用`:insert`,
`:tryInsert`, `:count`等方法.

## <a name="field-names" /> 字段名

字段名由 **输入物品ID转换为小驼峰命名** . 例如
`minecraft:raw_iron`变为`items.rawIron`, `minecraft:copper_ingot`
变为`items.copperIngot`. 脚本编辑器会根据处理的配方
自动补全正确名称, 无需记忆.

<LuaCode>
```lua
local furnace = network:get("furnace")
network:handle("...", function(job: Job, items: InputItems)
  furnace:face("top"):insert(items.rawIron) -- minecraft:raw_iron
  job:pull(furnace:face("bottom"))
end)
```
</LuaCode>

### <a name="duplicate-ingredients" /> 重复原料

同一种原料在配方多个槽位中出现时, 第二次
加后缀`2`, 第三次加`3`, 依此类推. 因此需要
两个铜锭和一个金锭的配方会提供以下字段:
`items.copperIngot`, `items.goldIngot`, `items.copperIngot2`.

<LuaCode>
```lua
local press = network:get("press")
network:handle("...", function(job: Job, items: InputItems)
  press:face("top"):insert(items.copperIngot)
  press:face("top"):insert(items.copperIngot2)
  press:face("north"):insert(items.goldIngot)
  job:pull(press:face("bottom"))
end)
```
</LuaCode>

## <a name="all" /> all

按配方所列顺序, 将所有输入作为列表返回. 当
同一个处理器处理多个配方, 且不同配方的字段名
不同时使用, 例如[`network:recipes`](network.md#recipes).

<LuaCode>
```lua
local furnace = network:get("furnace")
network:handle("...", function(job: Job, items: InputItems)
  for _, input in ipairs(items:all()) do
    furnace:face("top"):insert(input)
  end
  job:pull(furnace:face("bottom"))
end)
```
</LuaCode>

列表中的句柄与具名字段持有的是同一对象, 因此移动
`items.rawIron`也会清空列表中对应的条目.

## <a name="you-must-use-everything" /> 必须用完全部原料

处理器应将所有原料送入机器. 如果返回时
`items.<slot>`中还有剩余, 网络会将
合成视为未完成, 稍后重试配方. 不存在"跳过此
原料"模式; 配方要求N个铜锭, 就必须让N个铜锭
有实际去向.

> **注意:** "用完"指送入任何可达的位置, 通过
> `network:insert`存回网络也算. 检查只关心"脚本是否消耗了
> 交给它的原料", 不检查"是否送入正确机器".
