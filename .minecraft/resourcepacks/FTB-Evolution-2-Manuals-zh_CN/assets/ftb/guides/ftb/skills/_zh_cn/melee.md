---
navigation:
  parent: index.md
  title: 近战
  position: 10
  icon: minecraft:iron_sword
---

<Column alignItems="center" fullWidth={true}>
  # <Color id="red">近战</Color>

  <ItemImage id="minecraft:iron_sword" scale="2"/>

  近距离作战可以提升近战等级,包括攻击,击杀,格挡和承受伤害.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">经验来源</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

| 行为 | 近战经验 |
|---|---|
| 造成非弹射物伤害 | 每点伤害0.25 |
| 使用弹射物以外的方式击杀生物 | 见下方"击杀" |
| 用盾牌挡住攻击 | 每次5 |
| 承受摔落以外的伤害 | 每点伤害1 |

<ItemImage id="minecraft:air" scale="0.25"/>

"非弹射物"的范围比字面上更广.大多数法术,<ItemLink id="nautec:atlantean_rifle"/>的光束,以及LTX工业的枪械和手榴弹,在提供各自技能树经验的同时,也会计入近战伤害.箭,三叉戟,投掷物和Iron's Arms 'n Artifice的子弹则不计入.

攻击训练假人不会获得经验.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">击杀</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

击杀经验根据生物自身的经验掉落量和生命值计算:

* 先计入掉落的经验,最多计入10点
* 再加上超出10点部分的平方根的两倍
* 再加上其最大生命值的五分之一,此项最多计入40点

击杀僵尸(掉落5经验,20生命值)可获得9点技能经验;击杀凋灵(掉落50经验,300生命值)约可获得63点.

<ItemImage id="minecraft:air" scale="0.25"/>

> <Color id="yellow">注意</Color>:每个区块只计算前15次击杀,计数每5分钟重置.在同一处集中击杀的刷怪场很快就会停止提供经验.
