# 手册语言键翻译 (第 288-296 批)

9 个批次共 1029 个语言键, 全部为 Patchouli 或书籍式语言文件中的正文与标题.

| 批次 | 命名空间 | 范围 | 键 |
|---|---|---|---:|
| 288 | anima | Codex book: workshop diagram labels and the Getting Started chapter | 116 |
| 289 | anima | Codex book: Components and Golems chapters | 136 |
| 290 | anima | Codex book: Infusion and Saronite chapter | 96 |
| 291 | anima | Codex book: Collecting Souls and Spellcasting chapters | 122 |
| 292 | anima | Codex book: Gods & Worship and the spell list (30 spells) | 252 |
| 293 | anima | Codex book: Advanced part 1 (troubleshooting, workers, relays, idols, reconstructor, robe, offerings) | 132 |
| 294 | anima | Codex book: Advanced part 2 (golems, piloting, gods, shrines, priesthood, Pantheon, avatar fight) | 140 |
| 295 | anima | Codex book metadata: title, description and tooltip | 3 |
| 296 | arsmagicalegacy | Ability descriptions with affinity and range macros | 32 |

## 与普通语言批次的关系

手册键与普通键写在同一个 `zh_cn.json` 覆盖包里, 但批次分开: 普通批次只处理界面与物品文本, 手册批次只处理书页正文. 构建工具相同, 因此占位符, 数字顺序, § 颜色码, 换行数与行首行尾空格都受同一套校验.

## 处理原则

1. 书籍结构原样保留: 每段末尾的 `\` 换行标记, 空行数量, `$(br2)`/`$(br)` 宏, `entry://` 链接目标与 `%%` 转义一律不动, 只替换正文.
2. 术语先查已译物品名: 魂骨/萨隆铁/命血台桌/主仪式石/生命宝珠/灵质/法器/量化器/沉思晶格 等直接用覆盖包里已有的名字, 避免书里书外两套叫法.
3. 法术条目用模板生成: 30 个法术按 名称/查询句/消耗/冷却/效果/要点 六段统一, 冷却秒数与伤害数值逐条核对, 避免逐条手写产生偏差.
4. 数字与原文严格同序: 校验器按出现顺序比对数字, 中文语序需要调整时改写句式而不是调换数字顺序.

## 已完成的章节

- anima 死灵之书全部 997 键: 工作台图示, 入门, 部件, 魔像, 灌注与萨隆铁, 收集灵魂, 施法, 30 个法术, 神祇与信仰, 进阶(排查/工人/中继器/神像/复原器/长袍/献祭/魔像驾驶/神祇/神龛/祭司/万神殿/化身战).
- Ars Magica 能力说明 32 键.

## 剩余手册

- arsmagicalegacy 奥术全书 308 键.
- occultism 灵魂词典 217 键.
- 零散: starcatcher 50, neovitae 42, evilcraftcompat 25, betterfishtanks 21, animusnv 17, occultcooking 16, 以及 6 条单条条目.

游戏内验收未做.
