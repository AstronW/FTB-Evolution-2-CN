---
navigation:
  title: 地热发电机
  icon: ftbic:geothermal_generator
  parent: generators/index.md
  position: 2
item_ids:
  - ftbic:geothermal_generator
---

# <Color id="gold">地热发电机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="geothermal_generator" scale="2" />

  消耗内部8,000 mB储罐中的 **熔岩** ,产生 **320 FE/t** ,与本整合包的基础发电机相同.只要能从下界或附近熔岩湖持续抽取熔岩,就能稳定供电.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="geothermal_generator" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">补充熔岩</Color>
</Column>

* 手持熔岩桶右击方块,可灌入1,000 mB.
* 也可用<ItemLink id="pump" />或任意能输送流体的管道输入熔岩.
* 发电时每刻燃烧1 mB熔岩,因此一桶可持续50秒.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">参数</Color>
</Column>

* **等级:** LV
* **内部能量缓存:** 76,800 FE
* **储罐:** 8,000 mB
* **输出:** 320 FE/t
