---
navigation:
  parent: items-blocks/index.md
  icon: export_chest
  title: 输出箱
categories:
  - infrastructure
description: pulls items from network storage into its inventory
item_ids:
- nodeworks:export_chest
---

# <a name="export-chest" /> 输出箱

具有9个槽位, 自动从
[网络存储](../nodeworks-mechanics/network-storage.md)抽取物品到
自身缓存中.

<GameScene zoom="6">
  <ImportStructure src="../assets/assemblies/export_chest.snbt" />
</GameScene>

## <a name="Filter" /> <a name="filter" /> 过滤

界面支持输入一组过滤规则, 语法与
<ItemLink id="storage_card" />相同. 匹配任一规则的物品
都可导出. 过滤列表为空时箱子保持空闲, 防止刚放下
就立即抽空网络.

## <a name="push-face" /> 推送面

在界面中选择一个面, 便可自动将缓存内容送入
该侧相邻物品栏. 无需脚本即可为漏斗, 熔炉或机器
供料. 留空则将缓存作为手动取货
位置.

## <a name="Channel" /> <a name="channel" /> 频道

设置频道可将抽取限制为该频道上的存储卡.
默认从网络中的所有存储卡抽取. 详见
[选择频道](../lua-api/channel.md#choosing-a-channel).

## <a name="Redstone" /> <a name="redstone" /> 红石

界面中的红石设置控制箱子何时运行:

- **高电平** : 有红石信号时工作.
- **低电平** : 无红石信号时工作.
- **忽略** : 不受红石信号影响.

## <a name="Wireless" /> <a name="wireless" /> 无线传输

在箱子顶部放置<ItemLink id="broadcast_antenna" />, 并与
另一网络中的<ItemLink id="receiver_antenna" />配对. 输入
此箱子的物品会直接转发至接收端
网络的存储中.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="export_chest" />
