---
navigation:
  title: 泵
  icon: ftbic:pump
  parent: machines/index.md
  position: 11
item_ids:
  - ftbic:pump
  - ftbic:exfluid
---

# <Color id="gold">泵</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="pump" scale="2" />

  可自动向下延伸的流体开采设备.垂直放下管道,抽取遇到的熔岩,水或模组流体,并存入内部128桶容量的储罐.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="pump" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">运行方法</Color>
</Column>

* 放在方块上方.泵的管道会穿过空气和可替换方块向下延伸,直到遇见流体.
* 开采一个流体方块需要40游戏刻,管道向下移动一格需要10游戏刻.
* 默认情况下,抽走的流体被<ItemLink id="exfluid" />替换,以防利用无限流体源.如希望留下空洞,可在配置中禁用此功能.
* 从侧面连接管道或<ItemLink id="fluid_cell" />,将流体导出.

**参数:** HV级,缓存320,000 FE,耗能24 FE/t.
