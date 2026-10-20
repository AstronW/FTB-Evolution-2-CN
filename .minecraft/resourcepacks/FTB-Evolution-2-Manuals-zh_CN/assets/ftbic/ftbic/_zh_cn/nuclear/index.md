---
navigation:
  title: 核能
  icon: ftbic:nuclear_reactor
  position: 40
---

# <Color id="gold">核能发电</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="nuclear_reactor" scale="2" />

  模组中输出最高的电源,也是失误代价最大的设备.正常反应堆可产生 **每刻数百至数千<EnergyUnit />** ,失控反应堆则会 **摧毁你的基地** .
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">三个关键变量</Color>
</Column>

反应堆布局是三种互相影响的量之间的平衡问题.

* <Color id="red"> **热量** </Color>:由燃料棒产生,在堆芯累积.
* <Color id="aqua"> **冷却** </Color>:冷却单元和散热片从相邻燃料棒吸热并散出.
* <Color id="gold"> **输出** </Color>:每刻产生的<EnergyUnit />,相邻中子反射板及双联/四联燃料棒可提高输出.

热量达到100%时反应堆会 **爆炸** ,基础半径为 **10格** ,最大 **80格** ,足以炸出直达基岩的巨坑.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">分节</Color>
</Column>

<SubPages icons={true} />
