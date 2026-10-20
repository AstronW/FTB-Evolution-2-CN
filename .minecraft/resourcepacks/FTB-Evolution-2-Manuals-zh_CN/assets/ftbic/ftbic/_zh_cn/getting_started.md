---
navigation:
  title: 入门指南
  icon: ftbic:iron_furnace
  parent: index.md
  position: 1
---

# <Color id="gold">入门指南</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="iron_furnace" scale="2" />

  FTB工业奇械之旅从橡胶,铜和第一块机器外壳开始.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">第1步:橡胶</Color>
</Column>

猎杀史莱姆(或建造史莱姆农场),将每个黏液球 **熔炼** 成 **8个橡胶** .少量黏液球就足以满足前期布线需求.

模组中几乎所有线缆和机器都需要橡胶.

<ItemImage id="minecraft:air" scale="0.25"/>

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">第2步:铁熔炉</Color>
</Column>

通电之前,先用燃料驱动的升级版熔炉提高冶炼效率.

<Row>
  <ItemImage id="iron_furnace" />
  ### <Color id="aqua">铁熔炉</Color>
</Row>

<RecipeFor id="iron_furnace" />

消耗1块煤炭可烧炼 **12个物品** (原版为8个).在收集铜和锡期间,它是可靠的起步设备.

<ItemImage id="minecraft:air" scale="0.25"/>

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">第3步:电路板与机器外壳</Color>
</Column>

<Row>
  <ItemImage id="machine_block" />
  ### <Color id="aqua">机器外壳</Color>
</Row>

用于合成所有LV级机器的空外壳.

<RecipeFor id="machine_block" />

<Row>
  <ItemImage id="electronic_circuit" />
  ### <Color id="aqua">电路板</Color>
</Row>

由铜线,红石和铁板制成,几乎所有LV级设备都需要它.

<RecipeFor id="electronic_circuit" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">第4步:初次发电</Color>
</Column>

建造<ItemLink id="basic_generator" />,用<ItemLink id="lv_cable" />连接到<ItemLink id="macerator" />或<ItemLink id="powered_furnace" />,便进入了电力时代.

<RecipeFor id="basic_generator" />

将支持加工的粗矿放入打粉机,每个得到 **2个粉碎矿石** ,再熔炼成两锭.加入[洗矿机与离心机](machines/ore_refining.md)后,可达到 **每个粗矿5锭** ,即 **每个矿石方块15锭** .

<ItemImage id="minecraft:air" scale="0.25"/>

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">发展路线一览</Color>
</Column>

1. **LV** :基础发电机,初期机器,打粉机,电炉
2. **MV** :太阳能板,矿石加工链(粉→板/齿轮/棒)
3. **HV** :高级机器,压缩机,挤压机,辊压机
4. **EV** :核反应堆,量子装备,传送机
5. **IV/终局** :反物质,机械鞘翅,全自动化

接下来阅读[能源网络](energy/index.md),了解 **电压等级** , **电压** ,以及低等级线缆输入过高电力时会发生什么.
