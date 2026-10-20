---
navigation:
  parent: items-blocks/index.md
  icon: import_chest
  title: 输入箱
categories:
  - infrastructure
description: pushes items into network storage from its inventory
item_ids:
- nodeworks:import_chest
---

# <a name="import-chest" /> 输入箱

具有9个槽位, 会自动将放入的物品推送至
[网络存储](../nodeworks-mechanics/network-storage.md). 可以手动投入物品,
或使用漏斗, 其他模组的管道输入, 箱子随后
会自动将物品送进网络.

<GameScene zoom="6">
  <ImportStructure src="../assets/assemblies/import_chest.snbt" />
</GameScene>

无法接收的物品(因过滤, 空间不足等)会留在箱内,
便于查看堵塞原因.

## <a name="Channel" /> <a name="channel" /> 频道

在界面中设置频道, 可将推送限制为该
频道上的存储卡. 默认向网络中的所有存储卡推送. 另见
[选择频道](../lua-api/channel.md#choosing-a-channel).

## <a name="round-robin" /> 轮询

在界面中开启轮询, 可将输入分散到各目标
存储卡, 而非始终先填满第一张, 适合在多个存储
目标之间平衡负载.

## <a name="tick-interval" /> 工作间隔

界面可设置箱子尝试输入的频率, 默认每秒
一次. 降低间隔可加快接收, 但会增加网络负担;
低频工作场景可提高间隔.

## <a name="Redstone" /> <a name="redstone" /> 红石

界面中的红石设置控制箱子何时运行:

- **高电平** : 有红石信号时工作.
- **低电平** : 无红石信号时工作.
- **忽略** : 不受红石信号影响.

## <a name="Wireless" /> <a name="wireless" /> 无线传输

将<ItemLink id="receiver_antenna" />放在箱子顶部,
与另一网络中放在以下方块上的<ItemLink id="broadcast_antenna" />配对:
<ItemLink id="export_chest" />. 输入广播端输出箱的物品
会送达此箱子, 再像普通输入物品一样
进入本地网络存储.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="import_chest" />
