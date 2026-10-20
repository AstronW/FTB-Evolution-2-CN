---
navigation:
  parent: items-blocks/index.md
  icon: network_wrench
  title: 网络扳手
description: toggles pipe connections and links Focus Nodes
item_ids:
- nodeworks:network_wrench
---

# <a name="network-wrench" /> 网络扳手

网络扳手可在不拆除方块的情况下调整网络结构.
它能分别切换各个方块之间的管道连接,
也能远距离连接<ItemLink id="focus_node" />.

<ItemImage scale="6" id="network_wrench" />

## <a name="toggling-pipe-connections" /> 切换管道连接

在两个网络方块相接的面上Shift右击,
即可切换两者间的管道连接. 方块保持原位,
但网络会将该面视为没有管道.

这是扳手最常见的用途, 例如:
以下几种情况:

- 让<ItemLink id="node" />紧邻<ItemLink id="pipe" />,
  但不将两者合并为同一网络分支
- 关闭一个管道连接面, 将一个网络拆成两个
- 阻止<ItemLink id="terminal" />或其他设备
  意外连接到旁边的另一个网络

在同一面重复操作可恢复连接.

## <a name="linking-focus-nodes" /> 连接聚焦节点

<ItemLink id="focus_node" />是特殊情况, 两个聚焦节点
可用扳手进行远距离连接:

1. 在聚焦节点未接触其他网络方块的面上Shift右击,
   将其选为待连接的源节点. 方块会显示
   选中边框.
2. 右击另一个聚焦节点, 切换两者间的连接.

成功连接后仍会保留源节点选择, 因此可以连续
连接多个目标, 无需反复选择源节点.

### <a name="Rules" /> <a name="rules" /> 规则

- 两个聚焦节点必须与所选源节点处于 **同一维度** .
- 两者必须属于 **同一个网络控制器** . 扳手不会
  桥接两个独立网络.

违反规则时, 扳手会通过聊天消息说明原因.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="network_wrench" />
