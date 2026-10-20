---
navigation:
  parent: items-blocks/index.md
  icon: placer
  title: 放置器
categories:
  - device
description: a shared network placer
item_ids:
- nodeworks:placer
---

# <a name="placer-block" /> 放置器

放置器会将可放置方块的物品放到正前方.
脚本可以通过物品ID指定放置内容, 或传入
[ItemsHandle](../lua-api/items-handle.md). 匹配物品随后
从[网络存储](../nodeworks-mechanics/network-storage.md)取出并放置.
操作为同步执行, 脚本会在发起请求的同一游戏刻得到`true`/`false`.

<BlockImage scale="6" id="placer" />

## <a name="Placing" /> <a name="placing" /> 放置

放置器放下时, 正面朝向你当时瞄准的位置,
与活塞或发射器相同. 放置出的方块
位于正面前方. 仅支持具有方块形态的物品,
工具, 食物和其他杂项物品都会导致放置调用失败.

## <a name="block-filter" /> 方块过滤

放置器界面有一个槽位, 用于指定要放置的方块.
每次放置器启动时, 会从
[网络存储](../nodeworks-mechanics/network-storage.md)取出匹配
物品. 留空则保持空闲, 直至脚本请求
具体物品.

## <a name="Redstone" /> <a name="redstone" /> 红石

界面中的红石设置控制放置器何时允许启动:

- **高电平** : 有红石信号时工作.
- **低电平** : 无红石信号时工作.
- **忽略** : 不受红石信号影响, 仅在脚本
  调用时启动.

## <a name="Channel" /> <a name="channel" /> 频道

放置器界面可设置名称和频道. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解
频道如何限制哪些脚本能够访问此设备.

## <a name="Scripting" /> <a name="scripting" /> 脚本编程

脚本API见[PlacerHandle](../lua-api/placer-handle.md)页面.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="placer" />
