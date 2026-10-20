---
navigation:
  parent: index.md
  title: 奥瑞科技
  position: 40
  icon: oritech:fuel_generator
---
<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">奥瑞科技</Color>

  <ItemImage id="oritech:fuel_generator" scale="2"/>

  奥瑞科技的小型发电机比默认设置更强,裂变反应堆则大幅削弱,早期部件也不再需要钢.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">发电机</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

| 发电机 | 输出 |
|---|:---:|
| <ItemImage id="oritech:basic_generator"/> 基础发电机 | 64 RF/t (32) |
| <ItemImage id="oritech:bio_generator"/> 生物发电机 | 256 RF/t (64) |
| <ItemImage id="oritech:fuel_generator"/> 燃料发电机 | 8,192 RF/t (256) |
| <ItemImage id="oritech:lava_generator"/> 熔岩发电机 | 64 RF/t, 未改动 |
| <ItemImage id="oritech:big_solar_panel"/> 大型太阳能板 | 128 RF/t (32) |

熔岩发电机消耗熔岩的速度大幅加快,达到每秒128 mB.一桶可产生10,000 RF(76,800).

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="oritech:steam_engine"/>
  ### <Color id="aqua">蒸汽引擎</Color>
</Row>

* 蒸汽锅炉插件每RF产生的蒸汽量翻倍(比率4,原为2).蒸汽引擎每mB蒸汽的发电量没有改动.
* 锅炉容量为128桶(8).
* 使用的蒸汽与Colossal Reactors产出的蒸汽相同.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="oritech:nuclear_reactor_controller"/>
  ### <Color id="aqua">裂变反应堆</Color>
</Row>

* 每次燃料脉冲产生38 RF(64).
* 每个能量端口最多输出75,000 RF/t(25,000).
* 反应堆最多储存500,000,000 RF(50,000,000).
* 最大热量为4,000(2,000),但不稳定状态持续400游戏刻后即进入临界状态(600).
* 反应堆最大边长为16格(64).

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">储能</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

便携式储能装置和大型储能装置的容量提高25%,传输速率也提高25%:

* <ItemImage id="oritech:portable_energy_storage"/> 便携式储能装置:1,250,000 RF,6,250 RF/t
* <ItemImage id="oritech:large_storage"/> 大型储能装置:25,000,000 RF,12,500 RF/t

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">简化早期部件</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="oritech:magnetic_coil"/>
  ### <Color id="aqua">磁线圈</Color>
</Row>

用镍锭围绕铁锭和铁块合成,不再需要钢.每次产出四个.

<RecipeFor id="oritech:magnetic_coil"/>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="oritech:motor"/>
  ### <Color id="aqua">马达</Color>
</Row>

使用镍,铁板,一个磁线圈和一个铁块,不再需要钢.

<RecipeFor id="oritech:motor"/>
