---
navigation:
  title: 粉,板与棒
  icon: ftbic:dense_copper_plate
  parent: materials/index.md
  position: 1
item_ids:
  - ftbic:coal_dust
  - ftbic:charcoal_dust
  - ftbic:diamond_dust
  - ftbic:obsidian_dust
  - ftbic:dense_copper_plate
  - ftbic:copper_coil
  - ftbic:coal_ball
  - ftbic:compressed_coal_ball
  - ftbic:graphene
---

# <Color id="gold">粉,板及其他形态</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="dense_copper_plate" scale="2" />

  几乎所有配方都会使用的中间材料形态.粉来自<ItemLink id="macerator" />,板来自<ItemLink id="roller" />或<ItemLink id="extruder" />,棒和齿轮来自挤压加工链.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">特殊粉末</Color>
</Column>

<Row>
  <ItemImage id="ftbic:coal_dust" />
  ### <Color id="aqua">煤粉</Color>
</Row>

煤炭研磨而成,用于合成碳纤维和煤球.

<RecipesFor id="ftbic:coal_dust" />

<Row>
  <ItemImage id="ftbic:charcoal_dust" />
  ### <Color id="aqua">木炭粉</Color>
</Row>

<Row>
  <ItemImage id="ftbic:obsidian_dust" />
  ### <Color id="aqua">黑曜石粉</Color>
</Row>

<Row>
  <ItemImage id="ftbic:diamond_dust" />
  ### <Color id="aqua">钻石粉</Color>
</Row>

在打粉机中研磨钻石,再将两份粉压回钻石.当你想从回收装备中获取钻石时,这条路线可带来额外+100%的收益.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">特殊板材及其他部件</Color>
</Column>

<Row>
  <ItemImage id="dense_copper_plate" />
  ### <Color id="aqua">致密铜板</Color>
</Row>

将9块铜板压缩为一块,用于<ItemLink id="nuclear_reactor" />配方和高级部件.

<Row>
  <ItemImage id="copper_coil" />
  ### <Color id="aqua">铜制线圈</Color>
</Row>

将铜线缠绕在铁棒上制得,用于发电机和变压器.

<RecipeFor id="copper_coil" />

<Row>
  <ItemImage id="coal_ball" />
  ### <Color id="aqua">煤球</Color>
</Row>

4煤粉+4燧石→煤球,是钻石回收加工链的一环.

<RecipeFor id="coal_ball" />

<Row>
  <ItemImage id="compressed_coal_ball" />
  ### <Color id="aqua">压缩煤球</Color>
</Row>

压缩8个煤球制得,用于后续钻石配方.

<Row>
  <ItemImage id="graphene" />
  ### <Color id="aqua">石墨烯</Color>
</Row>

由碳和硅挤压而成,用于终局电路.

<RecipeFor id="graphene" />
