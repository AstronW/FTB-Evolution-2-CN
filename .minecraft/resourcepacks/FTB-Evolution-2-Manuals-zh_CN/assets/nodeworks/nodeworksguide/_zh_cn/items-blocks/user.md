---
navigation:
  parent: items-blocks/index.md
  icon: user
  title: 使用器
categories:
  - device
description: right-clicks with an item on the block in front of it
item_ids:
- nodeworks:user
---

# <a name="user-block" /> 使用器

使用器从
[网络存储](../nodeworks-mechanics/network-storage.md)取出物品, 并用它
右击方块正前方的目标. 可用于
给作物施骨粉, 刷扫可疑方块, 用打火石点燃TNT,
用桶装取流体, 或执行其他通常需要玩家
手动完成的操作.

<BlockImage scale="6" id="user" />

## <a name="Placing" /> <a name="placing" /> 放置

使用器放下时, 正面朝向你当时瞄准的位置,
与活塞或发射器相同. 它会寻找正前方两格内
的第一个非空气方块, 因此即使使用器与作物之间
隔着一格空气, 仍能操作作物.

## <a name="item-filter" /> 物品过滤

使用器界面有一个槽位, 用于指定所用物品.
每次启动时从网络存储取出匹配物品,
操作完成后返还. 过滤语法与
<ItemLink id="storage_card" />相同, 因此普通ID, 标签和通配符
均可使用.

## <a name="Mode" /> <a name="mode" /> 模式

使用器具有两种模式:

- **立即** : 每次启动执行一次右击, 适合施骨粉
  或使用打火石等单次操作.
- **按住** : 跨游戏刻持续按住右键, 直至释放.
  适合刷子等需要持续使用的工具. 按住30秒后会自动释放.

## <a name="Redstone" /> <a name="redstone" /> 红石

界面中的红石设置控制使用器何时允许启动:

- **高电平** : 有红石信号时工作.
- **低电平** : 无红石信号时工作.
- **忽略** : 不受红石信号影响, 仅在脚本
  调用时启动.

## <a name="Channel" /> <a name="channel" /> 频道

使用器界面可设置名称和频道. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解
频道如何限制哪些脚本能够访问此设备.

## <a name="Scripting" /> <a name="scripting" /> 脚本编程

脚本API见[UserHandle](../lua-api/user-handle.md)页面.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="user" />
