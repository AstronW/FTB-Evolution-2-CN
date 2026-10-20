---
navigation:
  parent: lua-api/index.md
  title: Importer
  icon: minecraft:hopper
categories:
  - api_types
  - api_preset
description: move items from A to B with a distribution strategy
---

# <a name="Importer" /> <a name="importer" /> Importer

全局对象`importer`用于构建物品搬运任务, 从一个或多个来源
取出物品, 存入一个或多个目标. 每个任务底层都由调度器
驱动, 按配置间隔持续运行, 直至
脚本停止或对句柄调用`:stop()`.

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

<LuaCode>
```lua
ImporterBuilder:filter(pattern: string): ImporterBuilder
```
</LuaCode>

将搬运范围限制为匹配过滤器的物品或流体. **可选.**
默认使用`*`, 移动所有物品. 使用的语法见
[Network:find](network.md#find), 包括`$item:id`, `$fluid:id`, `#tag`,
`modname:*`和正则表达式.

<LuaCode>
```lua
-- 仅移动圆石
importer:from(network)
  :filter("$item:minecraft:cobblestone")
  :to("io_*")
  :start()

-- 移动所有c:ores标签物品
importer:from("mobFarm"):filter("#c:ores"):to("storage"):start()
```
</LuaCode>

## <a name="Distribution" /> <a name="distribution" /> 分配方式

导入任务有两种目标分配方式. 默认依次
填充, 可显式切换为轮询.

### <a name="fill-(default)" /> <a name="fill-default" /> 依次填充(默认)

先填满第一个目标, 再将溢出物送至下一个,
依此类推. 适合有明确优先顺序, 希望先填满某箱子
再将多余物品送往其他地方的情况.

<LuaCode>
```lua
importer:from("furnaceOutput")
  :filter("$item:iron_ingot")
  :to("mainChest", "overflow")
  :start()
```
</LuaCode>

### <a name="roundrobin" /> roundrobin

<LuaCode>
```lua
ImporterBuilder:roundrobin(step: number?): ImporterBuilder
```
</LuaCode>

每个游戏刻均匀分配给所有目标. `step`为每刻
向每个目标送达的最大数量, 默认1. step=1且来源有三个物品时,
同一刻会给三个目标各送一个. 大批量运输时可
增大步长, 或通过`:every(1)`提高工作频率.

<LuaCode>
```lua
importer:from("bufferChest")
  :to("furnace1", "furnace2", "furnace3")
  :roundrobin()
  :every(10)
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

矿石以轮询方式送入三座熔炉, 产物集中到
中央箱子.

<LuaCode>
```lua
-- 将矿石均匀送入三座熔炉
importer:from("oreBuffer")
  :filter("$item:iron_ore")
  :to("furnace1", "furnace2", "furnace3")
  :roundrobin()
  :every(10)
  :start()

-- 从三座熔炉收集金属锭到输出箱
importer:from("furnace1", "furnace2", "furnace3")
  :filter("$item:iron_ingot")
  :to("outputChest")
  :start()
```
</LuaCode>

## <a name="see-also" /> 另见

* [预设共用方法](presets.md#shared-methods) (`:every`, `:start`,
  `:stop`, `:isRunning`).
* [Stocker](stocker.md)用于"维持库存"模式.
* [Network:find](network.md#find)介绍过滤语法.
