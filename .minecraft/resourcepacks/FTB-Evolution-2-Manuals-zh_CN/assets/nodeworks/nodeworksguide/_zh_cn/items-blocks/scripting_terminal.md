---
navigation:
  parent: items-blocks/index.md
  icon: terminal
  title: 脚本终端
categories:
  - terminal
  - requires_controller
description: where you write and run Lua scripts that control a network
item_ids:
- nodeworks:terminal
---

# <a name="scripting-terminal" /> 脚本终端

脚本终端用于编写和运行控制网络的Lua脚本.

> 需要<ItemLink id="network_controller" />才能使用

<BlockImage scale="6" id="terminal" />

## <a name="opening-the-editor" /> 打开编辑器

右击终端打开编辑器, 其中有三个面板:

- **侧栏** 列出网络中的所有卡片和变量. 点击即可在光标处插入
  一行`network:get("…")`.
- **脚本标签页** 包括`main`及自行创建的模块. 点击开始时运行`main`,
  其他标签页通过[`require(name)`](../lua-api/index.md)加载.
- **输出面板** 显示`print(…)`输出和脚本错误.
  - 可点击左侧箭头展开/收起输出, 或拖动分隔条调整大小.

![](../assets/images/terminal_gui.png)

## <a name="running-scripts" /> 运行脚本

(另见[脚本API](../lua-api/index.md)参考, 其中列出脚本的所有
功能, 包括网络查询, 合成, 调度回调和变量.)

点击开始, 加载并运行当前`main`标签页. `main`执行结束
后脚本便退出, 除非注册了回调以保持运行. 点击停止可结束
脚本.

### <a name="AutoRun" /> <a name="autorun" /> 自动运行

在编辑器中开启自动运行, 终端加载时便会自动启动脚本.
终端仅在所在区块加载时加载, 因此自动运行
不等于"服务器在线就一直运行". 玩家需要靠近
以加载区块, 或在网络的<ItemLink id="network_controller" />
中开启区块加载, 使附近没有玩家时也能
保持加载.

![](../assets/images/autorun.png)

### <a name="Redstone" /> <a name="redstone" /> 红石

终端收到红石脉冲时会切换脚本状态. 脚本停止时
脉冲会启动它, 已在运行时则停止它. 任意上升沿
均有效, 例如按钮, 压力板或新放置的红石火把.

> 脚本因实际运行时间超限而终止后, 红石无法重新启动,
> 直到你打开编辑器并编辑脚本. 这样可以防止红石时钟
> 对行为异常的终端反复触发
> 同一个故障脚本.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="terminal" />
