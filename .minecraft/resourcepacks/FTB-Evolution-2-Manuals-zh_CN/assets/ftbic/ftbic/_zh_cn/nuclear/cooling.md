---
navigation:
  title: 冷却元件
  icon: ftbic:heat_vent
  parent: nuclear/index.md
  position: 3
item_ids:
  - ftbic:small_coolant_cell
  - ftbic:medium_coolant_cell
  - ftbic:large_coolant_cell
  - ftbic:heat_vent
  - ftbic:reactor_heat_vent
  - ftbic:overclocked_heat_vent
  - ftbic:component_heat_vent
  - ftbic:advanced_heat_vent
  - ftbic:heat_exchanger
  - ftbic:reactor_heat_exchanger
  - ftbic:component_heat_exchanger
  - ftbic:advanced_heat_exchanger
---

# <Color id="gold">冷却元件</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="heat_vent" scale="2" />

  冷却元件分两类: **冷却单元** 将热量吸收到内部缓存,直至饱和; **散热片/热交换器** 则持续将热量从燃料棒传向散热片,再散入空气.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">冷却单元</Color>
</Column>

将热量存入有限缓存.饱和后停止吸热.仅依靠冷却单元的设计属于 **脉冲式** 设计,必须安排停机冷却.

<Row>
  <ItemImage id="small_coolant_cell" />
  ### <Color id="aqua">小型冷却单元</Color>
</Row>

<RecipeFor id="small_coolant_cell" />

<Row>
  <ItemImage id="medium_coolant_cell" />
  ### <Color id="aqua">中型冷却单元</Color>
</Row>

<RecipeFor id="medium_coolant_cell" />

<Row>
  <ItemImage id="large_coolant_cell" />
  ### <Color id="aqua">大型冷却单元</Color>
</Row>

<RecipeFor id="large_coolant_cell" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">散热片</Color>
</Column>

散热片从反应堆外壳或相邻元件散热,是 **持续运行** 设计的必需部件.

<Row>
  <ItemImage id="heat_vent" />
  ### <Color id="aqua">散热片</Color>
</Row>

基础散热元件,从反应堆外壳吸热并散入空气.

<RecipeFor id="heat_vent" />

<Row>
  <ItemImage id="reactor_heat_vent" />
  ### <Color id="aqua">反应堆散热片</Color>
</Row>

更强的外壳散热元件,每刻可从反应堆本体吸收更多热量.

<RecipeFor id="reactor_heat_vent" />

<Row>
  <ItemImage id="component_heat_vent" />
  ### <Color id="aqua">元件散热片</Color>
</Row>

从相邻 **元件** (冷却单元)而非外壳吸热,是循环利用冷却单元设计的核心.

<RecipeFor id="component_heat_vent" />

<Row>
  <ItemImage id="overclocked_heat_vent" />
  ### <Color id="aqua">超频散热片</Color>
</Row>

混合型散热元件,可与外壳和相邻元件交换热量.高负载时会损坏自身,但合理布置后效果很强.

<RecipeFor id="overclocked_heat_vent" />

<Row>
  <ItemImage id="advanced_heat_vent" />
  ### <Color id="aqua">高级散热片</Color>
</Row>

终局散热片,用于IV级设计.

<RecipeFor id="advanced_heat_vent" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">热交换器</Color>
</Column>

热交换器用于 **均衡** 热量:将热量从较热元件移至较冷元件,或从反应堆外壳移入元件.没有热交换器,热量会集中在燃料棒周围.

<Row>
  <ItemImage id="heat_exchanger" />
  ### <Color id="aqua">热交换器</Color>
</Row>

<RecipeFor id="heat_exchanger" />

<Row>
  <ItemImage id="reactor_heat_exchanger" />
  ### <Color id="aqua">反应堆热交换器</Color>
</Row>

专门与反应堆外壳交换热量,将外壳热量引入元件网格,再由散热片散出.

<RecipeFor id="reactor_heat_exchanger" />

<Row>
  <ItemImage id="component_heat_exchanger" />
  ### <Color id="aqua">组合热交换器</Color>
</Row>

只平衡相邻元件之间的热量,成本低廉.

<RecipeFor id="component_heat_exchanger" />

<Row>
  <ItemImage id="advanced_heat_exchanger" />
  ### <Color id="aqua">高级热交换器</Color>
</Row>

终局热交换器.

<RecipeFor id="advanced_heat_exchanger" />
