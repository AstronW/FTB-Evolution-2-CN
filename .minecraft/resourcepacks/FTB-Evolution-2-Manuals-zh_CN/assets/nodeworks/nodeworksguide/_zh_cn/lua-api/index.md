---
navigation:
  title: Nodeworks脚本API
  position: 40
---

# <a name="nodeworks-scripting-api" /> Nodeworks脚本API

<BlockImage scale="6" id="terminal" float="left" />

Nodeworks使用[Lua](https://www.lua.org/docs.html)编写脚本,
编辑器会在运行前处理一些便利扩展:

- **类型注解:** 如`local x: CardHandle`, `function(xs: { CardHandle }): ItemsHandle`等.
  - 告诉编辑器变量, 参数或返回值的类型, 从而获得准确悬停提示, 更好的自动补全和循环中的元素类型推断.

## <a name="built-ins" /> 内置对象

<CategoryIndexDescriptions category="api_builtin" />

- [clock()](): 脚本开始运行以来经过的秒数, 包含小数
- [print(...)](): 向终端输出日志
- [require(name)](): 按名称加载同一终端中的另一个脚本标签页

## <a name="Presets" /> <a name="presets" /> 预设

声明式构建器, 将常见调度循环封装成一行链式调用.
通用用法见[预设](presets.md).

<CategoryIndexDescriptions category="api_preset" />

## <a name="Types" /> <a name="types" /> 类型

<CategoryIndexDescriptions category="api_types" />
