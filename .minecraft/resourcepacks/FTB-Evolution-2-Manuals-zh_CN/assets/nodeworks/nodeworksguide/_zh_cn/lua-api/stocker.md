---
navigation:
  parent: lua-api/index.md
  title: Stocker
  icon: minecraft:observer
categories:
  - api_types
  - api_preset
description: keep a target topped up by pulling, crafting, or both
---

# <a name="Stocker" /> <a name="stocker" /> Stocker

全局对象`stocker`构建库存维持任务. 设置目标容器,
`:keep(n)`库存线及来源, 可选择拉取, 合成或两者结合.
库存低于目标时自动补足, 达到目标后绝不抽取
多余物品, 因此玩家额外放入的物品会保留.

## <a name="three-source-modes" /> 三种来源模式

根据物品来源, 从以下三种工厂方法之一
开始构建调用链.

### <a name="from" /> from

<LuaCode>
```lua
Stocker:from(...sources: string | CardHandle | network): StockerBuilder
```
</LuaCode>

从指定卡片或网络池拉取, 不足时不合成. 适合
"从此缓存箱取货"或"从共享池取货, 空了就等待".
配合[`:filter`](./stocker.md#filter)可仅匹配指定物品类型; 不设
过滤器时, 会用任意物品将目标填充至`:keep(n)`数量.

<LuaCode>
```lua
-- 从两个指定箱子取箭
stocker:from("chest1", "chest2"):filter("$item:arrow"):to("dispenser"):keep(64):start()

-- 从网络池取货, 耗尽后等待
stocker:from(network):filter("$item:arrow"):to("dispenser"):keep(64):start()
```
</LuaCode>

### <a name="ensure" /> ensure

<LuaCode>
```lua
Stocker:ensure(itemId: string): StockerBuilder
```
</LuaCode>

先从网络池拉取, 不足部分再合成. 最常用的
形式, 适合"始终保有N个此物品". 需要准确
物品ID, 因为合成规划必须有具体产物.

<LuaCode>
```lua
stocker:ensure("minecraft:arrow"):to("dispenser"):keep(64):start()
stocker:ensure("minecraft:iron_ingot"):to(network):keep(256):start()
```
</LuaCode>

### <a name="craft" /> craft

<LuaCode>
```lua
Stocker:craft(itemId: string): StockerBuilder
```
</LuaCode>

始终通过合成维持库存, 不从已有存储中拉取. 适合
必须确保新制产物, 或原料稀缺而不希望
从共享箱子取用, 宁愿按需合成的场景.

<LuaCode>
```lua
stocker:craft("minecraft:bread"):to("foodChest"):keep(16):start()
```
</LuaCode>

## <a name="required-methods" /> 必需方法

### <a name="to" /> to

<LuaCode>
```lua
StockerBuilder:to(target: string | CardHandle | network): StockerBuilder
```
</LuaCode>

设置目标. 接受卡片别名, CardHandle对象或`network`,
后者表示"维持共享池本身的库存". 任务会统计目标中匹配物品,
使用`network`时统计所有存储卡.
存储卡目标仍遵守自身规则, 仅允许的物品会送入.

### <a name="keep" /> keep

<LuaCode>
```lua
StockerBuilder:keep(amount: number): StockerBuilder
```
</LuaCode>

目标库存数量. 补足至此数量后停止. 如果
当前数量超过目标, 例如玩家额外投入或其他脚本
输入, 则不作任何操作, 只补充而不抽取.

## <a name="optional-methods" /> 可选方法

### <a name="filter" /> filter

指定哪些物品计入`:keep(n)`, 以及`:from`取出什么. 省略则计入任意物品.
可传入多个规则, 多次调用, 或提供一个表.
不带参数调用会清空规则. **`:ensure`和`:craft`会自动设置
规则**, 因此只有使用`:from`时才需要手动指定.

<LuaCode>
```lua
stocker
  :from("buffer")
  :filter("$item:arrow")
  :to("dispenser")
  :keep(64)
  :start()
```
</LuaCode>

### <a name="except" /> except

指定不计入数量且不取出的物品, 即使`:filter`会接受它们.

<LuaCode>
```lua
-- 一组箭, 但不要药箭
stocker:from("buffer")
  :filter("#minecraft:arrows")
  :except("minecraft:tipped_arrow")
  :to("dispenser")
  :keep(64)
  :start()
```
</LuaCode>

### <a name="batch" /> batch

<LuaCode>
```lua
StockerBuilder:batch(size: number): StockerBuilder
```
</LuaCode>

将合成请求合并为此批量大小. 默认0表示"精确合成
缺少数量", 例如缺3个就合成3个, 不论配方成本多低.
设置`:batch(64)`后每次合成64个, 适合
启动成本较高的多原料或多步骤配方, 避免许多小批任务
反复占用CPU.

<LuaCode>
```lua
stocker:craft("minecraft:iron_ingot"):to("chest"):keep(64):batch(32):start()
-- 缺10个时合成整批32个, 交付后目标可能暂时有74个.
```
</LuaCode>

批次余量可能使目标库存暂时超过`:keep(n)`, 后续
游戏刻会保持不动, 直至库存再次降至目标线以下.

## <a name="example-arrow-dispenser-with-fallback-crafting" /> <a name="example:-arrow-dispenser-with-fallback-crafting" /> 示例: 可按需合成箭的发射器

<LuaCode>
```lua
stocker:ensure("minecraft:arrow")
  :to("trapDispenser")
  :keep(64)
  :batch(16)
  :every(20)
  :start()
```
</LuaCode>

每秒检查: 若发射器少于64支箭, 先从共享池取用,
仍不足则再合成16支. 重复直至补足发射器库存.

## <a name="see-also" /> 另见

* [预设共用方法](presets.md#shared-methods) (`:every`, `:start`,
  `:stop`, `:isRunning`).
* [Importer](importer.md)适合没有库存目标的持续A到B搬运.
* [Network:craft](network.md#craft)是底层合成接口.
