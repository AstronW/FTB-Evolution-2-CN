---
navigation:
  title: 装罐机
  icon: ftbic:canning_machine
  parent: machines/index.md
  position: 8
item_ids:
  - ftbic:canning_machine
  - ftbic:empty_can
  - ftbic:canned_food
---

# <Color id="gold">装罐机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="canning_machine" scale="2" />

  将食物装入<ItemLink id="canned_food" />以便储存,为喷漆罐填充染料,并组装<ItemLink id="uranium_fuel_rod" />.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="canning_machine" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="empty_can" />
  ### <Color id="aqua">空罐</Color>
</Row>

由锡板制成,是所有装罐配方的容器.

<RecipeFor id="empty_can" />

<Row>
  <ItemImage id="canned_food" />
  ### <Color id="aqua">罐头食品</Color>
</Row>

消耗任意食物和空罐.装罐后的食物堆叠上限更高,并保留原食物的全部营养.

<Row>
  <ItemImage id="light_spray_paint_can" />
  ### <Color id="aqua">喷漆罐</Color>
</Row>

将任意染料装入<ItemLink id="empty_can" />,即可制成<ItemLink id="light_spray_paint_can" />或<ItemLink id="dark_spray_paint_can" />.详见[喷漆](../utilities/spray_paint.md).

<ItemImage id="minecraft:air" scale="0.25"/>

**参数:** LV级,缓存38,400 FE,耗能8 FE/t.
