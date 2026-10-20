---
navigation:
  title: 能量整流器
  icon: ftbic:mv_rectifier
  parent: energy/index.md
  position: 4
item_ids:
  - ftbic:lv_rectifier
  - ftbic:mv_rectifier
  - ftbic:hv_rectifier
  - ftbic:ev_rectifier
  - ftbic:iv_rectifier
---

# <Color id="gold">能量整流器</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="hv_rectifier" scale="2" />

  **本整合包无需整流器.** FTB工业奇械在此使用FE模式:所有发电机均输出FE,所有机器均可从任意面接收FE,因此其他模组的电力可以直接输入.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">工作原理</Color>
</Column>

整流器仍可合成.它具有方向性: **FE面** 从相邻线缆,发电机或储能设备接收电力,其余面按对应电压等级的传输速率输出:

| 整流器 | FE传输速率 |
|-----------|----------|
| LV | 1,024 FE/t |
| MV | 4,096 FE/t |
| HV | 16,384 FE/t |
| EV | 65,536 FE/t |
| IV | 262,144 FE/t |


<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="lv_rectifier" />
  ### <Color id="aqua">整流器(LV)</Color>
</Row>

<RecipeFor id="lv_rectifier" />

<Row>
  <ItemImage id="mv_rectifier" />
  ### <Color id="aqua">整流器(MV)</Color>
</Row>

<RecipeFor id="mv_rectifier" />

<Row>
  <ItemImage id="hv_rectifier" />
  ### <Color id="aqua">整流器(HV)</Color>
</Row>

<RecipeFor id="hv_rectifier" />

<Row>
  <ItemImage id="ev_rectifier" />
  ### <Color id="aqua">整流器(EV)</Color>
</Row>

<RecipeFor id="ev_rectifier" />

<Row>
  <ItemImage id="iv_rectifier" />
  ### <Color id="aqua">整流器(IV)</Color>
</Row>

<RecipeFor id="iv_rectifier" />
