# 农业与食物完成报告 (第 135-156 批)

农业与食物类的普通语言部分已完成, 共 21 个批次.

- 语言键: 989
- 中文值: 811
- 保留的非正文值: 178
- 未完成草稿: 无
- 剩余: 68 条手册语言键 (Starcatcher 50, Occult Cooking 16, Mystical Agriculture 2), 属手册阶段
- 游戏内验收: 未做

## 逐批明细

| 批 | 命名空间 | 键 | 中文 | 保留 |
|---|---|---:|---:|---:|
| 135 | mobflowutilities | 183 | 182 | 1 |
| 136 | productivefarming | 171 | 4 | 167 |
| 137 | agritechevolved | 158 | 157 | 1 |
| 138 | mystianapiary | 82 | 81 | 1 |
| 139 | horsepowered | 75 | 75 | 0 |
| 140 | nutritional | 72 | 71 | 1 |
| 142 | farmingforblockheads | 34 | 32 | 2 |
| 143 | matc | 33 | 33 | 0 |
| 144 | productivebees | 27 | 26 | 1 |
| 145 | horsingaround | 25 | 24 | 1 |
| 146 | fertilization | 25 | 25 | 0 |
| 147 | mysticalagriculture | 23 | 23 | 0 |
| 148 | occultcooking | 13 | 13 | 0 |
| 149 | beer | 28 | 28 | 0 |
| 150 | growthacceleratortiers | 16 | 16 | 0 |
| 151 | animal_pen | 14 | 12 | 2 |
| 152 | animalgarden_alligatorgar | 3 | 3 | 0 |
| 153 | animalgarden_crocodile | 2 | 2 | 0 |
| 154 | animalgarden_seaotter | 2 | 2 | 0 |
| 155 | animalgarden_bullshark | 2 | 2 | 0 |
| 156 | cookingforblockheads | 1 | 0 | 1 |

## 关键判断

1. **拉丁学名是专名, 不是待译正文**. Productive Farming 的 171 键里有 166 条是作物学名 (`Amaranthus blitum`, `Brassica oleracea var. italica`), 双语并列时本来就不翻译; 全部原样保留, 只翻 4 条界面文案. 这一条如果不先看清, 很容易把 166 条"未译"当成缺口去硬翻.
2. **动物与作物的名称对齐既有中文**. 神秘农业的五级精华 (下级/初级/中级/高级/终极) 与注魔水晶沿用模组自带中文, MATC 的五种水晶耐久配置据此命名; Sickle 与 Scythe 在同一模组里并存, 必须分开 (镰刀 / 巨镰), 否则两个物品在 JEI 里会重名.
3. **神秘时代的术语不能自创**. Productive Bees 的特殊蜜蜂条目大量涉及 咒波 (flux)、腐化 (taint)、灵气节点 (aura node)、要素 (aspect)、空灵之花; 这些沿用既有中文, 否则整合包里会出现两套魔法术语.
4. **一处上游缺陷**. Animal Pen 自带的 `zh_cn.json` 在第 322 行前缺少逗号, 整个文件不是合法 JSON, 游戏内会整份回退英文; 而且它的值本身也还是英文. 本批没有参考这份文件, 也没有修改 JAR, 只按英文源补了 14 键, 并在批次清单里记了来源说明.
5. **碎片化 tooltip 要按句子续写**. Animal Pen 有几条 `tooltip[1]` 是长句的后半段 (如 `should trigger advancements.`), 单独成键; 译文按从句续写, 不加句首主语, 避免拼起来读不通.

## 未做

- 游戏内验收: 未检查蜂房界面数值排版, 营养 HUD 位置, 特殊蜜蜂研究页换行, 厨房台连接状态显示.
