---
navigation:
  parent: example-setups/index.md
  icon: celestine_shard
  title: 天青石农场
categories:
  - example
---

# <a name="celestine-farm" /> 天青石农场

<ItemLink id="budding_celestine" />可以用<ItemLink id="breaker" />轻松自动采集, 也可搭配<ItemLink id="terminal" />.

破坏器应将破坏筛选器设为`#c:clusters`

![破坏器界面, 已将晶簇设为破坏筛选条件](../assets/images/breaker_clusters.png)

<GameScene zoom="4" interactive={true} paddingLeft="30" paddingRight="30">
  <ImportStructure src="../assets/assemblies/celestine_farm.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
</GameScene>

也可选用聚焦节点将各部分相连.

<GameScene zoom="4" interactive={true} paddingLeft="30" paddingRight="30">
  <ImportStructure src="../assets/assemblies/celestine_farm_focus_node.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
</GameScene>

在破坏器界面中将红石模式设为低电平, 使其
无需红石信号即可持续启用. 将各破坏器的目标设为<ItemLink id="celestine_cluster" />.

它们会破坏成熟天青石簇, 将产物送入[网络存储](../nodeworks-mechanics/network-storage.md).
