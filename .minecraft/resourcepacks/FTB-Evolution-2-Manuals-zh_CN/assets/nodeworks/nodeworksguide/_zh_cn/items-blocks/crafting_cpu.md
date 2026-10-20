---
navigation:
  parent: items-blocks/index.md
  icon: crafting_core
  title: 合成CPU
categories:
  - autocrafting
description: the brain of the autocrafting system in a network
item_ids:
- nodeworks:crafting_core
- nodeworks:crafting_storage
- nodeworks:substrate
- nodeworks:stabilizer
- nodeworks:co_processor
---

# <a name="crafting-cpu" /> 合成CPU

合成CPU是自动合成系统的大脑, 从
[配方存储方块](./storage_blocks.md)读取配方(包括本网络及广播子网的加工配方集),
从网络拉取原料, 执行合成, 再送回产物.
CPU组装完成后如何实际 *使用*, 见[自动合成](../nodeworks-mechanics/autocrafting.md).

## <a name="forming-the-cpu" /> 组装CPU

每个CPU中心必须恰好有一个<ItemLink id="crafting_core" />.
但仅有核心还不够, 至少需要一个<ItemLink id="crafting_storage" />
紧贴核心作为缓存. 没有缓存, CPU就无处存放
合成期间的物品, 因而不会启动.

布局自由, 无需扳手, 也没有固定形状.
放下核心, 在任意面接上缓存, 再将核心连接到节点, 它就会亮起.

<GameScene zoom="5" interactive={true} paddingLeft="50" paddingRight="60">
  <ImportStructure src="../assets/assemblies/basic_crafting_cpu.snbt" />
  <BlockAnnotation x="1" y="0" z="0">
    会产生热量, 建议搭配2个冷却块.
  </BlockAnnotation>
</GameScene>

> **提示:** 入门合成CPU建议连接两个<ItemLink id="stabilizer" />
> 方块到<ItemLink id="crafting_storage" />旁, 确保 **效率**
> 至少达到100%.

## <a name="expanding-the-cpu" /> 扩展CPU

其他CPU方块可增大规模或提高速度:

- <ItemLink id="crafting_storage" /> ( **合成缓存** ): 至少需要
一个. 更多缓存意味着合成期间能够容纳更多原料和
中间产物. 每个产生 **2热量** .
- <ItemLink id="co_processor" /> ( **合成协处理器** ): 每个使
CPU多并行执行一项合成. 每个产生 **3热量** .
- <ItemLink id="stabilizer" /> ( **合成冷却块** ): 抵消热量. 单独
放置时提供 **1冷却** , 每相邻一个冷却块
再增加 **1** . 一个冷却块周围紧贴四个冷却块时,
会提供 **5冷却** , 因此冷却块成群放置比
分散放置更强.
- <ItemLink id="substrate" /> ( **合成基板** ): 用于加速.
缓存或协处理器的每个面只要接触基板,
便使CPU加速 **10%** , 最高为 **4倍(400%)速度** .
基板接触核心, 其他基板或冷却块的面不产生加速,
因此将基板夹在缓存与协处理器之间
效果最好.

这些方块只需接触核心, 或沿已属于CPU的方块
继续连接. 无需扳手和界面操作, 新方块会在
下一游戏刻自动加入.

### <a name="heat,-cooling,-and-speed" /> <a name="heat-cooling-and-speed" /> 热量, 冷却与速度

每个缓存和协处理器都是独立热源, 冷却块
负责吸收与自身实际接触的热源的热量.
布局与数量同样重要:

- 热源面贴面堆放时, 每个共享面额外增加 **1热量** ,
  叠加在各方块自身热量之上. 因此缓存与
  协处理器挤成方块堆时, 比分散放置热得多.
- 每个冷却块提供一个总冷却值(单独为1, 成群时更高).
  该值会**平均分配给它接触的全部
  热源**. 夹在两个缓存之间的冷却块,
  将冷却能力各分一半; 位于六个热源中央时,
  对每个热源的效果就很弱.
- 当CPU总冷却不足以抵消总热量时, 速度会按比例 **降低
  运行速度**, 最低至 **25%**. CPU不会
  只是变得很慢.
- 冷却块只能抵消热量, 不会使速度超过100%. 只有
  基板可以继续提速, 上限为4倍.

<GameScene zoom="5" interactive={false} paddingLeft="60" paddingRight="60">
  <IsometricCamera yaw="180" roll="0" pitch="0" />
  <ImportStructure src="../assets/assemblies/overheating_crafting_cpu.snbt" />

  <LineAnnotation from="2.5 0 0" to="4.5 3 0" color="#ff0000" thickness="0.05" />
  <LineAnnotation from="2.5 3 0" to="4.5 0 0" color="#ff0000" thickness="0.05" />

  <LineAnnotation from="1 0 0" to="2.5 1.25 0" color="#00ff00" thickness="0.05" />
  <LineAnnotation from="1.02 0 0" to="-0.8 3 0" color="#00ff00" thickness="0.05" />
</GameScene>

> **提示:** 方块过热时还会有视觉提示, 例如呈现
> 黄色, 橙色, 红色或冒烟.

实际搭建时, 不要只在一大堆缓存和
协处理器旁贴少量冷却块, 试图压住所有热量.
将冷却块搭成专门的墙或散热鳍片, 让冷却块互相接触,
再布置热源, 使每个冷却块只需处理一至两个
热源面. 最后在缓存和协处理器剩余的面上
加入基板以提高速度.

## <a name="Recipes" /> <a name="recipes" /> 配方

<Row>
    <RecipeFor id="nodeworks:crafting_core" />
    <RecipeFor id="nodeworks:crafting_storage" />
    <RecipeFor id="nodeworks:substrate" />
    <RecipeFor id="nodeworks:stabilizer" />
    <RecipeFor id="nodeworks:co_processor" />
</Row>
