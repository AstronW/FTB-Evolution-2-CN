---
navigation:
  parent: lua-api/index.md
  title: Job
  icon: minecraft:paper
categories:
  - api_types
description: the first argument passed to a [network:handle callback](network.md#handle) and represents the in-flight processing job the handler is responsible for producing outputs for
---

# <a name="Job" /> <a name="job" /> Job

`Job`是你的[`network:handle`](network.md#handle)
函数收到的第一个参数. 每次网络需要执行加工
配方集中的配方时, 都会以新的`Job`和
从存储中取出的[原料](input-items.md)调用处理器. 处理器先将原料
送入机器, 再调用`job:pull(card)`, 告知网络
成品将从哪里取出.

## <a name="pull" /> pull

告诉网络成品会出现在哪里. 传入一张或多张
[CardHandle](card-handle.md), 网络会持续监视, 直至收集到
全部要求的产物数量.

若产物已在某张卡片中, 例如瞬时配方或
无序合成, 任务同一刻即可完成. 否则网络
每刻持续检查, 并取走卡片中已出现的物品, 因此
熔炉一次只产出一个金属锭也能正常工作.

<LuaCode>
```lua
local furnace = network:get("furnace")
network:handle("...", function(job: Job, items: InputItems)
  furnace:face("top"):insert(items.rawIron)
  -- 烧炼完成后从底面取出
  job:pull(furnace:face("bottom"))
end)
```
</LuaCode>

### <a name="multiple-source-cards" /> 多个来源卡片

若产物可能进入多个位置, 可传入多张卡片.
网络按顺序检查各卡片, 从其中有产物的位置
取走. 适合下游管道或漏斗按物品种类
将产物分配到不同箱子的情况.

<LuaCode>
```lua
local furnace = network:get("furnace")
local outboxA = network:get("outbox_a")
local outboxB = network:get("outbox_b")
network:handle("...", function(job: Job, items: InputItems)
  furnace:face("top"):insert(items.rawIron)
  -- 成品金属锭被分到两个箱子之一, 两边都可抽取
  job:pull(outboxA, outboxB)
end)
```
</LuaCode>

### <a name="put-items-in-first" /> 先放入原料

`:pull`只负责输出一侧. 你仍须自行将
[InputItems](input-items.md)送入机器. 若处理器返回时
`items.<slot>`还有剩余, 任务会被视为
未完成, 网络之后会重试配方.

### <a name="Timeout" /> <a name="timeout" /> 超时

产物始终未出现时, 合成最终会超时, 原料
返还存储. 各加工配方集都有自己的游戏刻超时设置,
可在界面调整, 默认为15秒. 大批烧炼或耗时较长的
模组配方等慢速机器应提高此值.

> **注意:** 处理器内的错误只会中止 *该次合成* , 不会
> 停止脚本其他部分. 任务意外卡住时, 请查看
> 终端日志中的错误.

## <a name="recipe" /> recipe

`Job`还会说明正在运行哪个加工配方集, 这样处理多个
配方的处理器, 例如[`network:recipes`](network.md#recipes)处理器,
就能对其中少数配方采用不同方式处理.

- `job.name`是配方集的名称, 与`network:handle`接受的名称相同.
- `job.inputs`按槽位顺序列出配方集的输入. 每项包含`id`和
  `count`, 若输入接受某标签的任意成员, 还会带有`tag`.
- `job.outputs`列出配方集的产物. 每项包含`id`, `count`和
  `optional`, 其中概率产物的该值为 true.

<LuaCode>
```lua
local furnace = network:get("furnace")
local blast = network:get("blast_furnace")
network:recipes("#c:raw_materials"):handle(function(job: Job, items: InputItems)
  -- 铁送往高炉, 其他物品送往普通熔炉.
  local machine = furnace
  if job.outputs[1].id == "minecraft:iron_ingot" then machine = blast end
  for _, input in ipairs(items:all()) do
    machine:face("top"):insert(input)
  end
  job:pull(machine:face("bottom"))
end)
```
</LuaCode>
