---
navigation:
  title: 弹出升级
  icon: ftbic:ejector_upgrade
  parent: upgrades/index.md
  position: 4
item_ids:
  - ftbic:ejector_upgrade
---

# <Color id="gold">弹出升级</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="ejector_upgrade" scale="2" />

  通过允许物品输出的面,将机器输出槽中的成品自动推入相邻物品栏.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="ejector_upgrade" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

* 用[侧面配置](../machines/side_configuration.md)选择输出面.仅输入或禁用物品传输的面不会弹出物品.
* 与<ItemLink id="powered_crafting_table" />配合,可不依赖连续漏斗搭建自动化生产线.
* 一个弹出升级就足够,安装多个不会加快输出.
