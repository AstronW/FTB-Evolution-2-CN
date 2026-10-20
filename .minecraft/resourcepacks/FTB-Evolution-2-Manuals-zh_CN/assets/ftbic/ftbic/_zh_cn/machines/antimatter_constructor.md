---
navigation:
  title: 反物质构建机
  icon: ftbic:antimatter_constructor
  parent: machines/index.md
  position: 13
item_ids:
  - ftbic:antimatter_constructor
  - ftbic:antimatter
  - ftbic:antimatter_crystal
---

# <Color id="gold">反物质构建机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="antimatter_constructor" scale="2" />

  终局机器.制造<ItemLink id="antimatter" />和<ItemLink id="antimatter_crystal" />,它们用于制作<ItemLink id="quantum_helmet" /><ZapMode>及<ItemLink id="iv_rectifier" />系列设备</ZapMode>.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="antimatter_constructor" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">运行方法</Color>
</Column>

* **等级:** IV
* **缓存:** <Energy config="machines.antimatter_constructor_capacity" />
* 缓慢地将输入能量积累为反物质原料,需要持续的IV级供电.建议使用核反应堆或大规模<ItemLink id="ev_solar_panel" />阵列.
* 接受可暂时成倍提高产出的"增幅"物品(见`antimatter_boost`配方).

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="antimatter_crystal" />
  ### <Color id="aqua">反物质晶体</Color>
</Row>

压缩后的反物质晶体,直接用于后期配方.

<RecipeFor id="antimatter_crystal" />
