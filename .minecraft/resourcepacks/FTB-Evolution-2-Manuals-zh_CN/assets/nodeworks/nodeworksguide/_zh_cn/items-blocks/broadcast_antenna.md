---
navigation:
  parent: items-blocks/index.md
  icon: broadcast_antenna
  title: 广播天线
categories:
  - infrastructure
description: broadcasts access to Network Controllers, Processing Storage, and Export Chests
item_ids:
- nodeworks:broadcast_antenna
---

# <a name="broadcast-antenna" /> 广播天线

根据下方放置的方块, 天线具有以下用途:

- 放在<ItemLink id="network_controller" />上: 广播此网络的无线访问权限.
与天线配对的<ItemLink id="portable_inventory_terminal" />
可在覆盖范围内的任意位置读写网络.
- 放在<ItemLink id="processing_storage" />上: 广播该方块及所有相邻
<ItemLink id="processing_storage" />中保存的<ItemLink id="processing_set" />,
供其他网络进行[自动合成](../nodeworks-mechanics/autocrafting.md).
- 放在<ItemLink id="export_chest" />上: 将箱子广播为无线投递点.
另一网络上配对的<ItemLink id="receiver_antenna" />会将
输入该箱子的物品直接送入那个网络.

<GameScene zoom="4" paddingTop="30" paddingLeft="60" paddingRight="60">
  <IsometricCamera yaw="180" roll="0" pitch="0" />
  <ImportStructure src="../assets/assemblies/broadcast_antenna_uses.snbt" />
  <BoxAnnotation min="2 0 0" max="4 1 1">
    这两个加工配方存储器的内容都会被广播.
  </BoxAnnotation>
  <BoxAnnotation min="5 0 0" max="6 1 1">
    广播后可供便携式物品终端访问.
  </BoxAnnotation>
  <BoxAnnotation min="0 0 0" max="1 1 1">
    将物品送入配对的输入箱.
  </BoxAnnotation>
</GameScene>

## <a name="Pairing" /> <a name="pairing" /> 配对

1. 打开广播天线界面.
1. 将<ItemLink id="link_crystal" />放入顶部槽位.
1. 取出水晶, 配对即已完成.

## <a name="Range" /> <a name="range" /> 范围

广播天线默认覆盖128格. 可使用
<ItemLink id="dimension_range_upgrade" />或<ItemLink id="multi_dimension_range_upgrade" />扩展范围.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="broadcast_antenna" />
