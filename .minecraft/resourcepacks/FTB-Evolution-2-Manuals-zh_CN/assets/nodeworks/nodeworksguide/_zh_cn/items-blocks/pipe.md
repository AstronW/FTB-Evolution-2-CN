---
navigation:
  parent: items-blocks/index.md
  icon: pipe
  title: 真空管道
categories:
  - infrastructure
description: the building block of every network
item_ids:
- nodeworks:pipe
- nodeworks:covered_pipe
---

# <a name="vacuum-pipe" /> 真空管道

Nodeworks网络的线路. 管道在所有网络方块之间
传输物品, 信号和路由信息.

<GameScene interactive={true} zoom="5" paddingLeft="20" paddingTop="20" paddingBottom="20">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="../assets/assemblies/vacuum_pipe.snbt" />
</GameScene>

将管道相邻放置, 或紧贴其他网络方块,
便会自动连接.

## <a name="hiding-pipes" /> 隐藏管道

### <a name="covered-pipes" /> 包覆管道

可用包覆管道隐藏线路: 在工作台中用一个方块
和围绕它的8根真空管道合成.

<GameScene interactive={true} zoom="5" paddingLeft="20" paddingTop="20" paddingBottom="20">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="../assets/assemblies/covered_pipe.snbt" />
</GameScene>

### <a name="focus-nodes" /> 聚焦节点

也可用<ItemLink id="focus_node" />穿过玻璃建立连接, 以此穿越墙体.

<GameScene interactive={true} zoom="5" paddingLeft="20" paddingTop="20" paddingBottom="20">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="../assets/assemblies/focus_node_glass.snbt" />
</GameScene>

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="pipe" />
