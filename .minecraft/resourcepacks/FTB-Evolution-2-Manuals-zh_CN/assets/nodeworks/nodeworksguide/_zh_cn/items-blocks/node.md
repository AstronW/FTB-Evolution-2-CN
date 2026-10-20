---
navigation:
  parent: items-blocks/index.md
  icon: node
  title: 节点
categories:
  - infrastructure
description: card host on a pipe network
item_ids:
- nodeworks:node
- nodeworks:focus_node
---

# <a name="Node" /> <a name="node" /> 节点

节点用于容纳[卡片](../nodeworks-mechanics/cards.md), 而
网络连通性由[管道](pipe.md)负责. 当你需要用卡片
与相邻方块交互时, 就在该处的管道线路中
放入节点.

<BlockImage scale="6" id="node" />

## <a name="Faces" /> <a name="faces" /> 侧面

各个面会根据相邻方块调整功能. 接触其他
网络方块的面会成为管道连接面, 禁用卡片槽;
接触普通方块的面则可安装卡片, 操作那个相邻方块.

## <a name="opening-the-gui" /> 打开界面

右击非管道面可打开该面的卡片网格. Shift右击
会打开 *相反* 一面, 适合目标面被遮挡时使用. 管道
面无法打开, 在侧面选择器中的标签会变暗.

![](../assets/images/node_gui.png)

## <a name="Cards" /> <a name="cards" /> 卡片

向设备面的9个槽位之一放入卡片, 即可为该面
添加对应功能:

- <ItemImage scale="0.5" id="io_card" /> <ItemLink id="io_card" />: 允许网络
  向相邻方块输入或从中取出物品.
- <ItemImage scale="0.5" id="storage_card" /> <ItemLink id="storage_card" />:
  将相邻方块的物品栏纳入网络存储.
- <ItemImage scale="0.5" id="redstone_card" /> <ItemLink id="redstone_card" />:
  读取并输出该面的红石信号.
- <ItemImage scale="0.5" id="observer_card" /> <ItemLink id="observer_card" />:
  读取所朝向方块的状态.

同一面上的多张卡片可共同工作. 同时安装IO卡和
红石卡后, 该面既能移动物品, 又能
输出红石信号.

## <a name="focus-node" /> 聚焦节点

<GameScene interactive={true} zoom="5">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="../assets/assemblies/focus_node.snbt" />
</GameScene>

<ItemLink id="focus_node" />是用于远距离连接的节点变种.
用以下工具配对两个聚焦节点:
<ItemLink id="network_wrench" />. 即使两者之间没有连续管道, 网络
也会将它们视为相连, 适合跨越空隙, 或连接
相隔较远的机器组,
无需全程铺设管道.

聚焦节点的六个面仍按普通节点工作:
具有相同的管道/设备/空闲角色, 相同卡片槽, 也会
自动连接相邻管道. 扳手建立的远程连接会额外加入
这些本地连接.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="node" />

<RecipeFor id="focus_node" />
