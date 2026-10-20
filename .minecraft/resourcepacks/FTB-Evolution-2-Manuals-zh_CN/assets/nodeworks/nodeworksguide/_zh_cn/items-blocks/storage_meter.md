---
navigation:
  parent: items-blocks/index.md
  icon: storage_meter
  title: 库存监测器
categories:
  - device
description: tracks the amount of items/fluids its configured to watch
item_ids:
- nodeworks:storage_meter
---

# <a name="storage-meter" /> 库存监测器

库存监测器监视网络中的指定物品, 当库存
低于阈值时输出红石信号. 它还可发起自动合成
任务补充库存.

<GameScene interactive={true} zoom="5" paddingLeft="40" paddingRight="40">
  <ImportStructure src="../assets/assemblies/stock_meter_door.snbt" />
  <DiamondAnnotation pos="3.5 0.5 1.5">
    <ItemImage id="minecraft:oak_planks" />
  </DiamondAnnotation>
  <DiamondAnnotation pos="0.5 0.5 0.5">
    <RecipeFor id="minecraft:oak_door" />
  </DiamondAnnotation>
  <BlockAnnotation x="1" color="#00f2ff">
    已开启自动合成, 会自动补充网络中的门库存.
  </BlockAnnotation>
</GameScene>

## <a name="using-storage-meters" /> 使用库存监测器

手持要监视的物品右击, 再空手右击
打开界面, 设置阈值和频道.

只要库存低于阈值, 就会输出红石信号.
开启自动合成时(默认开启), 还会发起合成任务
补足库存. 如果想用红石信号驱动
<ItemLink id="craft_requester" />, 可以关闭自动合成.

界面底部的状态标签显示当前工作状态, 悬停
可查看详情.

## <a name="subnet-example" /> 子网示例

<GameScene interactive={true} zoom="4" paddingLeft="40" paddingRight="40">
  <ImportStructure src="../assets/assemblies/storage_meter_subnet.snbt" />
  <BlockAnnotation y="2" x="2">
    将<ItemLink id="minecraft:raw_iron" />烧炼成<ItemLink id="minecraft:iron_ingot" />.
  </BlockAnnotation>
  <BlockAnnotation x="4" y="2" z="1">
    <ItemImage id="minecraft:raw_iron" />
  </BlockAnnotation>
  <RemoveBlocks id="minecraft:sandstone" />
  <RemoveBlocks id="minecraft:sandstone" />
</GameScene>

此例中, <Color id="green">子网</Color>的库存监测器监视箱子里的铁锭. 库存不足时会向<Color id="blue">另一个网络</Color>的<ItemLink id="craft_requester" />发送红石信号, 由后者发起使用<ItemLink id="processing_handler" />的自动合成任务.

## <a name="Channel" /> <a name="channel" /> 频道

库存监测器界面中的频道选择器, 同时决定合成产物去向和所监视网络存储的频道.

> **注意:** 更多信息见[选择频道](../lua-api/channel.md#choosing-a-channel).

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="storage_meter" />
