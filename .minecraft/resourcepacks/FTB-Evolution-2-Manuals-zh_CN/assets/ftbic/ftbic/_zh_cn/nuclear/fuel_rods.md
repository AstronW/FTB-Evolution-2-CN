---
navigation:
  title: 燃料棒
  icon: ftbic:uranium_fuel_rod
  parent: nuclear/index.md
  position: 2
item_ids:
  - ftbic:uranium_fuel_rod
  - ftbic:dual_uranium_fuel_rod
  - ftbic:quad_uranium_fuel_rod
---

# <Color id="gold">燃料棒</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="quad_uranium_fuel_rod" scale="2" />

  燃料棒同时产生 **热量** 和 **电力** .双联,四联燃料棒会大幅增加二者,也需要强得多的冷却能力.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="uranium_fuel_rod" />
  ### <Color id="aqua">铀燃料棒</Color>
</Row>

在<ItemLink id="canning_machine" />中由贫铀制得.基础单位:1倍输出,1倍热量.

<RecipeFor id="uranium_fuel_rod" />

<Row>
  <ItemImage id="dual_uranium_fuel_rod" />
  ### <Color id="aqua">双联铀燃料棒</Color>
</Row>

将两根燃料棒组合而成.4倍输出,2倍热量,单位燃料更高效,但冷却负荷也翻倍.

<RecipeFor id="dual_uranium_fuel_rod" />

<Row>
  <ItemImage id="quad_uranium_fuel_rod" />
  ### <Color id="aqua">四联铀燃料棒</Color>
</Row>

高功率设计的核心.10倍输出,4倍热量,需精心布置并配合强力冷却.

<RecipeFor id="quad_uranium_fuel_rod" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">放置规则</Color>
</Column>

燃料棒根据每个 **有效相邻元件** (燃料棒,反射板或散热元件)产生热量和电力.空槽不计入.设计时可遵循:

* 一根普通燃料棒搭配4块反射板,输出与一根四联燃料棒搭配2块反射板相当,可从这里起步.
* 只有冷却能力足够后,再升级到双联或四联燃料棒.
