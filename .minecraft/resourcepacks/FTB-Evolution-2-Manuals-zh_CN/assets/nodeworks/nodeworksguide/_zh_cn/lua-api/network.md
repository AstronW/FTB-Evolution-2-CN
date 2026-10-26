---
navigation:
  parent: lua-api/index.md
  title: Network
  icon: node
categories:
  - api_builtin
description: query storage, route items, open craft jobs, register handlers
---

# <a name="Network" /> <a name="network" /> Network

`network`模块是访问<ItemLink id="terminal" />当前所连Nodeworks网络的
入口, 用于查询存储, 在句柄之间路由物品, 以及注册回调.

## <a name="get" /> get

按名称返回网络中对象的引用, 支持各种
<ItemLink id="storage_card" />, <ItemLink id="io_card" />, <ItemLink id="redstone_card" />,
<ItemLink id="observer_card" />或<ItemLink id="variable" />, 通常在
脚本开头获取. 卡片与变量重名时优先返回卡片.

也可点击脚本终端侧栏, 自动插入获取它们的代码.

![准备点击物品](../assets/images/click-to-add-card-01.png) ![点击物品后](../assets/images/click-to-add-card-02.png)

<GameScene zoom="5" interactive={true} paddingLeft="50" paddingRight="60">
  <ImportStructure src="../assets/assemblies/chest_furnace_terminal.snbt" />
  <BoxAnnotation min="1 1.1 0.1" max="1.25 1.9 0.9" color="#AA83E0">
    重命名为 **"chest"** <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="1 0.1 0.1" max="1.25 0.9 0.9" color="#83E086">
    重命名为 **"furnace"** <ItemImage id="nodeworks:io_card" />
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
local chest = network:get("chest")        -- 获取存储卡
local furnace = network:get("furnace")    -- 获取IO卡
local count = network:get("count")        -- 获取名为"count"的变量
```
</LuaCode>

---

## <a name="getAll" /> <a name="getall" /> getAll

返回全部匹配指定类型卡片或变量的[HandleList](handle-list.md).
HandleList会将写入方法, 如`:set`, `:onChange`等,
广播到每个成员, 因此一行就能切换多个活塞或给
多张侦测卡注册处理器. 如需逐项遍历, 调用`:list()`.

<GameScene zoom="5" interactive={true} paddingLeft="50" paddingRight="60">
  <ImportStructure src="../assets/assemblies/chest_connected_storage_card.snbt" />
  <BoxAnnotation min="2.25 1.1 0.1" max="2 1.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="2.25 0.1 0.1" max="2 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
-- 广播: 一次开启所有红石卡
network:getAll("redstone"):set(true)
-- 需要读取方法返回值时, 逐成员遍历
local storages = network:getAll("storage")
for _, storage in storages:list() do
    print(storage.name)
end
-- "storage_0"
-- "storage_1"
```
</LuaCode>

---

## <a name="cards" /> cards

返回名称匹配通配模式的卡片[HandleList](handle-list.md). 适合
同时操作多张遵循相同命名
规则的卡片.

<LuaCode>
```lua
local allPistonCards = network:cards("piston_*")
allPistonCards:set(true) -- 开启所有活塞
```
</LuaCode>

---

## <a name="channel" /> <a name="channel-getall" /> channel

将查询范围限制为一种染料颜色频道, 返回[`Channel`](./channel.md)句柄.
其中`:get`, `:getAll`和`:getFirst`只能看到设置为
该颜色的卡片, 变量和设备, 使用相同频道过滤. 未知颜色会报错.

<LuaCode>
```lua
local red = network:channel("red")
red:getAll("redstone"):set(true) -- 仅红色频道的活塞
local count = red:get("counter") -- 红色频道上的变量
```
</LuaCode>

---

## <a name="channels" /> channels

返回网络中当前使用的所有染料颜色频道列表,
只要至少有一张卡片, 一个变量, 破坏器或放置器
使用该颜色就会列出. 按`DyeColor`的ID升序排列, 遍历顺序稳定,
适合在运行时发现频道, 而非硬编码列表.

