---
navigation:
  title: 合金炉
  icon: ftbic:alloy_smelter
  parent: machines/index.md
  position: 14
item_ids:
  - ftbic:alloy_smelter
---

# <Color id="gold">合金炉</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="alloy_smelter" scale="2" />

  三输入合金设备.将金属锭合成为青铜,琥珀金,殷钢,康铜,钢,末影,下界合金和高级合金等复合金属,无需先加工成粉或其他形态.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="alloy_smelter" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">槽位与输入唯一性规则</Color>
</Column>

合金炉有 **三个输入槽** 和 **一个输出槽** .每个输入槽存放一种原料,数量可自行调整;配方数量按单个槽位中的堆叠数匹配,不会跨槽合并.

输入槽遵循 **物品种类唯一** 规则:一种物品放入某个槽后,其他两个槽便不再接受同种物品.这样可避免误将一组物品拆分到不同槽位,导致要求同一槽中有`2 gold`的配方无法运行.应把4个金锭都放在槽位1,而不是槽位1放2个,槽位2放2个.

原料可匹配多个配方时,合金炉优先选择 **原料种类最多** 的配方.因此填满三个槽位时,会优先加工3输入合金,而不会选择其中的2输入配方.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">合金配方</Color>
</Column>

<Row>
  <ItemImage id="bronze_ingot" />
  ### <Color id="aqua">青铜</Color>
</Row>

3铜+1锡→4青铜锭.

<Row>
  <ItemImage id="electrum_ingot" />
  ### <Color id="aqua">琥珀金</Color>
</Row>

1银+1金→2琥珀金锭.

<Row>
  <ItemImage id="invar_ingot" />
  ### <Color id="aqua">殷钢</Color>
</Row>

2铁+1镍→3殷钢锭.

<Row>
  <ItemImage id="constantan_ingot" />
  ### <Color id="aqua">康铜</Color>
</Row>

1铜+1镍→2康铜锭.

<Row>
  <ItemImage id="steel_ingot" />
  ### <Color id="aqua">钢</Color>
</Row>

1个<ItemLink id="industrial_grade_metal" />+1煤炭 **或** 1木炭→1钢锭.钢是高级合金的前置材料,下方列出了<ItemLink id="advanced_alloy" />配方.

<Row>
  <ItemImage id="minecraft:netherite_ingot" />
  ### <Color id="aqua">下界合金</Color>
</Row>

2金+2下界合金碎片→1下界合金锭.完全跳过原版钻石装备与下界合金锭的锻造步骤.

<Row>
  <ItemImage id="enderium_ingot" />
  ### <Color id="aqua">末影</Color>
</Row>

3铅+1钻石粉+2末影珍珠→2末影锭.这是制作末影锭的唯一路线,没有有序合成配方.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">高级合金</Color>
</Column>

合金炉可通过三种以钢为基础的配方制作<ItemLink id="advanced_alloy" />. **所有路线都需要钢** ,请先将工业级金属与煤炭或木炭合金化制钢.

* 1钢+2青铜+1铝→1高级合金
* 1钢+1琥珀金+1铝→1高级合金
* 1钢+2殷钢+1铝→1高级合金

<RecipesFor id="advanced_alloy" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">参数</Color>
</Column>

* **等级:** MV(中压输入)
* **能量缓存:** 320,000 FE
* **耗能:** 384 FE/t,是<ItemLink id="advanced_powered_furnace" />的三倍
* **默认周期:** 每配方200游戏刻(可用<ItemLink id="overclocker_upgrade" />调整)

<ItemImage id="minecraft:air" scale="0.25"/>
