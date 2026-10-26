---
navigation:
  parent: items-blocks/index.md
  icon: inventory_terminal
  title: 物品终端
categories:
  - terminal
description: a viewport into [Network Storage](../nodeworks-mechanics/network-storage.md)
item_ids:
- nodeworks:inventory_terminal
---

# <a name="inventory-terminal" /> 物品终端

物品终端是查看[网络存储](../nodeworks-mechanics/network-storage.md)的窗口.

<BlockImage scale="6" id="inventory_terminal" />

## <a name="browsing-the-grid" /> 浏览物品网格

![](../assets/images/inventory_terminal_gui_expanded.png)

- 左击拿取一组物品
- 右击拿取半组
- 双击将所有匹配物品收集到鼠标上
- 将鼠标拿着的一组物品放到网格上, 可存入[网络存储](../nodeworks-mechanics/network-storage.md)
- 拿着物品右击网格, 仅存入一个
- 按住`Alt`显示网络中可自动合成的物品

左侧按钮可以:

- 更改布局
- 对网格排序
- 筛选存储物品, 配方或两者
- 筛选物品, 流体或两者
- 切换搜索框自动获得焦点
- 切换终端与 JEI 搜索同步
- 按频道筛选显示

中央是可折叠的合成网格, 按钮功能包括:

- 从网络自动拉取原料
- 将原料均匀分配到合成网格中
- 将合成网格中的原料送回网络存储

Shift点击合成结果可合成一组并放入物品栏. `Ctrl`+Shift点击会尽可能合成, 直至装满.

## <a name="Recipes" /> <a name="recipes" /> 配方

<RecipeFor id="inventory_terminal" />
