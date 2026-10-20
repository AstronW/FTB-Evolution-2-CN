---
navigation:
  title: 打粉机
  icon: ftbic:macerator
  parent: machines/index.md
  position: 3
item_ids:
  - ftbic:macerator
  - ftbic:advanced_macerator
---

# <Color id="gold">打粉机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="macerator" scale="2" />

  矿物翻倍的核心设备.将矿石研磨成各 **2份粉** ,将锭研磨成粉,也可将圆石研磨成沙子.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="macerator" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">用途</Color>
</Column>

* 粗矿方块→ **2份粉** (放入任意熔炉烧炼,金属锭产量翻倍).
* 金属锭→1份粉(用于回收或进一步加工).
* 圆石→沙子,沙砾→燧石等.

<RecipesFor id="ftbmaterials:coal_dust" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="advanced_macerator" />
  ### <Color id="aqua">高级打粉机</Color>
</Row>

MV版本:缓存320,000 FE,耗能128 FE/t,配方处理速度大幅提高.

<RecipeFor id="advanced_macerator" />
