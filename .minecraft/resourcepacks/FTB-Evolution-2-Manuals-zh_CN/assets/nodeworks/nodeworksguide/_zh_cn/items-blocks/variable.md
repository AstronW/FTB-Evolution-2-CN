---
navigation:
  parent: items-blocks/index.md
  icon: variable
  title: 变量
categories:
  - device
  - requires_controller
description: a shared network variable
item_ids:
- nodeworks:variable
---

# <a name="variable-block" /> 变量方块

变量方块保存一个可供整个网络共享的值.

> 需要<ItemLink id="network_controller" />才能使用.

<BlockImage scale="6" id="variable" />

## <a name="Configuration" /> <a name="configuration" /> 配置

将变量方块连接到网络后, 可以选择其 **类型** ,
并设置 **名称** . 二者都影响它在<ItemLink id="terminal" />中的显示.

![](../assets/images/variable_gui_count.png)

此例为名叫`count`的 **数字** 变量.

打开同一网络中的任意<ItemLink id="terminal" />, 就能在
侧栏看到并引用它.

![](../assets/images/variable_in_terminal.png)

### <a name="Types" /> <a name="types" /> 类型

- **number** (数字)
  - 数值, 可以是整数或小数
- **string** (字符串)
  - 最长256字符的文本
- **bool** (布尔值)
  - `true`或`false`

## <a name="Channel" /> <a name="channel" /> 频道

变量界面中也有频道选择器. 参阅
[选择频道](../lua-api/channel.md#choosing-a-channel), 了解频道
如何限制哪些脚本能够访问此变量.

## <a name="Scripting" /> <a name="scripting" /> 脚本编程

脚本API见[VariableHandle](../lua-api/variable-handle.md)页面.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="variable" />
