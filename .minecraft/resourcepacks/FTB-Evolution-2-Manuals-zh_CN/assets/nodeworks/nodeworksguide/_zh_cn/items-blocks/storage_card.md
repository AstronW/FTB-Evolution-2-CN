---
navigation:
  parent: items-blocks/index.md
  icon: storage_card
  title: 存储卡
categories:
  - card
description: marks the adjacent block as part of network storage
item_ids:
- nodeworks:storage_card
---

# <a name="storage-card" /> 存储卡

存储卡将相邻方块纳入[网络存储](../nodeworks-mechanics/network-storage.md), 即网络
查询, 路由写入和物品终端所使用的共享
物品池.

<ItemImage scale="6" id="storage_card" />

## <a name="Configuration" /> <a name="configuration" /> <a name="configuring-priority" /> 配置

手持 **存储卡** 右击, 可设置优先级, 频道
和过滤器.

![](../assets/images/storage-card-gui.png)

> **提示:** 使用<ItemLink id="card_programmer" />复制卡片设置,
> 还可选择同时复制名称和频道, 便于通过模板
> 批量配置卡片.
> 
> 也可使用[`network:route()`](../lua-api/network.md#route)批量设置卡片,
> 完全无需逐张操作.

## <a name="target-face" /> 目标侧面

可以选择卡片访问相邻方块的哪一面.
默认使用节点所朝向的面, 一般无需更改.
对于具有侧面专用槽位的设备则可覆盖此设置,
例如熔炉顶部接收原料, 侧面接收燃料,
底部输出产物.

## <a name="Channel" /> <a name="channel" /> 频道

存储卡界面中也有频道选择器. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解频道
如何限制哪些脚本, 路由规则和预设能够访问此卡.

## <a name="Filters" /> <a name="filters" /> 过滤器

每张存储卡都可配置为仅接收指定物品, 使具有
多张卡的网络将输入物品送到正确位置. 新卡
没有过滤规则, 默认接受全部物品.

### <a name="Mode" /> <a name="mode" /> 模式

存储卡界面的 **模式** 开关可切换规则列表的含义:

- **允许** : 仅接受匹配至少一条规则的物品
- **拒绝** : 拒绝匹配至少一条规则的物品, 其余通过

没有规则时, 模式不起作用, 但下面的 **可堆叠性** 和
**NBT** 过滤仍会叠加生效. 只有三个过滤器都保持
默认值(无规则, 任意可堆叠性, 任意NBT)时才接受全部物品.

### <a name="Rules" /> <a name="rules" /> 规则

每条规则是一行过滤语法, 针对尝试
进入卡片的物品进行匹配:

| 语法 | 匹配内容 |
| ----------------------- | ---------------------------------------------- |
| `minecraft:cobblestone` | 准确物品ID |
| `#minecraft:logs` | 此标签中的全部物品 |
| `minecraft:*` | 此模组/命名空间中的全部物品 |
| `/^.*_ore$/` | ID匹配此正则表达式的物品 |
| `*` | 全部物品/流体 |

有三种添加规则的方式:

1. 点击列表底部的 **[+添加规则]** , 在新行中输入.
输入过程中, 自动补全会建议物品ID和标签.
2. 从JEI拖入任意物品到规则列表, 将其ID作为新规则.
3. 在脚本终端中使用[`network:route()`](../lua-api/network.md#route),
一次为多张卡片设置规则.

### <a name="stackability-and-nbt" /> 可堆叠性与NBT

另外两个开关可在规则列表的基础上进一步缩小接收范围:

- **可堆叠性** : 在 **任意** / **仅可堆叠** / **仅不可堆叠** 间循环.
适合将工具和护甲与大宗资源分开, 无需列出所有物品ID.
- **NBT** : 在 **任意** / **有数据** / **无数据** 间循环.
有NBT的物品, 如受损工具, 命名物品和附魔书, 可与
无特殊数据的版本分开.

这三项设置共同生效. 物品必须同时满足
可堆叠性, NBT和规则列表才会进入卡片. 例如某卡设置为
`Mode: Allow`, `Stackability: Stackable only`, `NBT: No data`, 再加上规则
`#minecraft:swords`, 实际上不会接受任何物品. 剑无法堆叠,
因此在检查规则列表前, 就会被可堆叠性
条件拒绝. 请选择彼此相容的设置.

### <a name="Examples" /> <a name="examples" /> 示例

**大宗圆石存储**

> **模式:** 允许
> 
> **可堆叠性:** 任意
> 
> **NBT:** 任意
> 
> **规则:** #c:cobblestone

接受`#c:cobblestones`标签中的任意圆石.

**仅不可堆叠物品**

> **模式:** 允许
> 
> **可堆叠性:** 仅不可堆叠
> 
> **NBT:** 任意
> 
> **规则:** *留空*

仅接收不可堆叠物品的存储卡无需设置任何规则.

## <a name="installation-and-scripting" /> 安装与脚本编程

安装方式与<ItemLink id="io_card" />相同. 放入接触目标方块的
节点侧面槽位. 脚本API与IO卡相同,
完整方法见[CardHandle](../lua-api/card-handle.md#inventory-cards).

## <a name="the-difference-from-io" /> 与IO卡的区别

<ItemLink id="io_card" />对应的方块是脚本控制的物品栏.
脚本必须显式移动其中的物品. 存储卡则将
方块 *纳入* 网络共享存储池: `network:find`能够查询它,
<ItemLink id="inventory_terminal" />和<ItemLink id="portable_inventory_terminal" />会列出其中的物品, 合成配方也会
自动从中取用原料.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="storage_card" />
