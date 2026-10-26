---
navigation:
  parent: items-blocks/index.md
  icon: portable_inventory_terminal
  title: 便携式物品终端
categories:
  - tool
  - requires_controller
description: a portable viewport into any linked network's storage
item_ids:
- nodeworks:portable_inventory_terminal
---

# <a name="portable-inventory-terminal" /> 便携式物品终端

随身携带的终端.

<ItemLink id="inventory_terminal" />的手持版本. 通过
使用<ItemLink id="link_crystal" />与<ItemLink id="broadcast_antenna" />配对以无线连接,
天线需放在<ItemLink id="network_controller" />顶部.

<ItemImage scale="6" id="portable_inventory_terminal" />

## <a name="linking-it-to-a-network" /> 连接网络

便携式物品终端通过三个组件访问网络,
请先准备好:

<GameScene zoom="3" interactive={true} paddingTop="20">
  <ImportStructure src="../assets/assemblies/broadcast_antenna_network_controller.snbt" />
</GameScene>

- 目标网络中的<ItemLink id="network_controller" />
- 放在该控制器顶部的<ItemLink id="broadcast_antenna" />
- 与该天线配对的<ItemLink id="link_crystal" /> *(不要与加工配方存储器上的天线配对)*

<br clear="all" /><br clear="all" /><br clear="all" /><br clear="all" />
<FloatingImage src="../assets/images/portable_inventory_terminal_link_slot.png" align="left" />

将配对后的链接水晶放入便携式物品终端右上角的槽位.

连接建立后, 便携终端物品的纹理会亮起,
颜色与网络相同.

<br clear="all" />

## <a name="Range" /> <a name="range" /> 范围

广播范围的更多信息见<ItemLink id="broadcast_antenna" />页面.

## <a name="using-the-terminal" /> 使用终端

界面中的所有功能均与<ItemLink id="inventory_terminal" />相同.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="portable_inventory_terminal" />
