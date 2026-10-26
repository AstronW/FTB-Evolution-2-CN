---
navigation:
  parent: nodeworks-mechanics/index.md
  icon: minecraft:hopper
  title: 移动物品
categories:
  - example
---

# <a name="moving-items" /> 移动物品

Nodeworks网络最简单的任务, 是将容器中的物品取入
网络存储中. 本页先介绍基础用法, 再介绍几种变体,
带过滤器的相同布局.

---

## <a name="with-import/export-chests" /> <a name="with-importexport-chests" /> 使用输入箱与输出箱

### <a name="inserting-items-into-your-network" /> 向网络输入物品

放入<ItemLink id="import_chest"/>的物品都会进入[网络存储](../nodeworks-mechanics/network-storage.md).

<GameScene zoom="5" interactive={true}>
  <ImportStructure src="../assets/assemblies/moving_items_import_chest.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="1 0.1 0.1" max="1.25 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BlockAnnotation x="2">
    放入输入箱的物品
    会自动进入网络.
  </BlockAnnotation>
</GameScene>

### <a name="extracting-items-from-your-network" /> 从网络取出物品

<ItemLink id="export_chest"/>可从网络存储抽取物品到自身物品栏.

<GameScene zoom="5" interactive={true}>
  <ImportStructure src="../assets/assemblies/moving_items_export_chest.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="1 0.1 0.1" max="1.25 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BlockAnnotation x="2">
    放入输入箱的物品
    会自动进入网络.
  </BlockAnnotation>
</GameScene>

### <a name="moving-items-between-two-blocks" /> 在两个方块之间移动物品

如需专门在两个不同方块之间移动物品, 可组合使用<ItemLink id="export_chest"/>和<ItemLink id="node"/>, 并在节点内装入<ItemLink id="storage_card"/>.

<GameScene zoom="5" interactive={true}>
  <ImportStructure src="../assets/assemblies/moving_items_export_push.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="1 0.1 0.1" max="1.25 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BlockAnnotation x="2">
    输出箱将物品推入潜影盒
    ![](../assets/images/export_chest_push_left.png)
  </BlockAnnotation>
</GameScene>

### <a name="moving-items-from-network-to-network" /> 在网络之间移动物品

如需将多个箱子的物品送入另一个包含多个箱子的网络, 可组合使用输入箱和输出箱. 将输出箱设为把物品推入输入箱即可.

<GameScene zoom="3" interactive={true} paddingTop="20" paddingBottom="20">
  <ImportStructure src="../assets/assemblies/moving_items_net_to_net.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="2 0.1 0.1" max="2.25 1.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="6 0.1 0.1" max="5.75 1.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BlockAnnotation x="3">
    输出箱将物品推入输入箱
    ![](../assets/images/export_chest_push_left.png)
  </BlockAnnotation>
</GameScene>


---

## <a name="with-a-scripting-terminal" /> 使用脚本终端

### <a name="pull-all-items" /> 拉取全部物品

将潜影盒中的所有物品取入网络存储, 不作过滤.

<GameScene zoom="5" interactive={true}>
  <ImportStructure src="../assets/assemblies/moving_items.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="1 0.1 0.1" max="1.25 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="4.75 0.1 0.1" max="5 0.9 0.9" color="#83E086">
    重命名为 **"shulkerBox"** <ItemImage id="nodeworks:io_card" />
  </BoxAnnotation>
</GameScene>

脚本如下:

<LuaCode>
```lua
importer
    :from(shulkerBox)
    :to(network)
    :start()
```
</LuaCode>

> **注意:** 如需反向运输, 将`:from(shulkerBox)`改为`:from(network)`, 并使用`:to(shulkerBox)`.

此脚本运行后, 所有进入潜影盒的物品都会存入
网络存储, 即未被过滤器排除的存储卡中.

## <a name="filtering-route-by-item-kind" /> <a name="filtering:-route-by-item-kind" /> 过滤: 按物品种类路由

使用同一网络, 但将原木送入一张存储卡, 圆石送入另一张,
其他物品进入默认存储.

<GameScene zoom="5" interactive={true}>
  <ImportStructure src="../assets/assemblies/item_filtering.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="2 0.1 1.1" max="2.25 0.9 1.9" color="#AA83E0">
    **规则** : `#c:cobblestones`
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="2 1.1 1.1" max="2.25 1.9 1.9" color="#AA83E0">
    **规则** : `#c:logs`
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="2 2.1 1.1" max="2.25 2.9 1.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />
  </BoxAnnotation>
  <BoxAnnotation min="5.75 0.1 1.1" max="6 0.9 1.9" color="#83E086">
    重命名为 **"shulkerBox"** <ItemImage id="nodeworks:io_card" />
  </BoxAnnotation>
</GameScene>

复用之前的代码, 但各存储卡采用不同的[过滤设置](../items-blocks/storage_card.md#filters).
