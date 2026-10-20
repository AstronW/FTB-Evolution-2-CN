---
navigation:
  title: 太阳能板
  icon: ftbic:hv_solar_panel
  parent: generators/index.md
  position: 3
item_ids:
  - ftbic:lv_solar_panel
  - ftbic:mv_solar_panel
  - ftbic:hv_solar_panel
  - ftbic:ev_solar_panel
---

# <Color id="gold">太阳能板</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="hv_solar_panel" scale="2" />

  太阳能板需要 **上方直通天空** 且处于 **白天** 才能发电,夜间或被遮挡时没有输出.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="lv_solar_panel" />
  ### <Color id="aqua">太阳能板(LV)</Color>
</Row>

白天产生32 FE/t,缓存1,920 FE,入门级太阳能板.

<RecipeFor id="lv_solar_panel" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="mv_solar_panel" />
  ### <Color id="aqua">太阳能板(MV)</Color>
</Row>

白天产生256 FE/t,缓存15,360 FE.

<RecipeFor id="mv_solar_panel" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="hv_solar_panel" />
  ### <Color id="aqua">太阳能板(HV)</Color>
</Row>

白天产生2,048 FE/t,缓存122,880 FE.

<RecipeFor id="hv_solar_panel" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="ev_solar_panel" />
  ### <Color id="aqua">太阳能板(EV)</Color>
</Row>

白天产生16,384 FE/t,缓存800,000 FE,是模组中输出最高的太阳能板.

<RecipeFor id="ev_solar_panel" />
