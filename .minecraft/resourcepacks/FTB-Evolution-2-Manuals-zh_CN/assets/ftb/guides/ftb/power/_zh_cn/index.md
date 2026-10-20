---
navigation:
  title: 发电调整
  position: 0
  icon: powah:energy_cell_nitro
---


<Column alignItems="center" fullWidth={true}>
  # <Color id="gold">发电调整</Color>

  <ItemImage id="powah:energy_cell_nitro" scale="2"/>

  FTB Evolution 2重新平衡了各科技模组的发电,避免单一发电机使其他选择失去意义.本指南列出整合包的改动;未列出的内容以对应模组自身说明为准.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

> <Color id="yellow">数值格式为整合包数值(默认数值).</Color>FE与RF等价.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">主要规则</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

* 奥瑞科技熔岩发电机和Energized Power热力发电机的 **每桶熔岩提供10,000 FE** ;Powah岩浆发电机则为100,000 FE.
* **水不能用作反应堆冷却液.** Powah热力发电机和反应堆使用工业冷却液,将干冰丢入水源即可制得.
* **统一使用一种蒸汽.** Colossal Reactors产出奥瑞科技蒸汽,其涡轮机和奥瑞科技蒸汽引擎都可消耗这种蒸汽.
* **FTB工业奇械直接使用FE.** 其发电机和机器可以连接其他模组的线缆,无需能量整流器.
* **部分早期发电机已移除** ,各模组的发电路线起点由整合包重新安排.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">查找发电机</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

在JEI中搜索`$generator`可列出整合包中所有发电方块,搜索`$energystorage`可查找所有储能设备.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">目录</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<SubPages icons={true} />
