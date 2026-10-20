---
navigation:
  parent: items-blocks/index.md
  icon: redstone_card
  title: 红石卡
categories:
  - card
description: reads and writes redstone signals at the installed node face
item_ids:
- nodeworks:redstone_card
---

# <a name="redstone-card" /> 红石卡

读取并写入安装面上的红石信号.

<ItemImage scale="6" id="redstone_card" />

## <a name="installing-and-scripting" /> 安装与脚本编程

安装方式与<ItemLink id="io_card" />相同, 放入节点的侧面槽位.
具体步骤见[安装IO卡](./io_card.md#installing).
卡片读取和写入的都是 *该面* 的红石信号.

参阅[RedstoneCard脚本API](../lua-api/card-handle.md#redstone-card),
其接口与其他卡片不同.

## <a name="Channel" /> <a name="channel" /> 频道

红石卡界面中有频道选择器. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解频道
如何限制哪些脚本能够访问此卡.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="redstone_card" />
