---
navigation:
  title: 能源网络
  icon: ftbic:lv_cable
  position: 10
---

# <Color id="gold">能源网络</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="lv_cable" scale="2" />

  本整合包中的FTB工业奇械使用 **FE** .发电机从所有面输出FE,机器从所有面接收FE,任何模组的FE线缆或导管都可连接,无需<ItemLink id="lv_rectifier" />.

  FTB工业奇械经线缆向FE用电设备供电时,流量受线缆等级的传输速率限制.例如,连接到每刻可消耗数千FE的机器时,LV线缆仍只输送每刻1,024 FE,从而避免因过载烧毁.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">电压等级</Color>
</Column>

每种线缆和设备都有五种电压等级之一.输入超过设备等级上限时,它就会 **烧毁** .

| 等级 | 缩写 | 传输速率 | 典型用途 |
|------|--------|---------------|-------------|
| 低压     | **LV** | 1,024 FE/t    | 初期发电机和机器 |
| 中压  | **MV** | 4,096 FE/t   | 合金炉,回收机和高级机器 |
| 高压    | **HV** | 16,384 FE/t   | 采石场,泵和传送机 |
| 超高压 | **EV** | 65,536 FE/t | 核反应堆和大型电池盒 |
| 极高压  | **IV** | 262,144 FE/t | 反物质构建机和充电座 |

**基本原则:** 线缆等级应与所连接发电或用电设备的最高等级匹配.使用<ItemLink id="lv_transformer" />系列方块在不同电压等级间升压或降压.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">烧毁与保险丝</Color>
</Column>

输入电压过高的线缆会变成<ItemLink id="burnt_cable" />.机器也会熔毁,其方块实体变成烧焦的外壳,需要用<ItemLink id="fuse" />修复.

烧坏的线缆可回收成<ItemLink id="scrap" />.

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">分节</Color>
</Column>

<SubPages icons={true} />
