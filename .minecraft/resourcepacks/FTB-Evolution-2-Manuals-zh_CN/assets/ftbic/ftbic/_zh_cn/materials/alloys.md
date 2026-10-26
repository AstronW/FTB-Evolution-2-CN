---
navigation:
  title: 合金
  icon: ftbic:iridium_alloy
  parent: materials/index.md
  position: 2
item_ids:
  - ftbic:mixed_metal_blend
  - ftbic:advanced_alloy
  - ftbic:industrial_grade_metal
  - ftbic:steel_ingot
  - ftbmaterials:bronze_ingot
  - ftbmaterials:electrum_ingot
  - ftbmaterials:invar_ingot
  - ftbmaterials:constantan_ingot
  - ftbic:iridium_alloy
  - ftbic:machine_block
  - ftbic:advanced_machine_block
  - ftbic:enderium_ingot
  - ftbic:enderium_nugget
  - ftbic:enderium_plate
  - ftbic:enderium_rod
  - ftbic:enderium_gear
  - ftbic:enderium_wire
  - ftbic:enderium_block
---

# <Color id="gold">合金</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="iridium_alloy" scale="2" />

  合金将多种金属锭组合为高级材料.<ItemLink id="alloy_smelter" />是加工核心:所有金属合金都由它生产.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">基础合金</Color>
</Column>

将原料金属锭放入<ItemLink id="alloy_smelter" />制得.各合金均可重新打成粉,再次熔炼回收.

<Row>
  <ItemImage id="ftbmaterials:bronze_ingot" />
  ### <Color id="aqua">青铜</Color>
</Row>

3铜+1锡→4青铜.用于高级合金青铜路线的中级合金.

<Recipe id="ftb:unification/ftbic/alloy_smelting/from_ingots/bronze" />

<Row>
  <ItemImage id="ftbmaterials:electrum_ingot" />
  ### <Color id="aqua">琥珀金</Color>
</Row>

1银+1金→2琥珀金.用于高级合金琥珀金路线和导电合金加工链.

<Recipe id="ftb:unification/ftbic/alloy_smelting/from_ingots/electrum" />

<Row>
  <ItemImage id="ftbmaterials:invar_ingot" />
  ### <Color id="aqua">殷钢</Color>
</Row>

2铁+1镍→3殷钢.用于高级合金殷钢路线,也可充当耐热中间材料.

<Recipe id="ftb:unification/ftbic/alloy_smelting/from_ingots/invar" />

<Row>
  <ItemImage id="ftbmaterials:constantan_ingot" />
  ### <Color id="aqua">康铜</Color>
</Row>

通用中间合金. 合金炉没有康铜配方; 康铜锭可通过冶炼康铜粉, 或由粒和块转换得到.

<RecipesFor id="ftbmaterials:constantan_ingot" fallbackText="No recipes found for constantan." />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">钢:高级合金的起点</Color>
</Column>

<Row>
  <ItemImage id="steel_ingot" />
  ### <Color id="aqua">钢锭</Color>
</Row>

加工链中最重要的合金: **所有高级合金配方都以钢为起点.** 在<ItemLink id="alloy_smelter" />中将<ItemLink id="industrial_grade_metal" />与碳源合金化制得:

* 1工业级金属+1煤炭→1钢锭
* 1工业级金属+1木炭→1钢锭

<RecipesFor id="steel_ingot" />

制作<ItemLink id="advanced_machine_block" />,<ItemLink id="reactor_plating" />或任何HV及以上机器前,请先储备钢,因为它们的后续材料都需要高级合金.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">高级合金粉与工业级金属</Color>
</Column>

<Row>
  <ItemImage id="mixed_metal_blend" />
  ### <Color id="aqua">高级合金粉</Color>
</Row>

将<ItemLink id="advanced_alloy" />打粉后回收为高级合金粉,可再熔炼成高级合金.合金粉没有有序合成配方;合金炉配方会直接跳过这一阶段.

<RecipesFor id="mixed_metal_blend" />

<Row>
  <ItemImage id="industrial_grade_metal" />
  ### <Color id="aqua">工业级金属</Color>
</Row>

压缩铁:将三个铁锭压缩为一个工业级金属.用于<ItemLink id="machine_block" />,也是炼钢的主要原料.

<RecipeFor id="industrial_grade_metal" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">高级合金</Color>
</Column>

<Row>
  <ItemImage id="advanced_alloy" />
  ### <Color id="aqua">高级合金</Color>
</Row>

所有后期机器,护甲,反应堆部件和<ItemLink id="iridium_alloy" />的基础材料.在<ItemLink id="alloy_smelter" />中通过三种以钢为基础的配方之一制得:

* 1钢+2青铜+1铝→1高级合金
* 1钢+1琥珀金+1铝→1高级合金
* 1钢+2殷钢+1铝→1高级合金

根据手头合金选择路线:铜和锡充足时青铜路线最便宜;殷钢路线消耗更多铁;银和金充足时,琥珀金路线最省金属锭.

<RecipesFor id="advanced_alloy" />

<Row>
  <ItemImage id="iridium_alloy" />
  ### <Color id="aqua">铱合金</Color>
</Row>

用<ItemLink id="advanced_alloy" />强化铱板制得的终级合金,用于<ItemLink id="iridium_circuit" />,<ItemLink id="iridium_neutron_reflector" />和<ItemLink id="quantum_helmet" />.

<RecipeFor id="iridium_alloy" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">末影</Color>
</Column>

紫蓝色魔法合金,用于<ItemLink id="teleporter" />,<ItemLink id="iv_cable" />和高级电路板.

<Row>
  <ItemImage id="enderium_ingot" />
  ### <Color id="aqua">末影锭</Color>
</Row>

在<ItemLink id="alloy_smelter" />中制作: 1 个铅锭 + 1 个钻石 + 1 个末影珍珠 → 1 个末影合金锭. 没有有序合成配方.

<Recipe id="ftb:unification/ftbic/alloy_smelting/from_ingots/enderium" />

<Row>
  <ItemImage id="enderium_block" />
  ### <Color id="aqua">末影块</Color>
</Row>

9锭→一个方块,便于大量储存.

<RecipeFor id="enderium_block" />

末影合金具有所有常见加工形态:<ItemLink id="enderium_nugget" />,<ItemLink id="enderium_plate" />,<ItemLink id="enderium_rod" />,<ItemLink id="enderium_gear" />和<ItemLink id="enderium_wire" />.
