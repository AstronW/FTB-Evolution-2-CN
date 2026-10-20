---
navigation:
  title: 数据中心
  icon: hostilenetworks:data_center
  position: 1
  parent: index.md
item_ids:
  - hostilenetworks:data_center
  - hostilenetworks:data_center_io_port
---

<Column alignItems="center" fullWidth={true}>
  # <Color id="gold">数据中心</Color>

  <ItemImage id="hostilenetworks:data_center" scale="2"/>

  最多可同时运行25个自我意识级数据模型,也是本整合包中唯一能让数据模型产出物品的设备.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">外壳结构</Color>
</Column>

<Column alignItems="center" fullWidth={true}>
  <GameScene zoom="2" interactive={true} background="#333333">
    <ImportStructure src="data_center.nbt"/>
    <IsometricCamera yaw="-45" pitch="30"/>
    <BoxAnnotation min="1 1 1" max="6 6 6" color="#ff5555">
      内部5x5x5空间必须全部为空气.
    </BoxAnnotation>
    <BlockAnnotation x="3" y="1" z="6" color="#ffaa00">
      控制器必须朝向外壳的 **外侧** .
    </BlockAnnotation>
    <BlockAnnotation x="5" y="1" z="6" color="#55ffff">
      IO端口为可选部件,可以替换墙壁或顶面的任意方块.
    </BlockAnnotation>
  </GameScene>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

* 外壳尺寸为7x7x7,底面使用<ItemLink id="minecraft:obsidian"/>(黑曜石标签内的任意方块均可).
* 墙壁和顶面使用<ItemLink id="minecraft:black_stained_glass"/>或<ItemLink id="hostilenetworks:data_center_io_port"/>.
* 用<ItemLink id="hostilenetworks:data_center"/>替换底面上一层的墙壁方块,并朝向外侧.同一层墙壁上的任何位置都可以,包括拐角.
* 外壳不符合要求时,控制器屏幕会列出缺失的方块及其坐标.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">运行模型</Color>
</Column>

* 将自我意识级模型放入5x5网格,不接受较低等级的模型.
* 在四个输入槽中放入<ItemLink id="hostilenetworks:prediction_matrix"/>.每个模型每轮消耗一个.
* <Color id="red">右击模型槽位,选择它要生产的物品.</Color>未选择产物的模型不会运行.<Color id="aqua">固定</Color>模式重复生产一种掉落物;<Color id="aqua">队列</Color>模式按列表依次生产.
* 每轮耗时15秒,产出模型对应的<Color id="green">通用预测产物</Color>和一种选定掉落物,存入16槽的输出缓存.
* 每个模型每刻耗能为其模拟耗能再加25%.能量缓存容量为20,000,000 FE.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">IO端口</Color>
</Column>

<Row>
  <ItemImage id="hostilenetworks:data_center_io_port"/>
  ### <Color id="aqua">数据中心IO端口</Color>
</Row>

控制器本身即可输入能量和物品.借助端口,管道和线缆可以从外壳的其他面连接数据中心.右击端口可循环切换模式.

| 模式 | 连接目标 |
|---|---|
| <Color id="aqua">能量</Color> | 能量缓存 |
| <Color id="aqua">模型</Color> | 5x5模型网格 |
| <Color id="aqua">输入</Color> | 四个输入槽 |
| <Color id="aqua">输出</Color> | 输出缓存,仅可抽取 |

每个端口一次只能使用一种模式,可按需放置多个端口.
