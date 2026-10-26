---
navigation:
  parent: lua-api/index.md
  title: Importer
  icon: minecraft:hopper
categories:
  - api_types
  - api_preset
description: move items and fluids from A to B with a distribution strategy
---

# <a name="Importer" /> <a name="importer" /> Importer

全局对象`importer`用于创建搬运任务, 从一个或
多个来源取出物品和流体, 再送入一个或多个目标. 每个输入器
本质上都是定时任务, 会按配置的间隔持续运行,
直到脚本停止, 或你对其句柄调用`:stop()`.

## <a name="from" /> from

<LuaCode>
```lua
Importer:from(...sources: string | CardHandle | network): ImporterBuilder
```
</LuaCode>

开始构建导入任务链. 来源可混用卡片别名, CardHandle
对象或全局`network`, 后者表示整个网络存储池.
至少需要一个来源.

<LuaCode>
```lua
importer:from("farmChest")                        -- 一个具名来源
importer:from(network)                            -- 网络存储池作为来源
importer:from("chestA", network, network:get("chestB"))  -- 混用来源
```
</LuaCode>

## <a name="to" /> to

<LuaCode>
```lua
ImporterBuilder:to(...targets: string | CardHandle | network): ImporterBuilder
```
</LuaCode>

设置目标, 与`:from`一样支持多种形式: 卡片别名, CardHandle
对象或表示存储池的`network`. 至少需要一个目标.

以存储卡为目标时, 仍遵守该卡自己的规则. 只有规则列表,
可堆叠性和数据过滤器允许的物品才会送入, 行为与
`network:insert`相同. 即使导入任务的过滤器放宽, 仅接受护甲的卡片
也仍然只接收护甲, 不受`:filter`覆盖.

<LuaCode>
```lua
importer:from("farm"):to("storage1", "storage2"):start()
importer:from("mobFarm"):to(network):start()  -- 存入共享池
```
</LuaCode>

## <a name="filter" /> filter

指定搬运内容. 符合任一规则的物品都会搬运; 省略则搬运所有内容. 筛选语法与[Network:find](network.md#find)相同.

可多次调用`:filter()`来添加多个筛选条件, 不带参数调用则会重置筛选器.

<LuaCode>
```lua
importer
  :from(network)
  :filter("$item:minecraft:cobblestone")
  :filter("$item:minecraft:stone")
  :to("io_*")
  :start()

local puller = importer
  :from("quarry")
  :filter("#c:ores")
  :to(network)

puller:filter() -- 重置筛选器
puller:start() -- 启动输入器
```
</LuaCode>

## <a name="except" /> except

指定明确 **不想** 搬运的物品.

<LuaCode>
```lua
-- 所有矿石, 但排除熔炉无法冶炼的那一种
importer
  :from(network)
  :to("furnace_*")
  :filter("#c:ores")
  :except("mod:uranium")
  :roundrobin()
  :start()

-- 清空机器, 但留下其中的矿渣
importer:from("crusher"):to(network):except("mod:slag"):start()
```
</LuaCode>

## <a name="Fluids" /> <a name="fluids" /> 流体

输入器也能搬运流体. 规则可以指定流体, `$fluid:`用于选择
与物品同名的流体. 数量以毫桶计, 一桶为`1000`. 没有储罐的目标在搬运流体时会被跳过.

<LuaCode>
```lua
importer
  :from(network)
  :to("boiler")
  :filter("$fluid:minecraft:water")
  :start()
```
</LuaCode>

## <a name="Distribution" /> <a name="distribution" /> 分配方式

输入器有两种向多个目标分配内容的方式.
默认依次填满, 轮询分配则需显式启用.

### <a name="fill-(default)" /> <a name="fill-default" /> 依次填充(默认)

先填满第一个目标, 再将溢出物送至下一个,
依此类推. 适合有明确优先顺序, 希望先填满某箱子
再将多余物品送往其他地方的情况.

<LuaCode>
```lua
importer
  :from("furnaceOutput")
  :filter("$item:iron_ingot")
  :to("mainChest", "overflow")
  :start()
```
</LuaCode>

### <a name="roundrobin" /> roundrobin

向每个目标均匀分配. 可提供一个数字, 指定每个目标每轮得到多少, 默认 1.
搬运物品时单位为个, 搬运流体时单位为毫桶,
因此流体输入器可将步长设为 1000, 每轮每个目标得到一桶.

<LuaCode>
```lua
importer
  :from("bufferChest")
  :to("furnace1", "furnace2", "furnace3")
  :roundrobin()
  :start()

importer
  :from(network)
  :to("boiler_*")
  :filter("$fluid:minecraft:water")
  :roundrobin(1000)
  :start()
```
</LuaCode>

轮询游标每刻前移一位, 因此即使来源不足,
某刻只有部分目标收到物品, 也能保持公平分配.

## <a name="wildcards-in-card-aliases" /> 卡片别名中的通配符

`:from`和`:to`均支持卡片名称中的`*`通配符. 传入一个
`"io_*"`, 会在导入任务解析快照时展开为所有匹配别名的
卡片, 并在网络拓扑
变化时重新展开.

<LuaCode>
```lua
-- 从一个箱子分配到所有名为io_...的卡片
importer:from("input"):to("io_*"):roundrobin():start()

-- 从一组来源箱子汇集到单个输出箱
importer:from("farm_*"):to("storage"):start()
```
</LuaCode>

## <a name="example-two-stage-smelter-array" /> <a name="example:-two-stage-smelter-array" /> 示例: 两段式熔炉阵列

将矿石和原材料轮询送入所有熔炉, 再将加工完成的金属锭
收回网络.

<LuaCode>
```lua
local furnaces = network:cards("furnace_*")

-- 向熔炉均匀供料
importer:from(network)
  :to(furnaces:face("top"))
  :filter("#c:ores", "#c:raw_materials")
  :except("mod:uranium")
  :roundrobin()
  :every(10)
  :start()

-- 收集所有产物
importer:from(furnaces:face("bottom"))
  :to(network)
  :start()
```
</LuaCode>

## <a name="see-also" /> 另见

* [预设共用方法](presets.md#shared-methods) (`:every`, `:start`,
  `:stop`, `:isRunning`).
* [Stocker](stocker.md)用于"维持库存"模式.
* [Network:find](network.md#find)介绍过滤语法.
