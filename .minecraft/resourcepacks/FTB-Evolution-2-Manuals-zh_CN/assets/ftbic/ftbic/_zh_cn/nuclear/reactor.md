---
navigation:
  title: 核反应堆
  icon: ftbic:nuclear_reactor
  parent: nuclear/index.md
  position: 1
item_ids:
  - ftbic:nuclear_reactor
  - ftbic:nuclear_reactor_chamber
---

# <Color id="gold">核反应堆</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="nuclear_reactor" scale="2" />

  反应堆核心具有3×3元件网格,最多可连接 **6个核反应仓** (每面一个),扩展为9+6×3=27个槽位.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="nuclear_reactor" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">核反应仓</Color>
</Column>

在反应堆任意面安装反应仓,即可解锁新的一列3个元件槽,最多6个反应仓→9列→共27槽.反应仓也会将管道输入的 **能量** 和 **物品** 传递给中心反应堆.将线缆或漏斗连接到反应仓外侧,与直接连接反应堆的电网和物品栏效果相同.

<RecipeFor id="nuclear_reactor_chamber" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">运行方法</Color>
</Column>

* **等级:** 默认EV输出,极限设计可达到IV.
* **内部能量缓存:** 800,000 FE.
* 打开界面,将燃料棒,散热片,冷却单元,反射板和隔板放入网格.
* 用红石控制反应堆开关.没有信号时暂停,便于在两次脉冲之间冷却.
* Jade/The One Probe显示实时热量百分比和输出.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">环境冷却</Color>
</Column>

反应堆每周期检查外壳及相连反应仓所有朝外的面.每个接触 **水** 方块的面,都会按比例增强内部各<ItemLink id="heat_vent" />,<ItemLink id="reactor_heat_vent" />,<ItemLink id="overclocked_heat_vent" />和<ItemLink id="advanced_heat_vent" />从外壳散热的能力:

* 0个面邻水→ **1倍** 冷却(基准)
* 完全浸没→ **10倍** 冷却,按邻水面数线性增加

省钱做法是将反应堆放入浅水池,再用玻璃封顶,这样各元件的`reactorCool`值最多可免费变成10倍.流动水和静止水均有效,熔岩和空气无效.

强化线缆及其烧坏变种被视为 **中性** 面,计算比例时完全跳过.因此用强化线缆从水下反应堆引出电力,不会稀释水冷加成.

<ItemImage id="minecraft:air" scale="0.25"/>

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">防护结构</Color>
</Column>

热量达到100%时,反应堆一定会爆炸.在尝试激进设计前,请先用抗爆方块(<ItemLink id="reinforced_stone" />或<ItemLink id="reinforced_glass" />)构筑防护墙.爆炸从 **10格基础半径** 增长,最大为 **80格** ,足以波及基岩.

元件槽可用部件详见[燃料棒](fuel_rods.md),[冷却](cooling.md),[反射板](reflectors.md)和[隔板](plating.md).
