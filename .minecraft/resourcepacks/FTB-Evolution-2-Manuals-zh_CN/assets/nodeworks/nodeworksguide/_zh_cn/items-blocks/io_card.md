---
navigation:
  parent: items-blocks/index.md
  icon: io_card
  title: IO卡
categories:
  - card
  - requires_controller
description: used for reading and writing an inventory/tank from scripts
item_ids:
- nodeworks:io_card
---

# <a name="io-card" /> IO卡

IO卡允许网络按需读写相邻方块的
物品栏. 安装IO卡后, 脚本可查询方块内的
物品, 并向其中输入或取出物品与流体.

> 要在脚本中使用 IO卡, 必须先有一个<ItemLink id="network_controller" />

<ItemImage scale="6" id="io_card" />

## <a name="Installing" /> <a name="installing" /> 安装

IO卡安装在<ItemLink id="node" />的侧面槽位中. 右击
与目标方块相接的节点面, 将
IO卡放入9个槽位之一. 卡片只影响 *该面* ,
因此同一节点的不同面可以安装IO卡, 分别控制
不同的相邻方块.

![](../assets/images/node_gui.png)

## <a name="what-it-does" /> 功能

装有IO卡的方块会以可由脚本访问的物品栏
形式出现在网络中:

- `card:find(filter)`返回包含匹配内容的[ItemsHandle](../lua-api/items-handle.md)
  句柄.
- `card:insert(items)`/`card:tryInsert(items)`向其中移动物品.
- `card:count(filter)`统计匹配物品的总量(流体以mB计).

与<ItemLink id="storage_card" />不同, IO卡对应的方块 **不属于**
[网络存储](../nodeworks-mechanics/network-storage.md). 脚本必须显式地向其中输入或取出物品,
全网络查询`network:find`不会看到其中的内容,
<ItemLink id="inventory_terminal" />和<ItemLink id="portable_inventory_terminal" />也不会列出它们.

## <a name="Channel" /> <a name="channel" /> 频道

IO卡界面中有频道选择器. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解频道
如何限制哪些脚本和预设能够访问此卡.

## <a name="Scripting" /> <a name="scripting" /> 脚本编程

IO卡句柄可用的全部方法见[CardHandle参考](../lua-api/card-handle.md#inventory-cards)
页面.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="io_card" />
