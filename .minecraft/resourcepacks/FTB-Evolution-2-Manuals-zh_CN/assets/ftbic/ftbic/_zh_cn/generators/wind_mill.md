---
navigation:
  title: 风力发电机
  icon: ftbic:wind_mill
  parent: generators/index.md
  position: 4
item_ids:
  - ftbic:wind_mill
---

# <Color id="gold">风力发电机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="wind_mill" scale="2" />

  发电量取决于高度.在天气和遮挡修正前,配置输出从Y=64时的 **9.6 FE/t** 提升至Y=320时的 **104 FE/t** .
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="wind_mill" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">放置要求</Color>
</Column>

* 最低有效高度为 **Y=64** ,低于此高度时不发电.
* 输出从Y=64到 **Y=320** 线性增加.
* 周围5格范围内(下方2格至上方5格)每有一个非空气方块,有效高度就降低一格,因此应保持周围空旷.
* **下雨** 时输出乘以1.2.
* **雷暴** 时输出乘以1.5.

<ItemImage id="minecraft:air" scale="0.25"/>
***

适合作为被动补充电源,也让高空建筑更有价值.在高处分散放置多台风力发电机,不要堆叠,因为它们彼此也会被视为障碍物.
