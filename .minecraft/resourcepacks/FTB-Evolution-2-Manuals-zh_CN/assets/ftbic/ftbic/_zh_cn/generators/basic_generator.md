---
navigation:
  title: 基础发电机
  icon: ftbic:basic_generator
  parent: generators/index.md
  position: 1
item_ids:
  - ftbic:basic_generator
---

# <Color id="gold">基础发电机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="basic_generator" scale="2" />

  你的第一种电源:燃烧固体燃料的小型发电机,输出为 **320 FE/t** .
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="basic_generator" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">参数</Color>
</Column>

* **等级:** LV(输出320 FE/t)
* **内部能量缓存:** 128,000 FE
* **燃料槽:** 可容纳一组物品

将燃料放入唯一的物品槽.发电机会持续燃烧直至燃料耗尽,缓存充满时也 **不会** 停止,因此应直接连接<ItemLink id="lv_battery_box" />以免浪费.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">可用燃料</Color>
</Column>

只有下列燃料可以燃烧.熔岩桶,烈焰棒等其他熔炉燃料在这里无效.燃料槽也能放入其他物品,但它们只会堵住槽位,因此自动供料时应配置过滤.

* 煤炭与木炭:1,600游戏刻
* 煤炭块:16,000游戏刻
* 原木与木板:300游戏刻
* 树苗,木棍和甘蔗:100游戏刻
* 仙人掌:200游戏刻
* <ItemLink id="scrap" />:400游戏刻,成本低廉且燃烧性能不错

<RecipesFor id="scrap" />
