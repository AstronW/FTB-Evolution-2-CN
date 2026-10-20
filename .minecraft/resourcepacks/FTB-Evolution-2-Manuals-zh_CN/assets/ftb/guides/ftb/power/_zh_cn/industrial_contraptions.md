---
navigation:
  parent: index.md
  title: FTB工业奇械
  position: 20
  icon: ftbic:basic_generator
---
<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">FTB工业奇械</Color>

  <ItemImage id="ftbic:basic_generator" scale="2"/>

  FTB工业奇械直接使用FE.其发电机可向任意模组的线缆输出FE,机器也可从所有面接收FE,因此不再需要能量整流器.发电机,太阳能板,线缆和机器能量缓存的性能最高提升至默认值的四倍.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">发电机</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

| 发电机 | 输出 |
|---|:---:|
| <ItemImage id="ftbic:basic_generator"/> 基础发电机 | 320 FE/t (80) |
| <ItemImage id="ftbic:geothermal_generator"/> 地热发电机 | 320 FE/t (160) |
| <ItemImage id="ftbic:wind_mill"/> 风力发电机 | 9.6 至 104 FE/t (2.4 至 52) |
| <ItemImage id="ftbic:lv_solar_panel"/> 低压太阳能板 | 32 FE/t (8) |
| <ItemImage id="ftbic:mv_solar_panel"/> 中压太阳能板 | 256 FE/t (64) |
| <ItemImage id="ftbic:hv_solar_panel"/> 高压太阳能板 | 2,048 FE/t (512) |
| <ItemImage id="ftbic:ev_solar_panel"/> 超高压太阳能板 | 16,384 FE/t (4,096) |

风力发电机在y64以下仍不发电,在y320时达到最大输出;下雨和雷暴天气会提供加成.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="ftbic:nuclear_reactor"/>
  ### <Color id="aqua">核反应堆</Color>
</Row>

* 输出为默认值的 **四倍** .
* 水冷效果为默认值的 **五倍** (倍率10,原为2).
* 内部能量缓存容量翻倍.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">线缆与能量缓存</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

### <Color id="aqua">线缆</Color>

| 等级 | 传输速率 |
|---|:---:|
| LV | 1,024 FE/t (256) |
| MV | 4,096 FE/t (1,024) |
| HV | 16,384 FE/t (4,096) |
| EV | 65,536 FE/t (16,384) |
| IV | 262,144 FE/t (65,536) |

> <Color id="red">输入过高等级的电力仍会烧毁机器.</Color>

<ItemImage id="minecraft:air" scale="0.25"/>

### <Color id="aqua">机器能量缓存</Color>

所有机器的储能容量均为默认值的四倍,每次加工的耗能保持不变.电池和电池盒的容量没有改动.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">基础发电机燃料</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

基础发电机除原有燃料(煤炭,木炭,原木,木板,树苗,木棍,甘蔗,仙人掌和废料)外,还可使用:

| 燃料 | 燃烧时间 |
|---|:---:|
| 小撮煤炭与小撮木炭 | 200 游戏刻 |
| <ItemImage id="ftbmaterials:charcoal_block"/> 木炭块 | 16,000 游戏刻 |
| <ItemImage id="justdirethings:coal_t1"/> Just Dire Things煤炭 | 4,800 至 129,600 游戏刻 |
| Just Dire Things煤炭块 | 48,000 至 1,296,000 游戏刻 |
| <ItemImage id="mysticalagradditions:inferium_coal"/> 神秘农业扩展煤炭 | 2,400 至 76,800 游戏刻 |
| 神秘农业扩展煤炭块 | 21,600 至 691,200 游戏刻 |
| 邪恶工艺血蜡煤炭 | 3,200 游戏刻, 32,000 制成块时为 |
| Mob Flow Utilities灌注煤炭与木炭 | 12,800 游戏刻 |
| Compressium压缩煤炭 | 144,000 游戏刻 起 |

非燃料物品无法放入燃料槽.

> <Color id="yellow">以320 FE/t运行时,一块煤炭可产生512,000 FE.</Color>
