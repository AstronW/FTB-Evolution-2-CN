---
navigation:
  parent: nodeworks-mechanics/index.md
  title: 子网
  icon: broadcast_antenna
categories:
  - networking
  - mechanic
---

# <a name="Subnets" /> <a name="subnets" /> 子网

子网是通过无线方式将自身部分能力提供给
另一网络的独立网络. 每个子网都有自己的
<ItemLink id="network_controller" />, 独立存储和
合成系统, 并通过配对的
<ItemLink id="broadcast_antenna" />与
<ItemLink id="receiver_antenna" />同主网络通信.

<GameScene zoom="3" interactive={true} paddingTop="30" paddingLeft="50" paddingRight="50">
  <ImportStructure src="../assets/assemblies/subnet.snbt" />
</GameScene>

## <a name="why-split-a-network" /> 拆分网络的理由

小型基地使用单个网络即可. 随着机器与配方
数量增加, 拆分网络会成为方便的
组织方式:

- **专门化** : 用于烧炼, 酿造或矿石
  加工的子网, 可将对应配方与机器集中一处,
  而不是散布在主基地各处.
- **复用** : 搭建一次冶炼子网, 即可将其配方
  提供给你的所有基地.
- **隔离** : 某个子网的崩溃, 卡顿或卡住的合成任务
  不会影响其他部分. 每个网络独立运行CPU, 存储和
  脚本.
- **整洁** : 主网络只看到子网广播的配方,
  看不到后方的管道和机器.

## <a name="exposing-processing-recipes" /> 共享加工配方

最常见的子网结构是由一组
<ItemLink id="processing_storage" />保存
<ItemLink id="processing_set" />, 再广播这些配方, 以便
其他网络在自动合成时调用.

1. 在子网中搭建
   <ItemLink id="processing_storage" />集群, 放入子网
   应提供的<ItemLink id="processing_set" />.
2. 将<ItemLink id="broadcast_antenna" />直接放到集群中任意
   <ItemLink id="processing_storage" />顶部.
3. 在天线界面中用<ItemLink id="link_crystal" />完成配对.
4. 在接收网络中放置
   <ItemLink id="receiver_antenna" />并接入网络, 将
   同一颗<ItemLink id="link_crystal" />放入其界面.

接收网络随后能看到子网加工配方存储集群中的
全部配方, 就像本地配方一样. 需要这些配方的
任务可正常自动合成.

机器和原料仍由子网持有. 接收网络只负责
请求产物, 再由子网交付.

## <a name="wireless-item-transfer" /> 无线物品传输

子网也可直接交换物品: 将广播端的
<ItemLink id="export_chest" />与以下位置的
<ItemLink id="receiver_antenna" />配对:
<ItemLink id="import_chest" />顶部. 配对步骤见输出箱和接收
天线页面.

## <a name="Range" /> <a name="range" /> 范围

天线默认范围为128格. 范围升级可以扩展到
跨区块, 跨维度, 因此子网无需紧挨着
使用它的网络. 常见布局包括:

- 下界的冶炼子网向主世界的主基地供货.
- 刷怪场子网将掉落物广播至远处的分类基地.
- 提供通用配方的共享"配方库"子网, 供服务器中
  其他所有基地调用.
