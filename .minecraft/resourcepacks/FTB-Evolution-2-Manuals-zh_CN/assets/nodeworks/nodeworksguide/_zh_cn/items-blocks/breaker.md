---
navigation:
  parent: items-blocks/index.md
  icon: breaker
  title: 破坏器
categories:
  - device
description: mines and harvests blocks in front of it
item_ids:
- nodeworks:breaker
---

# <a name="breaker-block" /> 破坏器

破坏器会花费一定时间破坏正前方的方块,
并将掉落物送回
[网络存储](../nodeworks-mechanics/network-storage.md), 或交给
脚本指定的处理函数. 其开采等级相当于钻石镐, 破坏耗时则使用
木镐公式, 因此较硬的方块明显需要更长时间.

<BlockImage scale="6" id="breaker" />

## <a name="Placing" /> <a name="placing" /> 放置

放置破坏器时, 正面会朝向你当时瞄准的位置,
与活塞或发射器相同. 该面前方的方块
就是`:mine()`会破坏的目标.

## <a name="target-filter" /> 目标过滤

破坏器界面可过滤要破坏的方块. 留空时
可破坏前方的任意方块; 指定方块后则限制为
该目标.

## <a name="tree-felling" /> 伐木

将破坏器放在树根位置, 即可一次砍倒整棵树.

<GameScene zoom="4" paddingTop="30" paddingLeft="60" paddingRight="60" interactive={true} >
  <ImportStructure src="../assets/assemblies/breaker_tree_felling.snbt" />
  <BlockAnnotation x="2" y="1" z="2">
  破坏最后一块支撑树木的原木, 会使整棵树倒下.
  </BlockAnnotation>
  <RemoveBlocks id="minecraft:sandstone" />
  <RemoveBlocks id="minecraft:sandstone" />
</GameScene>

## <a name="Redstone" /> <a name="redstone" /> 红石

界面中的红石设置控制破坏器何时允许启动:

- **高电平** : 有红石信号时工作.
- **低电平** : 无红石信号时工作.
- **忽略** : 不受红石信号影响, 仅在脚本
  调用`:mine()`时启动.

## <a name="Channel" /> <a name="channel" /> 频道

破坏器界面可设置名称和频道. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解
频道如何限制哪些脚本能够访问此设备.

## <a name="Scripting" /> <a name="scripting" /> 脚本编程

破坏器的脚本API见[BreakerHandle](../lua-api/breaker-handle.md)页面.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="breaker" />
