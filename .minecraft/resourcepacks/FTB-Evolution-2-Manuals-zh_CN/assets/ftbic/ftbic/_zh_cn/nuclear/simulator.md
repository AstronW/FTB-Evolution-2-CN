---
navigation:
  title: 反应堆模拟器
  icon: ftbic:reactor_simulator
  parent: nuclear/index.md
  position: 10
item_ids:
  - ftbic:reactor_simulator
---

# <Color id="gold">反应堆模拟器</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="reactor_simulator" scale="2" />

  核反应堆设计工作台.将元件放入网格,以最高1000倍速度模拟,在世界中搭建实际反应堆前了解其热量变化.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">使用方法</Color>
</Column>

1. 放置模拟器并打开界面.
2. 用反应仓调节按钮选择实际设计的反应仓数量(0至6个,对应解锁3至9列).
3. 用水冷调节按钮设置反应堆外壳与水接触的比例,与实际反应堆的环境冷却倍率相对应.
4. 向网格中放入虚拟元件.可从元件选择器或JEI拖入,右击槽位清除.这些操作不消耗实际物品.
5. 点击 **分析** 快速判定.模拟器会复制当前设计,模拟燃料棒的完整寿命,并报告 **稳定** 或 **在第N周期过热** .
6. 点击 **开始** 运行实时模拟,通过速度栏选择20倍/100倍/500倍/1000倍.每刻功率,累计发电量和已运行周期实时更新.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">控制按钮</Color>
</Column>

* **开始** :开始或继续模拟.
* **暂停** :中途冻结模拟,槽位恢复可编辑状态,运行计数保持不变.
* **重置** :清空所有槽位和计数,整张设计板恢复空白.
* **重新开始** :从周期0重新运行当前设计,燃料棒和冷却单元恢复满耐久.
* **分析** :在后台检查燃料棒完整寿命,不改变实时模拟计数.

模拟正在运行且未暂停时,槽位锁定,反应仓和水冷调节按钮禁用.请先暂停再编辑.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">分享设计</Color>
</Column>

* **导出** 将当前设计的JSON描述复制至剪贴板,可粘贴到聊天或保存为笔记文件.
* **导入** 读取剪贴板中的JSON并载入模拟器.

用[反应堆蓝图](blueprint.md)将布局带到实际反应堆,或分享给其他玩家.在物品栏中保留空白蓝图,点击 **写入蓝图** .反应堆也可通过 **加载预设** 载入保存的预设,或用 **粘贴设计** 载入导出的布局.

<ItemImage id="minecraft:air" scale="0.25"/>
***

模拟器无需供电,可以多做几台与朋友分享.等到在基地中搭建真实反应堆时,你已经知道它将如何运行.
