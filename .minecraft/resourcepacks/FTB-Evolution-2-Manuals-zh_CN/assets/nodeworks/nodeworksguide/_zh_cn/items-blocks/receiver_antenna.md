---
navigation:
  parent: items-blocks/index.md
  icon: receiver_antenna
  title: 接收天线
categories:
  - infrastructure
description: connects to broadcasted processing storages and export chests
item_ids:
- nodeworks:receiver_antenna
---

# <a name="receiver-antenna" /> 接收天线

用于将一个网络连接到另一个[子网](../nodeworks-mechanics/subnets.md).
适合将[加工配方集](./recipe_sets.md#processing-set)分散到不同
网络中, 并用于[自动合成](../nodeworks-mechanics/autocrafting.md).

<GameScene zoom="4" paddingTop="30" paddingLeft="60" paddingRight="60">
  <IsometricCamera yaw="180" roll="0" pitch="0" />
  <ImportStructure src="../assets/assemblies/receiving_antenna_uses.snbt" />
  <BoxAnnotation min="2 0 0" max="3 1 1">
    从另一网络接收加工配方集.
  </BoxAnnotation>
  <BoxAnnotation min="0 0 0" max="1 2 1">
    接收广播输出箱中的物品.
  </BoxAnnotation>
</GameScene>

## <a name="wireless-item-intake" /> 无线物品输入

将接收天线放在<ItemLink id="import_chest" />顶部,
与另一网络中放在以下方块上的<ItemLink id="broadcast_antenna" />
配对: <ItemLink id="export_chest" />. 输入广播端
输出箱的物品会落入此输入箱, 从而在两个网络之间
建立无线运输通道.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="receiver_antenna" />
