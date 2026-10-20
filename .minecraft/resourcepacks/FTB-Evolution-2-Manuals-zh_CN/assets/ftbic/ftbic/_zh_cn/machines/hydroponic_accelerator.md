---
navigation:
  title: 水培加速器
  icon: ftbic:hydroponic_accelerator
  parent: machines/index.md
  position: 5
item_ids:
  - ftbic:hydroponic_accelerator
  - ftbic:advanced_hydroponic_accelerator
---

# 水培加速器

<ItemImage id="hydroponic_accelerator" scale="2" float="right"/>

<RecipeFor id="hydroponic_accelerator" />

将种子放入 **种子** 槽,将允许的方块放入 **土壤** 槽.土壤会留在机器内,永不消耗.供给水和能量即可种植作物.配方返还种子时,种子保留在种子槽中继续生长,只有多余种子进入输出,因此一粒种子就足以持续运行.输出槽分别存放农产品,返还种子和可选副产物.初始小麦配方使用泥土时为正常速度,使用苔藓时为 **1.25倍速度** .JEI会列出每个配方的土壤选择和速度.

基础机器有一对种子与土壤槽,三个输出槽.水箱容量为16,000 mB,默认每个生长周期消耗250 mB.使用 **I/O** 配置物品,流体和能量传输面. **L** 按钮可将种子和土壤槽锁定为指定物品,也可从JEI拖入物品来设置虚拟锁定.虚拟锁定只是过滤,不会提供实际原料.

## 杂交模式

只有高级水培加速器可在 **生长** 和 **杂交** 模式之间切换.向一组杂交通道的每条通道各放入一种亲本种子,两个亲本都必须具有与各自土壤匹配的有效生长配方.JEI会显示可用组合及成功概率.杂交成功时消耗两个亲本各一粒种子,产出所列突变物品;失败时返还两个亲本.无论成功与否,都消耗时间,水和能量.任一可能产物没有足够输出空间时,机器会等待.

## 高级水培加速器

<ItemImage id="advanced_hydroponic_accelerator" scale="2" float="right"/>

<RecipeFor id="advanced_hydroponic_accelerator" />

高级机器有 **四对独立的种子与土壤槽** 和十二个输出槽,每条通道各分为农产品,种子和副产物槽.每对输入都可单独设置虚拟锁定,种植不同作物.水箱容量为32,000 mB.各活动通道独立耗能,最高总耗能为单通道的四倍.它还接受<ItemLink id="parallel_processing_upgrade" />:每条通道可在同一周期内,按种子槽中的种子数量同时种植,最多四粒,耗水和耗能相应倍增.

杂交模式下,通道 **1+2** 和 **3+4** 组成两组独立杂交.每个亲本使用各自土壤,由较慢的土壤决定杂交速度.失败后的亲本返还至各自通道的种子输出槽.模式,锁定和进度都会随世界保存.
