---
navigation:
  parent: items-blocks/index.md
  icon: instruction_set
  title: 配方集
categories:
  - autocrafting
description: stores crafting recipes for [autocrafting](../nodeworks-mechanics/autocrafting.md)
item_ids:
- nodeworks:instruction_set
- nodeworks:processing_set
---

# <a name="recipe-sets" /> 配方集

自动合成使用两种配方集保存
[合成配方](../nodeworks-mechanics/autocrafting.md).

配方集是保存单个配方的模板物品, 供
[自动合成](../nodeworks-mechanics/autocrafting.md)系统执行. 每个
配方集在自己的界面中编写, 再放入对应[存储方块](./storage_blocks.md).

两类配方集分别适用于:

- **合成指令集:** 原版3x3合成配方, 包括有序和无序合成
- **加工配方集:** 其他配方, 如烧炼, 模组机器, 多产物加工或有超时要求的流程

---

## <a name="instruction-set" /> 合成指令集

<ItemImage scale="4" id="instruction_set" />

3x3合成模板, 原版工作台中可用的配方在这里都能使用.

### <a name="creating-a-recipe" /> 编写配方

右击打开界面, 拿着物品点击虚拟槽位, 可固定一个
虚拟副本, 不消耗实际物品; 再点击空槽即可清除.
图案匹配已知合成配方时, 结果槽会自动填充.
**全部清除** 可重置网格.

界面还有 **标签替代** 开关. 开启时(默认开启),
配方接受与模板原料属于相同标签的任意物品,
例如橡木木板槽也可使用白桦木板, 云杉木板或
`#minecraft:planks`中的其他物品. 关闭后仅匹配准确物品ID.

> **提示:** 此界面支持JEI的 **(+)** 配方转移按钮, 可在JEI中选择合成
> 配方后点击(+), 一步填满网格.

### <a name="deploying-it" /> 部署配方

将写好的配方集放入<ItemLink id="instruction_storage" />. 相邻的
合成指令存储器会组成集群, 只要集群中的 *任意* 方块
接入网络, CPU就能读取整组配方集.

---

## <a name="processing-set" /> 加工配方集

<ItemImage scale="4" id="processing_set" />

自由形式的配方, 最多9种输入和3种输出, 还可设置
每次加工的超时. 适合3×3网格无法描述的流程, 如烧炼,
高炉冶炼, 模组机器配方, 多产物加工, 或任何
*"等待N游戏刻后才会出现产物"* 的过程.

### <a name="creating-a-recipe" /> 编写配方

右击打开界面, 包括:

- **输入网格** : 3×3个虚拟槽, 可在任意位置设置原料.
- **输出列** : 3个虚拟产物槽.
- **超时栏** : 0–999游戏刻(0为不设超时). `+`和`-`按钮每次调整20, Shift点击调整100.
- **串行开关** : 开启后, CPU不会同时并行执行
  此配方的多个实例.
- **替代开关** : 开启后, 从标签配方填入的原料槽
  (图标会轮换显示标签成员)接受标签中的任意物品,
  各输入也接受相同物品的任意数据组件变种. 关闭后
  仅匹配显示的准确物品.
- **全部清除** : 重置所有设置.

在已填充槽位上滚动可调整数量: 向上+1,
向下-1; 数量为1时再向下滚动会清空.

> **提示:** 这里也支持JEI的 **(+)** , 且具有 *通用性* . JEI
> 已知的任意配方类别, 如烧炼, 高炉或模组配方, 都可以使用. 若某输入
> 在JEI中显示多个候选物品, 例如`#minecraft:smelts_to_glass`中的不同沙子, 会记录为该
> 标签, 开启替代后即可使用你已有或可合成的任意成员.

### <a name="deploying-it" /> 部署配方

将写好的配方集放入<ItemLink id="processing_storage" />. 与
合成指令存储器一样, 相邻加工配方存储器会形成集群. CPU
会协调实际执行配方的外部机器.

## <a name="Recipes" /> <a name="recipes" /> 配方

<Row>
    <RecipeFor id="instruction_set" />
    <RecipeFor id="processing_set" />
</Row>
