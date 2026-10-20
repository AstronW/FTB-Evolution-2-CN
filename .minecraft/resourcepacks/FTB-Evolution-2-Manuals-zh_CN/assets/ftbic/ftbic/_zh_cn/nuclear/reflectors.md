---
navigation:
  title: 中子反射板
  icon: ftbic:thick_neutron_reflector
  parent: nuclear/index.md
  position: 5
item_ids:
  - ftbic:neutron_reflector
  - ftbic:thick_neutron_reflector
  - ftbic:iridium_neutron_reflector
---

# <Color id="gold">中子反射板</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="iridium_neutron_reflector" scale="2" />

  计算输出时,反射板视为 **有效的相邻燃料棒** :燃料棒旁放置反射板,作用如同那里还有另一根燃料棒.除铱反射板外,其余反射板的寿命均有限.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="neutron_reflector" />
  ### <Color id="aqua">中子反射板</Color>
</Row>

廉价的一次性部件,随使用逐渐耗尽.

<RecipeFor id="neutron_reflector" />

<Row>
  <ItemImage id="thick_neutron_reflector" />
  ### <Color id="aqua">加厚中子反射板</Color>
</Row>

寿命更长,中期设计的常用选择.

<RecipeFor id="thick_neutron_reflector" />

<Row>
  <ItemImage id="iridium_neutron_reflector" />
  ### <Color id="aqua">铱中子反射板</Color>
</Row>

寿命无限,成本较高,但适合所有永久运行的设计.

<RecipeFor id="iridium_neutron_reflector" />
