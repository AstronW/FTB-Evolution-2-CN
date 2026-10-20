---
navigation:
  title: 传送机
  icon: ftbic:teleporter
  parent: utilities/index.md
  position: 1
item_ids:
  - ftbic:teleporter
---

# <Color id="gold">传送机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="teleporter" scale="2" />

  用于传送玩家的平台.按名称配对两台传送机,为其中一台接入MV及以上电力,站上去即可到达另一台.连接后还可用作2向物品和流体管道(见下文).
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">搭建方法</Color>
</Column>

1. 放置传送机并打开界面.
2. 设置其 **ID** ,即其他传送机看到的名称.
3. 选择是否 **公开** :公开传送机会出现在所有人的列表中,未公开的仅对所有者可见.
4. 从任意面接入 **HV电力** .传送机是完整的HV节点:既接受HV输入,也能输出HV,因此连接的任意一端都可充当电源或用电端.
5. 在另一台传送机的界面中,从列表选择目的地.如果对端没有指向其他目标,选定目的地后也会自动建立回程连接.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">能量消耗</Color>
</Column>

* **最低:** <Energy config="machines.teleporter_min_use" />(距离不超过16格).
* **最高:** <Energy config="machines.teleporter_max_use" />(距离达到或超过1,200格).
* 两个距离界限之间按线性计算.

目的地区块 **必须已加载** .目标较远时,应使用区块加载器预加载,否则传送会报错.

<ItemImage id="minecraft:air" scale="0.25"/>
***

只有传送机的 **所有者** 可重命名,删除或取消公开.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">物品与流体传输</Color>
</Column>

相连的两台传送机也构成双向管道.漏斗,管道,泵等能向方块输入物品或流体的设备均可连接任意一端.从一端输入的资源会送到另一端.

每台传送机针对每种资源各有两个内部缓存:

* **发送缓存** :9个槽位+16 000 mB流体储罐.外部管道,漏斗和导管向传送机输入的资源进入这里.
* **接收缓存** :9个槽位+16 000 mB流体储罐.外部管道从传送机抽取的资源来自这里.

每隔几个游戏刻,传送机便将发送缓存传入对端的接收缓存.两端都会进行,因此同一对传送机可同时双向运输.每端每次传输上限约为8个物品和2 000 mB流体.

所有外部存取均通过这两个内部缓存进行,因此任意模组中能向物品栏推入资源的管道或导管,都可填充发送缓存;能抽取资源的设备都可排出接收缓存,无需特别兼容.

传送机的物品接口将发送槽标记为"仅插入",接收槽标记为"仅抽取",因此多数模组的自动检测无需额外配置即可正确传输.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">传输耗能与供电</Color>
</Column>

通过连接运输资源会在 **发送端** 产生少量待机耗能,不按物品逐个计费,而是在有流量时每秒收取一次.上一秒没有运输时便停止耗能.

两端 **以100%效率共享电力** :每隔几个游戏刻,两端缓存会平衡至相同充能比例,因此为任意一端供电,另一端也能立即使用.两台传送机都可向相连线缆网络 **输出HV电力** .常见用法是在发电区和采石场或机器区各放一台,再将远端连接至机器电网.电力按需双向流动,跨维度也有效.

传送机会从彼此的主动供电网络中排除,因此将同一对传送机连到同一段线缆上,不会造成往返循环.两端的传输由平衡机制处理,其他传输由线缆网络处理.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">清空按钮</Color>
</Column>

对端不可用时(未连接,对端区块未加载或缓存已满),资源会积压在发送缓存中.界面有两个按钮可处理:

* **清空物品** :将当前传送机发送槽中的全部物品移入自己的接收槽,便于普通抽取管道从接收侧取回.
* **清空流体** :对流体储罐执行相同操作.

拆除方块时,其内部物品会掉落到世界中,因此搬走尚有物品的传送机不会丢失这些物品.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">跨维度管道</Color>
</Column>

物品和流体传输与玩家传送一样支持跨维度.传输活动期间,对端区块会 **自动强制加载** ,无需额外放置区块加载器.停止运输约一分钟后会释放区块.
