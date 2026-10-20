---
navigation:
  parent: items-blocks/index.md
  icon: network_controller
  title: 网络控制器
categories:
  - infrastructure
description: the heart of a network, every network requires one
item_ids:
- nodeworks:network_controller
---

# <a name="network-controller" /> 网络控制器

每个Nodeworks网络必须恰好有一个控制器. 没有控制器时,
与其相连的[管道](pipe.md)和[节点](node.md)都会保持休眠.

<GameScene interactive={true} zoom="5">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="../assets/assemblies/controller_node_terminal.snbt" />
</GameScene>

放下控制器并从它引出管道, 连接到这些
管道的方块便会加入网络.

## <a name="Identity" /> <a name="identity" /> 网络标识

控制器界面可设置网络名称和颜色.
名称仅供显示, 颜色则影响节点的发光颜色, 便于区分
同一区域中的多个网络.

## <a name="chunk-loading" /> 区块加载

在界面中开启区块加载后, 网络经过的所有区块
都会保持强制加载. 适用于需要在你远离时
继续工作的自动合成系统.

## <a name="one-per-network" /> 每个网络仅限一个

两个控制器接入同一管道网络会发生冲突, 两个
网络都会停止, 直至移除其中一个控制器.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="network_controller" />
