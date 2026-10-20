---
navigation:
  title: 线缆
  icon: ftbic:mv_cable
  parent: energy/index.md
  position: 1
item_ids:
  - ftbic:lv_cable
  - ftbic:mv_cable
  - ftbic:hv_cable
  - ftbic:ev_cable
  - ftbic:iv_cable
  - ftbic:burnt_cable
  - ftbic:lv_reinforced_cable
  - ftbic:mv_reinforced_cable
  - ftbic:hv_reinforced_cable
  - ftbic:ev_reinforced_cable
  - ftbic:iv_reinforced_cable
  - ftbic:burnt_reinforced_cable
---

# <Color id="gold">线缆</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="hv_cable" scale="2" />

  线缆将发电机,用电设备和电池连成一个电网.能量沿连续线缆瞬间传输,最远可达配置中的 **最大线缆长度** (默认300).
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="lv_cable" />
  ### <Color id="aqua">铜质线缆(LV) - 1,024 FE/t</Color>
</Row>

橡胶包覆的铜线.基础发电机,打粉机和电炉的常用线缆.

<RecipeFor id="lv_cable" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="mv_cable" />
  ### <Color id="aqua">铝质线缆(MV) - 4,096 FE/t</Color>
</Row>

绝缘金线,用于MV变压器与中等级机器之间.

<RecipeFor id="mv_cable" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="hv_cable" />
  ### <Color id="aqua">金质线缆(HV) - 16,384 FE/t</Color>
</Row>

绝缘铁线,用于高级机器以及核反应堆的初段输出.

<RecipeFor id="hv_cable" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="ev_cable" />
  ### <Color id="aqua">末影线缆(EV) - 65,536 FE/t</Color>
</Row>

绝缘铱线,用于传送机,反物质构建机和量子装备充电座.

<RecipeFor id="ev_cable" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="iv_cable" />
  ### <Color id="aqua">玻璃线缆(IV) - 262,144 FE/t</Color>
</Row>

模组中传输速率最高的线缆,适合满功率反应堆和终局反物质生产线.

<RecipeFor id="iv_cable" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="burnt_cable" />
  ### <Color id="aqua">烧坏的线缆</Color>
</Row>

线缆输入电压过高时会变成这个方块.将其拆除,换成正确等级的线缆,再把烧坏的残骸打成<ItemLink id="scrap" />.

<RecipeFor id="scrap" fallbackText="Drop a Burnt Cable in any crafting grid for scrap." />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">强化线缆</Color>

  <ItemImage id="lv_reinforced_cable" scale="2" />

  完整立方体,拥有<ItemLink id="reinforced_stone" />的坚固程度,同时仍按对应等级的速率传输电力.可用它 **穿过** 反应堆防护墙布线而不留下缺口.各等级颜色与对应普通线缆一致.
</Column>

强化线缆可与同等级普通线缆连接,穿墙转换时无需变压器.强化线缆过载后会变成<ItemLink id="burnt_reinforced_cable" />--核心烧焦,无法导电的防爆石方块,而不是脆弱的普通烧坏线缆,因此仍能保持防护墙完整.

<Row>
  <ItemImage id="lv_reinforced_cable" />
  ### <Color id="aqua">强化铜质线缆(LV) - 1,024 FE/t</Color>
</Row>

<RecipeFor id="lv_reinforced_cable" />

<Row>
  <ItemImage id="mv_reinforced_cable" />
  ### <Color id="aqua">强化铝质线缆(MV) - 4,096 FE/t</Color>
</Row>

<RecipeFor id="mv_reinforced_cable" />

<Row>
  <ItemImage id="hv_reinforced_cable" />
  ### <Color id="aqua">强化金质线缆(HV) - 16,384 FE/t</Color>
</Row>

<RecipeFor id="hv_reinforced_cable" />

<Row>
  <ItemImage id="ev_reinforced_cable" />
  ### <Color id="aqua">强化末影线缆(EV) - 65,536 FE/t</Color>
</Row>

<RecipeFor id="ev_reinforced_cable" />

<Row>
  <ItemImage id="iv_reinforced_cable" />
  ### <Color id="aqua">强化玻璃线缆(IV) - 262,144 FE/t</Color>
</Row>

<RecipeFor id="iv_reinforced_cable" />

<Row>
  <ItemImage id="burnt_reinforced_cable" />
  ### <Color id="aqua">烧坏的强化线缆</Color>
</Row>

强化线缆过载后的形态.仍免疫凋灵和末影龙破坏,能继续充当防护方块,但不再传导能量.请换成正确等级的新强化线缆.
