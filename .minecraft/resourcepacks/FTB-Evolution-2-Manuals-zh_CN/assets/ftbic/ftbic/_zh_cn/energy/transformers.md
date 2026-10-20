---
navigation:
  title: 变压器
  icon: ftbic:mv_transformer
  parent: energy/index.md
  position: 3
item_ids:
  - ftbic:lv_transformer
  - ftbic:mv_transformer
  - ftbic:hv_transformer
  - ftbic:ev_transformer
---

# <Color id="gold">变压器</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="mv_transformer" scale="2" />

  变压器可以将高等级电压 **降低** 为低等级,反向连接则可 **升压** .每台变压器有一个高压面和五个低压面.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

不用变压器而将HV电力输入LV机器,会使其立即烧毁.变压器将N级电力转换为下一级,按对应低等级的传输速率输出.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="lv_transformer" />
  ### <Color id="aqua">变压器(LV)</Color>
</Row>

将MV(4,096 FE/t)降为LV(1,024 FE/t).

<RecipeFor id="lv_transformer" />

<Row>
  <ItemImage id="mv_transformer" />
  ### <Color id="aqua">变压器(MV)</Color>
</Row>

将HV(16,384 FE/t)降为MV(4,096 FE/t).

<RecipeFor id="mv_transformer" />

<Row>
  <ItemImage id="hv_transformer" />
  ### <Color id="aqua">变压器(HV)</Color>
</Row>

将EV(65,536 FE/t)降为HV(16,384 FE/t).

<RecipeFor id="hv_transformer" />

<Row>
  <ItemImage id="ev_transformer" />
  ### <Color id="aqua">变压器(EV)</Color>
</Row>

将IV(262,144 FE/t)降为EV(65,536 FE/t).

<RecipeFor id="ev_transformer" />
