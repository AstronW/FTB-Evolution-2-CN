---
navigation:
  title: 量子护甲
  icon: ftbic:quantum_chestplate
  parent: armor/index.md
  position: 2
item_ids:
  - ftbic:quantum_helmet
  - ftbic:quantum_chestplate
  - ftbic:quantum_leggings
  - ftbic:quantum_boots
---

# <Color id="gold">量子护甲</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="quantum_chestplate" scale="2" />

  终局动力护甲.防护机制与碳纤维护甲相同,但储能达到 **<Energy config="equipment.quantum_armor_capacity" />** ,支持飞行,完整伤害吸收和EV级充电.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="quantum_helmet" />
  ### <Color id="aqua">量子头盔</Color>
</Row>

<RecipeFor id="quantum_helmet" />

<Row>
  <ItemImage id="quantum_chestplate" />
  ### <Color id="aqua">量子胸甲</Color>
</Row>

储存整套护甲的能量.有电时双击跳跃键可悬停和飞行,悬停耗能为<Energy config="equipment.armor_flight_energy" rate="true" />.胸甲还支持滑翔,滑翔时按住跳跃键加速,按住潜行键减速.

<RecipeFor id="quantum_chestplate" />

<Row>
  <ItemImage id="quantum_leggings" />
  ### <Color id="aqua">量子护腿</Color>
</Row>

<RecipeFor id="quantum_leggings" />

<Row>
  <ItemImage id="quantum_boots" />
  ### <Color id="aqua">量子靴子</Color>
</Row>

<RecipeFor id="quantum_boots" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">提示</Color>
</Column>

* 胸甲在悬停或滑翔时消耗<Energy config="equipment.armor_flight_energy" rate="true" />.滑翔中的加速和制动会额外耗能.
* 吸收伤害只消耗储存的能量.部件不会损失耐久,胸甲没电时不提供保护.
* 将<ItemLink id="charge_pad" />放在<ItemLink id="ev_battery_box" />上方,站上去即可快速为整套护甲充电.
