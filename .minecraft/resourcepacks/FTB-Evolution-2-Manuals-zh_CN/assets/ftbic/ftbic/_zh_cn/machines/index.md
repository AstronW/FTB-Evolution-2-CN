---
navigation:
  title: 机器
  icon: ftbic:macerator
  position: 30
---

# <Color id="gold">机器</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="macerator" scale="2" />

  FTB工业奇械的配方加工机器具有物品栏,配方处理循环,能量缓存及最多四个 **升级** 槽.高级版本的缓存更大,吞吐量更高.批次供料器等实用机器则有各自的控制方式.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">机器通用功能</Color>
</Column>

配方加工机器共有以下功能:

* **能量缓存** :显示在界面右侧
* **进度条** :随配方处理逐步填满,默认每配方200游戏刻
* **升级槽** :可安装<ItemLink id="overclocker_upgrade" />,<ItemLink id="energy_storage_upgrade" />,<ItemLink id="transformer_upgrade" />或<ItemLink id="ejector_upgrade" />
* **[侧面配置](side_configuration.md)** :通过I/O按钮分别设置物品,流体和能量的传输面
* **[输入槽锁定](side_configuration.md)** :通过L按钮设置持久保存的虚拟物品过滤

所有LV机器都以<ItemLink id="machine_block" />为外壳,配合对应的核心原料(例如打粉机需要<ItemLink id="electronic_circuit" />,燧石和石头).

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">分节</Color>
</Column>

<SubPages icons={true} />
