---
navigation:
  title: 碳纤维护甲
  icon: ftbic:carbon_chestplate
  parent: armor/index.md
  position: 1
item_ids:
  - ftbic:carbon_helmet
  - ftbic:carbon_chestplate
  - ftbic:carbon_leggings
  - ftbic:carbon_boots
---

# <Color id="gold">碳纤维护甲</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="carbon_chestplate" scale="2" />

  入门级动力护甲.每吸收一点伤害消耗<Energy config="equipment.armor_damage_energy" />,而不是损失耐久.胸甲容量为 **<Energy config="equipment.carbon_armor_capacity" />** .
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="carbon_helmet" />
  ### <Color id="aqua">碳纤维头盔</Color>
</Row>

<RecipeFor id="carbon_helmet" />

<Row>
  <ItemImage id="carbon_chestplate" />
  ### <Color id="aqua">碳纤维胸甲</Color>
</Row>

储存整套护甲所需的能量.

<RecipeFor id="carbon_chestplate" />

<Row>
  <ItemImage id="carbon_leggings" />
  ### <Color id="aqua">碳纤维护腿</Color>
</Row>

<RecipeFor id="carbon_leggings" />

<Row>
  <ItemImage id="carbon_boots" />
  ### <Color id="aqua">碳纤维靴子</Color>
</Row>

<RecipeFor id="carbon_boots" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

未穿戴有电的对应胸甲时,其余部件不提供保护.电量不足时,只能吸收剩余电量足以抵消的伤害.
