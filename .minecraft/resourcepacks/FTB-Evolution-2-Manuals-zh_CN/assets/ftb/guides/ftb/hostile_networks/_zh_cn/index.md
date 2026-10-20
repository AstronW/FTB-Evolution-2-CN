---
navigation:
  title: 敌对生物网络
  icon: hostilenetworks:deep_learner
  position: 0
item_ids:
  - hostilenetworks:deep_learner
  - hostilenetworks:blank_data_model
  - hostilenetworks:sim_chamber
  - hostilenetworks:prediction_matrix
---

<Column alignItems="center" fullWidth={true}>
  # <Color id="gold">敌对生物网络</Color>

  <ItemImage id="hostilenetworks:deep_learner" scale="2"/>

  让数据模型学习生物的战斗方式或矿石的形成规律,再让数据中心将这些知识转化为掉落物和矿产.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">基本流程</Color>
</Column>

1. 手持<ItemLink id="hostilenetworks:blank_data_model"/>右击生物或矿石方块,将模型与其绑定.只有具有模型的生物和矿石才可绑定;本整合包新增的种类见[数据模型](data_models.md).
2. 将模型放入<ItemLink id="hostilenetworks:deep_learner"/>(4个槽位).只要学习者位于主物品栏,副手或Curios饰品栏中,就会记录数据.
3. 击杀对应生物,或不用精准采集挖掘对应矿石.每次击杀或挖矿,都会为学习者内所有匹配的模型增加数据.
4. 模型达到<Color id="green">基础</Color>级(6数据)后,即可放入<ItemLink id="hostilenetworks:sim_chamber"/>继续训练,无需战斗.模拟室不接受缺陷级模型.
5. 模型达到<Color id="gold">自我意识</Color>级后,将其移入[数据中心](data_center.md).数据中心才是产出资源的地方.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">模型等级</Color>
</Column>

| 等级 | 所需数据 | 每次击杀或挖矿获得的数据 |
|---|:---:|:---:|
| <Color id="dark_gray">缺陷</Color> | 0 | 1 |
| <Color id="green">基础</Color> | 6 | 4 |
| <Color id="blue">高级</Color> | 54 | 10 |
| <Color id="light_purple">超级</Color> | 354 | 18 |
| <Color id="gold">自我意识</Color> | 1,254 | 已满级 |

首领与普通生物使用同一张等级表.模型的悬停提示会显示还需击杀多少次.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">模拟室</Color>
</Column>

<Row>
  <ItemImage id="hostilenetworks:sim_chamber"/>
  ### <Color id="aqua">仅供训练</Color>
</Row>

在FTB Evolution 2中,模拟室固定为<Color id="aqua">训练</Color>模式,无法切换.每轮运行耗时15秒,消耗一个<ItemLink id="hostilenetworks:prediction_matrix"/>,为模型增加1数据,但不产出物品.每刻耗能为模型模拟耗能再加20%.

单靠训练速度很慢:基础级模型还需运行1,248轮,约5.2小时,才能达到自我意识级.带着深度学习者击杀或挖矿会更快.模型达到自我意识级后,模拟室便会停止.

> <Color id="yellow">注意</Color>:本整合包禁用了战利品制造机和制造指令单.数据中心直接配置自身的产物.
