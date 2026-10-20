---
navigation:
  parent: index.md
  title: 冷却液,蒸汽与燃料
  position: 15
  icon: powah:dry_ice
---
<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">冷却液,蒸汽与燃料</Color>

  <ItemImage id="powah:dry_ice" scale="2"/>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">冷却与热源</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="ftb:industrial_coolant_bucket"/>
  ### <Color id="aqua">工业冷却液</Color>
</Row>

工业冷却液取代了反应堆冷却所用的水.将 **干冰** 丢入静止水源方块,即可把它变成工业冷却液.

* **Powah:** 热力发电机和反应堆唯一可用的流体冷却液.水没有效果.
* **Colossal Reactors:** 可用作反应堆内部的散热介质.详见[Colossal Reactors](colossal_reactors.md).

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="auroral:shimmering_ice"/>
  ### <Color id="aqua">Powah固体冷却剂</Color>
</Row>

常见固体冷却剂仍然有效:雪球,雪块,冰,浮冰,蓝冰和干冰.整合包另外添加了:

| 冷却剂 | 用量 | 温度 |
|---|:---:|:---:|
| <ItemImage id="auroral:shimmering_ice"/> 微光冰 | 712 | -32 |

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:blazing_crystal_block"/>
  ### <Color id="aqua">Powah热源</Color>
</Row>

热力发电机与下列方块配合使用时,热源效果有所调整:

| 方块 | 热量 |
|---|:---:|
| <ItemImage id="powah:blazing_crystal_block"/> 烈焰水晶块 | 1,500 (2,800) |
| <ItemImage id="oritech:manhattan_module"/> 曼哈顿模块 | 4,000 (新增) |
| <ItemImage id="ftbic:nuke"/> 核弹 | 4,000 (新增) |
| <ItemImage id="justdirethings:coalblock_t4"/> 蚀空烬质块 | 3,000 (新增) |

岩浆块和熔岩没有改动.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">蒸汽</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

奥瑞科技蒸汽是整合包中唯一的蒸汽.水冷的Colossal Reactors反应堆产出它,Colossal Reactors涡轮机和奥瑞科技蒸汽引擎消耗它.可以自由地用管道在两个模组之间输送蒸汽.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">燃料</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="minecraft:lava_bucket"/>
  ### <Color id="aqua">熔岩</Color>
</Row>

将熔岩用作燃料时,各发电机每桶的发电量如下(奥瑞科技与Energized Power为 **10,000 FE** ,Powah例外):

* 奥瑞科技熔岩发电机:10,000(76,800)
* Energized Power热力发电机:10,000(50,000)
* Powah岩浆发电机:100,000(当前模组每100 mB产生10,000 FE)

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="ftbmaterials:charcoal_block"/>
  ### <Color id="aqua">新增熔炉燃料</Color>
</Row>

以下物品可在熔炉以及接受熔炉燃料的机器中燃烧:

| 燃料 | 燃烧时间 |
|---|:---:|
| <ItemImage id="ftbmaterials:charcoal_block"/> 木炭块 | 16,000 游戏刻 |
| <ItemImage id="mysticalagradditions:inferium_coal"/> 下级至究极精华煤炭 | 2,400 至 76,800 游戏刻 |
| 下级至究极精华煤炭块 | 21,600 至 691,200 游戏刻 |

神秘农业扩展的煤炭每提升一级,燃烧时间便翻倍.
