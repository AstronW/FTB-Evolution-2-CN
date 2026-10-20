---
navigation:
  parent: index.md
  title: 魔法
  position: 50
  icon: arsmagicalegacy:spell_book
---

<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">魔法</Color>

  <ItemImage id="arsmagicalegacy:spell_book" scale="2"/>

  整合包中各类魔法模组的行为都能提升魔法等级,并不限于魔法艺术.仪式,法阵,酿造,灵魂操作和附魔均有效,可以选择自己喜欢的流派.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

> <Color id="yellow">注意</Color>:魔法艺术:传承有独立的魔法等级和技能点,用于解锁法术组件,与本技能树分开计算.它的魔法等级每提升一级,本魔法技能树也会获得经验.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">通用来源</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

| 行为 | 魔法经验 |
|---|---|
| 对生物造成魔法伤害 | 每点伤害0.5 |
| 在<ItemLink id="minecraft:enchanting_table"/>上为物品附魔 | 30 |

<ItemImage id="minecraft:air" scale="0.25"/>

魔法伤害包括原版魔法(瞬间伤害,中毒药水云等),魔法艺术:传承的法术,根源魔法经典版的法术,以及邪恶工艺的复仇光束.攻击训练假人不会获得经验.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">各模组来源</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="arsmagicalegacy:spell_book"/>
  ### <Color id="aqua">魔法艺术:传承</Color>
</Row>

* <Color id="gray">魔法艺术的魔法等级每提升一级</Color>:60

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="neovitae:master_ritual_stone"/>
  ### <Color id="aqua">Neo Vitae</Color>
</Row>

* <Color id="gray">在以下方块上激活仪式</Color> <ItemLink id="neovitae:master_ritual_stone"/>:100
* <Color id="gray">在以下方块上激活不完美仪式</Color> <ItemLink id="neovitae:imperfect_ritual_stone"/>:20
* <Color id="gray">自我献祭</Color>:每献出一点生命值获得3点经验.包括为生命宝珠充能,站在<ItemLink id="neovitae:ara_vitae"/>旁让它抽取血液,以及自愿献祭仪式.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="occultism:golden_sacrificial_bowl"/>
  ### <Color id="aqua">神秘学</Color>
</Row>

* <Color id="gray">完成任意仪式</Color>:80

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="witchery:golden_ritual_chalk"/>
  ### <Color id="aqua">巫术</Color>
</Row>

* <Color id="gray">完成用以下粉笔绘制的仪式</Color> <ItemLink id="witchery:golden_ritual_chalk"/>:100.仪式完成时你必须在线.
* <Color id="gray">从以下方块中装瓶取出药酿</Color> <ItemLink id="witchery:cauldron"/>:10
* <Color id="gray">施放符号学法术</Color>:5
* <Color id="gray">吸血鬼,狼人或巫妖等级每提升一级</Color>:150

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="rootsclassic:staff"/>
  ### <Color id="aqua">根源魔法经典版</Color>
</Row>

* <Color id="gray">在以下方块上开始仪式</Color> <ItemLink id="rootsclassic:altar"/>:100
* <Color id="gray">用以下物品施法</Color> <ItemLink id="rootsclassic:staff"/>:5

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="anima:infusion_table"/>
  ### <Color id="aqua">Anima</Color>
</Row>

* <Color id="gray">在以下方块上完成灌注</Color> <ItemLink id="anima:infusion_table"/>:60
* <Color id="gray">在以下方块上抄写或翻译法术书</Color> <ItemLink id="anima:soul_altar"/>:25
* <Color id="gray">向以下方块献上的祭品被接受</Color> <ItemLink id="anima:dark_altar"/>:15
* <Color id="gray">使用祭司能力</Color>:10
* <Color id="gray">用以下武器或萨隆铁箭击杀生物并释放灵魂</Color> <ItemLink id="anima:saronite_sword"/>:8
* <Color id="gray">用玻璃器皿提取灵魂</Color>:8
* <Color id="gray">施放灵魂法术</Color>:5
* <Color id="gray">将瓶装灵魂倒入灵魂之井</Color>:3

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="evilcraft:box_of_eternal_closure"/>
  ### <Color id="aqua">邪恶工艺</Color>
</Row>

* <Color id="gray">用以下物品捕获灵体</Color> <ItemLink id="evilcraft:box_of_eternal_closure"/>:80
* <Color id="gray">用以下物品唤起亡者</Color> <ItemLink id="evilcraft:necromancer_staff"/>:20
* <Color id="gray">用以下物品击中至少一只生物</Color> <ItemLink id="evilcraft:mace_of_distortion"/>:10

<ItemImage id="minecraft:air" scale="0.25"/>

<Color id="gold">提示</Color>:仪式类行为的单次经验最多.每天做几次Neo Vitae,巫术,根源魔法或神秘学仪式,比单靠施法升级更快.
