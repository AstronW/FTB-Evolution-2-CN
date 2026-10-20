---
navigation:
  title: 搅拌机
  icon: nautec:mixer
  position: 4
  parent: laser_chemistry/laser_chemistry-index.md
item_ids:
  - nautec:mixer
---

# <Color id="light_purple">搅拌机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="mixer" scale="2"/>
  将物品混入盐水, 以制作化学品, 海蓝钢混合物和机器零件.
</Column>

## <Color id="gold">搭建</Color>

搅拌机可从任意一面接收激光束, 只要每 tick 到达至少 10 AP(可配置)就会运行. 一个燃烧海晶碎片或海棱水晶碎片的<ItemLink id="aquatic_catalyst"/>就足够. 燃烧海晶水晶的则不够; 请通过[激光转接器](laser_manipulation.md)接入第二个源头.

用空手右键点击可打开它. 它有四个原料槽位, 一个输出槽位, 一个输入储罐和一个输出储罐, 每个储罐容量为 32,000 mB(32 桶, 可配置).

* 手持<ItemLink id="saltwater_bucket"/>右键点击可为输入储罐加注. 盐水来自[深海排水口](drain.md), 或由搅拌机本身用水桶和盐制作.
* 手持空桶右键点击可从输出储罐取出流体.
* 漏斗和管道可以放入原料, 加注输入储罐并抽出输出储罐.
* 物品产物可从输出槽位抽出.
* 默认情况下每个面都可执行以上所有操作. [侧面配置](nautec:getting_started/utilities.md)可分别设置每个面的物品和流体.

工作时搅拌器会旋转. <ItemLink id="prism_monocle"/>会显示到达的功率, Jade 还会显示其储罐和搅拌进度.

***

## <Color id="gold">配方</Color>

JEI 会在搅拌分类下列出原料.

| 产物 | 消耗流体 | 时间 |
|---|---|---|
| 1,000 mB 盐水 | 1,000 mB 水和 1 个<ItemLink id="salt"/> | 5 秒 |
| 1,000 mB 电解藻类浆液 | 1,000 mB 盐水 | 10 秒 |
| 1,000 mB 蚀刻酸 | 1,000 mB 盐水 | 7.5 秒 |
| 5 个海蓝钢混合物 | 1,000 mB 盐水 | 5 秒 |
| 1 个<ItemLink id="burnt_coil"/> | 1,000 mB 盐水 | 10 秒 |
| 2 个<ItemLink id="aquatic_chip"/> | 1,000 mB 盐水 | 10 秒 |
| 1 个<ItemLink id="pressure_synthesizer"/> | 8,000 mB 盐水 | 20 秒 |
| 1 个<ItemLink id="atlantean_pressure_synthesizer"/> | 8,000 mB 盐水 | 30 秒 |

只有当产物能放入输出时配方才会开始, 因此请在批次之间清空输出储罐或槽位. 断电只会暂停混合, 不会重置进度.

<Color id="gold">提示</Color>: 输出储罐中有流体时, 手持桶右键点击会作用于输出储罐, 因此盐水桶无法放入. 请先清空输出.

各流体的用途参见[化学流体](chemistry_introduction.md).

***

### <Color id="aqua">搅拌机配方</Color>

<ItemLink id="whisk"/>可由破损的搅拌器修复, 或用铸铁棒, 海棱水晶碎片和海蓝钢锭合成.

***

## <Color id="gold">更强的光束</Color>

搅拌机需要 10 AP. 更强的光束会让每个配方运行得更快: 其速度是(光束 ÷ 10)的平方根.

| 光束 | 速度 |
|---|---|
| 10 AP | ×1 (正常) |
| 40 AP | ×2 |
| 90 AP | ×3 |
| 160 AP | ×4 |

配方表中的时间基于 10 AP 的光束.

关于该规则及其适用的每台机器, 参见[更强的光束](nautec:getting_started/stronger_beams.md).

<RecipeFor id="mixer"/>
