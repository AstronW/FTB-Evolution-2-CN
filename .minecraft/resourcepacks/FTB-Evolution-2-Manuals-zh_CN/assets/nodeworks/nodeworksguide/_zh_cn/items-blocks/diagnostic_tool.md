---
navigation:
  parent: items-blocks/index.md
  icon: diagnostic_tool
  title: 诊断工具
categories:
  - tool
description: inspect a network's topology, CPUs, scripts, and recent errors
item_ids:
- nodeworks:diagnostic_tool
---

# <a name="diagnostic-tool" /> 诊断工具

用于检查Nodeworks网络的手持工具. 右击任意
网络方块可打开诊断面板, 汇总网络的全部
组成部分及其当前工作情况.

<ItemImage scale="6" id="diagnostic_tool" />

## <a name="how-to-use-it" /> 使用方法

右击目标网络中的任意方块即可,
<ItemLink id="node" />, <ItemLink id="terminal" />,
<ItemLink id="network_controller" />, 天线或存储方块都
有效. 也可点击
[合成CPU](crafting_cpu.md)多方块结构中的任意部分(核心, 缓存, 冷却块,
基板, 协处理器), 工具会遍历相连结构, 自动找到
核心.

如果点击的方块不属于网络, 工具会显示
提示消息, 不会打开面板.

## <a name="what-it-shows" /> 显示内容

诊断面板汇总网络所提供的全部信息:

- **拓扑** : 网络中的每个方块, 包括位置, 类型和
  各自详情. <ItemLink id="node" />会列出各面的卡片,
  以及它们所操作的相邻方块.
- **网络标识** : 控制器名称和颜色, 以及
  红石模式, 处理器重试上限和区块加载
  开关.
- **CPU** : 网络中的各个<ItemLink id="crafting_core" />,
  当前合成任务, 缓存使用量, 效率, 以及
  多方块结构是否正确组装.
- **终端** : 网络中的每个<ItemLink id="terminal" />,
  包括脚本列表, 自动运行标记, 运行状态, 以及
  各运行脚本注册的[加工配方集](recipe_sets.md#processing-set)
  处理器.
- **可合成物品** : 网络能自动合成的完整物品列表,
  从所有<ItemLink id="instruction_storage" />
  和<ItemLink id="processing_storage" />收集.
- **近期错误** : 网络中各终端最近10条脚本错误,
  通过游戏刻偏移显示距发生时间有多久.

此面板只读. 点击任何内容都不会改变
网络, 仅用于查明各部分在哪里,
以及哪里出了问题.

## <a name="when-to-reach-for-it" /> 适用场景

- 合成失败, 想查看错误, 但不想走到
  <ItemLink id="crafting_core" />旁.
- 接手大型复杂网络, 需要查看全貌.
- 想了解某配方为何不能自动合成,
  可合成列表会显示网络实际掌握的配方.
- 脚本似乎卡住时, 可在终端面板查看运行状态
  和已注册处理器, 无需逐个打开终端.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="diagnostic_tool" />
