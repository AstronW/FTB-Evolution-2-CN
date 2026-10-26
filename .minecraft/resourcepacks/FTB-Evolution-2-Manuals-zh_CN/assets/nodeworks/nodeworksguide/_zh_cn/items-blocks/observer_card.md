---
navigation:
  parent: items-blocks/index.md
  icon: observer_card
  title: 侦测卡
categories:
  - card
  - requires_controller
description: reads the block at the installed node face, id, properties, and change events
item_ids:
- nodeworks:observer_card
---

# <a name="observer-card" /> 侦测卡

读取安装面前方的方块, 提供方块ID, 全部状态
属性(生长`age`, `facing`, `waterlogged`, `lit`等),
以及变化回调, 以便脚本在方块切换到目标
状态时立即响应.

> 要在脚本中使用侦测卡, 需要<ItemLink id="network_controller" />才能使用<ItemLink id="terminal" />

<ItemImage scale="6" id="observer_card" />

## <a name="what-it&#x27;s-for" /> <a name="what-its-for" /> 用途

按生长阶段采收的农场是典型用途. 与原版侦测器
相连的活塞会在每次生长变化时动作, 可能提前打碎小晶芽,
只得到1个碎片, 而不是等到完整晶簇的4个. 使用侦测卡后,
脚本可以读取实际阶段, 只在方块长成最终形态时
触发破坏器.

它也适合读取红石信号以外的状态: 活板门
开关, 门状态, 蜂巢蜂蜜等级, 滴水石填充程度, 阳光
传感器读数, 甜浆果/海带/甘蔗生长, 方块下方
结冰或积雪等, 只要有可比较的`BlockState`属性即可.

## <a name="installing-and-scripting" /> 安装与脚本编程

安装方式与<ItemLink id="io_card" />相同, 放入节点某个面.
具体步骤见[安装IO卡](./io_card.md#installing).
卡片读取 *该面* 正前方的方块.

它提供的方法见[ObserverCard脚本API](../lua-api/card-handle.md#observer-card)
页面.

## <a name="Channel" /> <a name="channel" /> 频道

侦测卡界面中有频道选择器. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解频道
如何限制哪些脚本能够访问此卡.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="observer_card" />
