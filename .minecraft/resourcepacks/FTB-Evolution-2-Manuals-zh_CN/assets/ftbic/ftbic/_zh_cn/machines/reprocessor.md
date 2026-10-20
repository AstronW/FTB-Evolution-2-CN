---
navigation:
  title: 回收机
  icon: ftbic:reprocessor
  parent: machines/index.md
  position: 9
item_ids:
  - ftbic:reprocessor
  - ftbic:scrap
  - ftbic:scrap_box
---

# <Color id="gold">回收机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="reprocessor" scale="2" />

  将 **各种废弃物品** 转化为<ItemLink id="scrap" />.废料是优质的基础发电机燃料,也可进一步制成<ItemLink id="scrap_box" />,开启后随机获得稀有材料.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="reprocessor" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

* 输入:圆石,泥土,腐肉,木棍等带有可回收标签的物品.
* 输出:每次加工约有12.5%概率产生废料(可配置).
* **参数:** MV级,缓存128,000 FE,耗能64 FE/t.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="scrap_box" />
  ### <Color id="aqua">废料盒</Color>
</Row>

将9个废料压缩为废料盒.右击开启后随机掉落物品,从煤炭到钻石装备都有可能.

<RecipeFor id="scrap_box" />
