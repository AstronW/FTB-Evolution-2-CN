---
navigation:
  parent: items-blocks/index.md
  icon: multi_processing_handler
  title: 多配方加工处理器
categories:
  - autocrafting
  - requires_controller
description: one handler for many processing set recipes
item_ids:
- nodeworks:multi_processing_handler
---

# <a name="multi-processing-handler" /> 多配方加工处理器

一种能同时处理多个配方的<ItemLink id="processing_handler" />,
配方来自[加工配方集](./recipe_sets.md#processing-set). 将多个
矿石配方绑定到同一个处理器, 放在一组熔炉前,
[合成CPU](./crafting_cpu.md)就会把每次合成分配给它, 无需 Lua,
也无需为每种配方单独放置处理器.

> 需要<ItemLink id="network_controller" />才能使用

<GameScene zoom="3" interactive={true} paddingLeft="50" paddingRight="50" paddingTop="30">
  <IsometricCamera yaw="160" roll="0" pitch="10" />
  <ImportStructure src="../assets/assemblies/multi_processor_handler.snbt" />
  <BoxAnnotation min="0 2 0" max="1 2.25 1" color="#3C44AA">
    <ItemImage id="storage_card" /> 蓝色频道存储卡
  </BoxAnnotation>
  <BoxAnnotation min="0 0.75 0" max="1 1 1" color="#B02E26">
    <ItemImage id="storage_card" /> 红色频道存储卡
  </BoxAnnotation>
  <BlockAnnotation x="2" y="1">
    已配置多个烧炼配方.
  </BlockAnnotation>
</GameScene>

## <a name="two-sides" /> 两个侧面

形状与加工处理器相同: **背面** 接入
主网络, **正面** 作为独立微型网络的起点, 通过
管道, 节点和存储卡连接机器. 布局参见
[两个侧面](./processing_handler.md#two-sides).

## <a name="choosing-recipes" /> 选择配方

右击处理器打开界面. 主网络上的所有加工配方集
都会列出, 各带一个复选框. 勾选希望交给此处理器
的配方. 已勾选配方排在最前面, 搜索框可按配方名或物品名缩小列表范围.

角落的计数器显示已勾选数量和上限. 已由
脚本或其他处理器负责的配方会变灰, 达到
上限后, 其余配方也会全部变灰.

勾选的配方若从加工配方存储器中移除, 仍会留在
列表中并标为缺失, 以便取消勾选. 配方集恢复后,
该条目会重新生效.

## <a name="Channels" /> <a name="channels" /> 频道

所有配方共享一个输入频道和一个输出频道.
任意已勾选配方的原料都会送到微型网络中输入颜色的<ItemLink id="storage_card" />
所连接的容器, 成品则从
输出颜色的卡片处取出. 对一组熔炉而言, 就是在每台熔炉
顶面放一张蓝色卡片, 底面放一张红色卡片.

所有原料都经过同一个频道, 因此需要在卡片上
分类. 为每张存储卡设置[筛选器](./storage_card.md#filters), 只有
符合条件的物品才会进入对应方块: 每台熔炉侧面的卡片
允许`#c:coal`通过, 用于接收燃料; 顶面的卡片拒绝它, 用于接收
矿石, 两张卡片都使用蓝色频道.

![](../assets/images/in_out_channels.png)

## <a name="parallel-mode" /> 并行模式

默认情况下, 处理器一次只运行一次合成. 同一合成树中的两个配方会排队, 避免争用熔炉, 等待它的协处理器则会先处理其他工作.
如需更改此行为, 可按下 **并行** 开关, 让多次合成同时运行.

![](../assets/images/parallel_toggle.png)

## <a name="compared-to-the-processing-handler" /> 与加工处理器比较

使用<ItemLink id="processing_handler" />处理需要独占
机器或为每种原料设置独立频道的配方. 当许多配方
共用一组机器, 且路由方式相同时,
则使用多配方加工处理器.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="multi_processing_handler" />