> **注意:** 新成员的默认频道为`white`, 因此几乎所有非空网络
> 都会在这里列出它.

<LuaCode>
```lua
for _, color in network:channels() do
  print(color, "is in use")
end
-- "white"正在使用
-- "red"正在使用
-- "blue"正在使用
```
</LuaCode>

常见用法是在每个活动频道运行同一处理逻辑,
无需关心玩家选了哪些颜色.

<LuaCode>
```lua
for _, color in network:channels() do
  network:channel(color):getAll("redstone"):set(false)
end
```
</LuaCode>

---

## <a name="find" /> find

扫描全部[网络存储](../nodeworks-mechanics/network-storage.md),
查找匹配过滤器的物品或流体, 返回汇总句柄 *(数量为各存储之和)* ,
无匹配时返回`nil`.

<LuaCode>
```lua
local all = network:find("*") -- 若有内容则获取全部物品与流体
local allItems = network:find("$item:*") -- 仅物品
local allFluids = network:find("$fluid:*") -- 仅流体
local allCoal = network:find("minecraft:coal") -- 物品ID
local allLogs = network:find("#minecraft:logs") -- 标签
local allRaw = network:find("/^Raw.*/") -- 正则表达式
```
</LuaCode>

使用`:find`返回的物品前, 应先检查是否有匹配结果.

<LuaCode>
```lua
local allCoal = network:find("minecraft:coal")
if allCoal then
  print("we have coal")
end
```
</LuaCode>

---

## <a name="findEach" /> <a name="findeach" /> findEach

