---
navigation:
  parent: items-blocks/index.md
  icon: craft_requester
  title: 合成请求器
categories:
  - device
description: starts an autocrafting job given a redstone signal
item_ids:
- nodeworks:craft_requester
---

# <a name="craft-requester" /> 合成请求器

合成请求器收到红石信号时会发起自动合成任务.
可配置要合成的物品和每批数量.

<GameScene interactive={true} zoom="5" paddingLeft="40" paddingRight="40">
  <ImportStructure src="../assets/assemblies/craft_requester_door.snbt" />
  <DiamondAnnotation pos="3.5 0.5 1.5">
    <ItemImage id="minecraft:oak_planks" />
  </DiamondAnnotation>
  <DiamondAnnotation pos="0.5 0.5 0.5">
    <RecipeFor id="minecraft:oak_door" />
  </DiamondAnnotation>
  <BoxAnnotation min="1.2 1 0.3" max="1.8 1.2 0.7" color="#00f2ff">
    红石信号激活合成请求器, 合成其配置的物品.
  </BoxAnnotation>
</GameScene>

## <a name="using-the-craft-requester" /> 使用合成请求器

手持物品右击, 设置要合成的物品. 再空手右击
打开界面, 选择每批数量和[输出频道](./craft_requester.md#channel).

保持红石信号时会持续排队合成, 每次处理一批.
信号停止后也会停止请求.

可用按钮触发单次合成, 或配合<ItemLink id="storage_meter" />
自动补货. 库存降低或恢复时, 监测器会自行
切换红石信号.

界面底部的状态标签显示当前工作状态, 悬停可查看
详细信息.

## <a name="Channel" /> <a name="channel" /> 频道

合成请求器界面中的频道选择器决定合成产物的去向.

> **注意:** 更多信息见[选择频道](../lua-api/channel.md#choosing-a-channel).

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="craft_requester" />
