---
navigation:
  title: 电池与电池盒
  icon: ftbic:hv_battery
  parent: energy/index.md
  position: 2
item_ids:
  - ftbic:single_use_battery
  - ftbic:lv_battery
  - ftbic:mv_battery
  - ftbic:hv_battery
  - ftbic:ev_battery
  - ftbic:creative_battery
  - ftbic:lv_battery_box
  - ftbic:mv_battery_box
  - ftbic:hv_battery_box
  - ftbic:ev_battery_box
  - ftbic:industrial_bank_cell
  - ftbic:industrial_bank_port
  - ftbic:energy_crystal
---

# <Color id="gold">电池与电池盒</Color>

## <Color id="gold">工业储能组</Color>

将<ItemLink id="industrial_bank_cell" />和<ItemLink id="industrial_bank_port" />面贴面放置,即可组成储能组.每个储能单元增加容量,每个端口通过外露的面接收和输出能量;需要更多连接时可添加端口.右击任意单元或端口,可查看整组的电量,容量和成员数量.端口界面还有四个 **充电** 槽,可用储能组中的能量为电池及其他储能物品充电.端口的侧面配置可限制输入和输出面.

每个储能单元可容纳<Energy config="energy.bank_cell_capacity" />.每个端口自动输出上限为<Energy config="energy.bank_port_transfer" rate="true" />,单次输入事务的上限也相同.输入的能量会转移至相连单元,让端口持续接收电力.这两个数值和每组最大方块搜索数均由服务端配置决定.拆分储能组后,能量仍保留在各单元内;重新连接后,会恢复共享的电量显示.储能组外壳会在相邻面上连成一体.

潜行右击端口可循环切换外观: **端口** (默认连接符号), **仪表** , **基础** (与单元相同的普通钢面).外观设置独立保存在各端口上,重载世界后仍保留,不影响能量输入或输出.选定样式会短暂显示在快捷栏上方.

仪表以发光条显示整个储能组的充能比例.在同一平面上将相邻端口设为仪表,即可组成更宽或更高的显示屏.矩形仪表面板从整块面板的底部开始填充.基础或端口样式,空隙,被遮挡的面和拐角都会截断显示;不规则仪表形状则会拆分成较小的矩形面板.

<RecipeFor id="industrial_bank_cell" />
<RecipeFor id="industrial_bank_port" />

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="hv_battery_box" scale="2" />

  电池提供便携电力.电池盒则是电网缓存:将电池放入充电,充满后取出供手持设备使用.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">便携电池</Color>
</Column>

<Row>
  <ItemImage id="single_use_battery" />
  ### <Color id="aqua">一次性电池</Color>
</Row>

廉价的一次性电池,容量为<Energy config="energy.single_use_battery_capacity" />.适合应急,不适合长期供电.

<RecipeFor id="single_use_battery" />

<Row>
  <ItemImage id="lv_battery" />
  ### <Color id="aqua">电池(LV)</Color>
</Row>

容量为<Energy config="energy.lv_battery_capacity" />,LV级.你能制作的第一种充电电池.

<RecipeFor id="lv_battery" />

<Row>
  <ItemImage id="mv_battery" />
  ### <Color id="aqua">电池(MV)</Color>
</Row>

容量为<Energy config="energy.mv_battery_capacity" />.使用<ItemLink id="energy_crystal" />从LV电池升级而来.

<RecipeFor id="mv_battery" />

<Row>
  <ItemImage id="hv_battery" />
  ### <Color id="aqua">电池(HV)</Color>
</Row>

容量为<Energy config="energy.hv_battery_capacity" />.用于中后期手持装备.

<RecipeFor id="hv_battery" />

<Row>
  <ItemImage id="ev_battery" />
  ### <Color id="aqua">电池(EV)</Color>
</Row>

容量为<Energy config="energy.ev_battery_capacity" />.模组中容量最大的便携电池.

<RecipeFor id="ev_battery" />

<Row>
  <ItemImage id="creative_battery" />
  ### <Color id="aqua">创造电池</Color>
</Row>

能量无限,仅限创造模式.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">电池盒</Color>
</Column>

电池盒左侧是 **放电** 槽,右侧是 **充电** 槽.将已充电电池放入放电槽,可为电池盒供电;将空电池或其他储能物品放入充电槽,即可补充电量.每种电池盒还有与其等级相符的内部能量缓存.

打开 **I/O** ,选择 **能量** ,将任意面设为 **输出** 即可向该面供电;可将多个面同时设为输出.设为 **输入** 可接收能量, **双向** 允许两个方向传输, **禁用** 则断开连接. **默认** 保留原始布局:正面输出,其余面输入.各面的输入/输出纹理会随其输出状态变化.同样的控制方式适用于LV,MV,HV和EV电池盒.

<Row>
  <ItemImage id="lv_battery_box" />
  ### <Color id="aqua">电池盒(LV) (<Energy config="energy.lv_battery_box_capacity" />)</Color>
</Row>

<RecipeFor id="lv_battery_box" />

<Row>
  <ItemImage id="mv_battery_box" />
  ### <Color id="aqua">电池盒(MV) (<Energy config="energy.mv_battery_box_capacity" />)</Color>
</Row>

<RecipeFor id="mv_battery_box" />

<Row>
  <ItemImage id="hv_battery_box" />
  ### <Color id="aqua">电池盒(HV) (<Energy config="energy.hv_battery_box_capacity" />)</Color>
</Row>

<RecipeFor id="hv_battery_box" />

<Row>
  <ItemImage id="ev_battery_box" />
  ### <Color id="aqua">电池盒(EV) (<Energy config="energy.ev_battery_box_capacity" />)</Color>
</Row>

<RecipeFor id="ev_battery_box" />

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="energy_crystal" />
  ### <Color id="aqua">能量水晶</Color>
</Row>

由钻石和红石压缩而成.制作MV及以上电池和高容量设备时需要使用.

<RecipeFor id="energy_crystal" />