类似[find](./network.md#find), 扫描全部[网络存储](../nodeworks-mechanics/network-storage.md),
寻找匹配过滤器的物品或流体, 但返回[ItemsHandle](./items-handle.md)列表.
各项按物品ID及是否具有NBT数据区分.

<LuaCode>
```lua
for _, items in network:findEach("$item:*") do
  print(items.id, items.count, items.kind)
end
```
</LuaCode>

例如网络中有附魔和未附魔的钻石剑,
它们会被分为不同条目.

<LuaCode>
```lua
for _, items in network:findEach("minecraft:diamond_sword") do
  print(items.id, items.hasData)
end
-- "minecraft:diamond_sword" true
-- "minecraft:diamond_sword" false
```
</LuaCode>

---

## <a name="count" /> count

返回[网络存储](../nodeworks-mechanics/network-storage.md)中匹配过滤器的
总数量, 流体以mB计.

过滤语法与[find](network.md#find)完全相同.

<LuaCode>
```lua
print("swords:", network:count("minecraft:diamond_sword"))
print("cobblestone:", network:count("minecraft:cobblestone"))
print("all:", network:count("*"))
-- "swords:" 3
-- "cobblestone:" 256
-- "all:" 259
```
</LuaCode>

---

## <a name="insert" /> insert

将[ItemsHandle](items-handle.md)中的资源送入[网络存储](../nodeworks-mechanics/network-storage.md), 遵守标准
<ItemLink id="storage_card" />优先级. 必须能装下每一个物品, 否则
完全不移动, 返回`false`. 需要尽力而为的部分输入时,
请使用[tryInsert](./network.md#tryinsert).

<LuaCode>
```lua
local ok = network:insert(items)
if ok then
  print("all items were moved")
else
  print("no items were moved, not enough space")
end
```
</LuaCode>

---

## <a name="tryInsert" /> <a name="tryinsert" /> tryInsert

类似[`insert`](network.md#insert), 但只移动能装下的部分,
不要求全部成功. 返回实际送达数量, 范围0至请求数量.
未装下的部分留在来源中, 适合允许部分移动的场景.

<LuaCode>
```lua
local moved = network:tryInsert(items)
print(moved .. " items were moved") -- 可以是0至items.count
```
</LuaCode>

---

## <a name="craft" /> craft

(另见[自动合成](../nodeworks-mechanics/autocrafting.md).)

为指定物品排队合成, 返回[CraftBuilder](./craft-builder.md).
默认情况下, 成品在合成完成后会自动存入
[网络存储](../nodeworks-mechanics/network-storage.md),
无需链式调用:

<LuaCode>
```lua
-- 发起后无需处理: 面包就绪后自动入库
network:craft("minecraft:bread", 4)
```
</LuaCode>

链式调用`:connect(fn)`可自行接收结果. 回调收到
[ItemsHandle?](items-handle.md), 成功时非空, 失败时为`nil`, 如规划
失败, 异步超时或没有CPU. 调用`:connect`会覆盖自动入库行为.

<LuaCode>
```lua
local furnace = network:get("furnace")
network:craft("minecraft:charcoal"):connect(function(item: ItemsHandle?)
  if item then
    furnace:insert(item)
  end
end)
```
</LuaCode>

---

## <a name="shapeless" /> shapeless

立即使用[网络存储](../nodeworks-mechanics/network-storage.md)中的原料执行无序配方.
配方无效或缺少原料时, 不进行合成,
返回`nil`.

<LuaCode>
```lua
-- 合成打火石, 产物自动存入网络存储.
network:shapeless("minecraft:flint", 1, "minecraft:iron_ingot", 1)
```
</LuaCode>

---

## <a name="handle" /> handle

(另见[自动合成](../nodeworks-mechanics/autocrafting.md).)

为网络内的<ItemLink id="processing_set" />注册加工处理器.
处理器会收到原料, 并必须使用传入的[Job](job.md)来`pull`
产物. 传入[InputItems](input-items.md)的全部物品 **必须**
由处理器取走.

<GameScene zoom="5" interactive={true} paddingTop="40" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/processing_storage_single_entry.snbt" />
  <BoxAnnotation min="1.9 0.1 0.75" max="1.1 0.9 1" color="#83E086">
    重命名为 **"furnace"** <ItemImage id="nodeworks:io_card" />
  </BoxAnnotation>
  <BlockAnnotation x="0" y="0" z="0">
    <Row>
      <ItemImage id="minecraft:raw_iron" />
      **➜**
      <ItemImage id="minecraft:iron_ingot" />
    </Row>
  </BlockAnnotation>
</GameScene>

<LuaCode>
```lua
local furnace = network:get("furnace")
-- 粗铁->铁锭的处理器
network:handle("…", function(job: Job, items: InputItems)
  furnace:face("top"):insert(items.rawIron)
  job:pull(furnace:face("bottom"))
end)
```
</LuaCode>

---

## <a name="recipes" /> recipes

使用一个函数处理多个加工配方集. 指定配方集所需的输入,
所有输入都符合规则的配方集就会交给这个处理器. 后续加入
网络的配方集也会自动纳入, 无需重启脚本.

<LuaCode>
```lua
local furnaces = network:get("furnaces")

local function smelt(job: Job, items: InputItems)
  for _, input in items:all() do
    furnaces:face("top"):insert(input)
  end
  job:pull(furnaces:face("bottom"))
end

network
  :recipes("#c:ores", "#c:raw_materials")
  :except("mod:uranium", "mod:other_ore")
  :handle(smelt)
```
</LuaCode>

### <a name="which-sets-match" /> 哪些配方集符合规则

- **`network:recipes(...)`**: 配方集的每项输入都必须符合这些
  规则之一. 只筛选金属锭时, 还需要煤的配方集会被排除,
  因而不会混入合金配方. 不提供规则则匹配所有配方集.
- **`:except(...)`**: 任一输入符合这些规则的配方集都会被排除.
- **`:outputs(...)`**: 可选. 配方集所有必定产出的物品也必须
  符合这些规则之一. 当同一输入会交给不同
  机器时可使用, 例如粗铁送入熔炉制锭, 或送入粉碎机制粉.
  不检查概率产物.

<LuaCode>
```lua
-- 原材料, 但只匹配产出金属锭的配方集.
network:recipes("#c:raw_materials"):outputs("#c:ingots"):handle(smelt)
```
</LuaCode>

规则语法与[存储卡筛选器](../items-blocks/storage_card.md#filters)相同,
因此物品 ID, `#tags`和`*`通配符都可以使用.

### <a name="who-wins" /> 优先顺序

- 为配方集精确指定的[`network:handle`](./network.md#handle)始终优先于`recipes`处理器.
- 绑定到<ItemLink id="processing_handler" />或<ItemLink id="multi_processing_handler" />的配方集
  仍由对应方块负责. 宽泛规则不会夺走你在方块上勾选的配方集.
- 两个`recipes`处理器都匹配同一配方集时, 优先使用先注册的处理器.

### <a name="one-craft-at-a-time" /> 每次只运行一次合成

`recipes`处理器一次只运行一次合成, 因为这些配方通常共用
相同机器. 其他需要它的合成会等待轮到自己,
避免争用熔炉. 如果各配方从不共用机器, 例如
一组熔炉中每台都处理不同输入, 可调用`:parallel()`, 让
多次合成同时进行.

<LuaCode>
```lua
network:recipes("#c:raw_materials"):parallel():handle(smelt)
```
</LuaCode>

### <a name="stopping-and-checking" /> 停止与查询

`:handle`返回一个处理器, 可停止它, 或查询当前由它处理的配方集.

<LuaCode>
```lua
local ores = network:recipes("#c:ores"):handle(smelt)
for _, line in ipairs(ores:sets()) do
  print(line) -- minecraft:raw_iron -> minecraft:iron_ingot
end
ores:stop()
```
</LuaCode>

从[`job`](job.md#recipe)读取每次合成的详细信息, 输入则来自
[`items:all()`](input-items.md#all).

---

## <a name="route" /> route

批量编辑名称匹配模式的所有卡片的[过滤设置](../items-blocks/storage_card.md#filters),
卡片类型为<ItemLink id="storage_card" />. 返回可链式调用的构建器,
一组卡片的完整规则集可以用
一条调用设置. 每个方法立即修改匹配卡片, 等同于
逐张右击并在界面中手动编辑.

名称模式用`*`作通配符. `cobblestone_*`匹配`cobblestone_0`,
`cobblestone_1`等. 单独使用`*`匹配网络中所有存储卡.

<LuaCode>
```lua
network:route("cobblestone_*")
  :reset()
  :rule("#c:cobblestones")
  :noNbt()
  :allow()
```
</LuaCode>

### <a name="builder-methods" /> 构建器方法

| 方法 | 效果 |
| ------------------------------------------------------ | ------------------------------------------------- |
| `:rule(filter)` | 追加规则, 与界面规则列表语法相同 |
| `:clearRules()` | 删除全部规则, 保留模式 |
| `:allow()`/`:deny()` | 设置规则列表模式 |
| `:stackable()`/`:nonStackable()`/`:anyStackable()` | 设置可堆叠性过滤 |
| `:hasNbt()`/`:noNbt()`/`:anyNbt()` | 设置NBT过滤 |
| `:reset()` | 清除规则, 设为允许+任意+任意 |

调用返回同一构建器, 因此可链式组合. 修改立即生效,
并在保存和加载后保留.

---

## <a name="debug" /> debug

打印网络拓扑摘要.

<LuaCode>
```lua
network:debug()
-- === 网络调试 ===
-- 控制器: BlockPos{x=-25, y=70, z=10}
-- 节点: 1
--   节点BlockPos{x=-25, y=70, z=9}: 1张卡片
--     NORTH: cobblestone_storage (storage)
-- 终端: 1
--   BlockPos{x=-26, y=70, z=9}
-- CPU: 0
-- 合成器(合成指令集): 0
-- 加工API: 0
-- 变量: 0
```
</LuaCode>
