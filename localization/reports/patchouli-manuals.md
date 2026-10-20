# Patchouli 书籍汉化完成

Patchouli 阶段完成 8 本书的 zh_cn 覆盖, 产物写入 `.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN/assets/<ns>/patchouli_books/<book>/zh_cn/`.

| 命名空间 | 书籍 | 文件 | 字段 | 新译 | 处理 |
| --- | --- | ---: | ---: | ---: | --- |
| mffs | MFFS 力场手册 | 50 | 242 | 242 | 全量新译 |
| animal_pen | Animal Pen 动物围栏指南 | 58 | 206 | 206 | 全量新译; 术语沿用第 151 批 |
| apotheosis | 神化编年史 | 123 | 557 | 58 | 58 条新译, 其余沿用 JAR 自带中文并半角化 |
| arsmagicalegacy | 奥术纲要 (Patchouli 内联字段) | 14 | 26 | 26 | 正文经语言键承载, 本批只译内联字段; 条目正文引用 lang 键 |
| justdirethings | Just Dire Things 书 | 6 | 20 | 20 | 20 条新译, 其余沿用 JAR 自带中文 |
| modularrouters | Modular Routers 手册 | 61 | 226 | 5 | 5 条新译 (FTB Filter System 与假玩家), 其余沿用已装 CFPA |
| productivebees | 资源蜜蜂指南 | 81 | 258 | 13 | 13 条拉丁学名原样保留 (沿用第 136 批拉丁学名惯例), 其余沿用已装 CFPA |
| iceandfire | 冰与火之歌序章 | 1 | 1 | 1 | 上游 en_us 即为中文, 原样收录 |

合计 394 个 zh_cn 文件, 覆盖 1536 个文本字段, 其中 571 条为本项目新译; 其余沿用 JAR 自带中文或已装 CFPA (半角化后并入本包, 保证字段完整).

## 机制

- 提取/构建/校验: `localization/patchouli_translation.py extract|build|check [ns...]`, 已挂入 `project.py check`.
- 校验保护: `$(...)` 宏序列, `%%`, 数字顺序, 换行数, ASCII 标点; 上游即中文的字段允许原样收录.
- 带上游中文的书 (apotheosis, justdirethings) 以 JAR 内 zh_cn 为底, 只补缺口字段; productivebees 与 modularrouters 以已装 CFPA 文件为底; 发布时 Manuals 包先于 CFPA 写入, 冲突以 Manuals 为准, 文件为超集因此无损.
- 拉丁学名 (productivebees 13 条) 按第 136 批惯例原样保留.

## 覆盖对照

盘点 (`remaining-1.4.0-manuals.json`) 的 Patchouli 暂无候选 557 字段全部处理: 新译 543 条 (mffs 242, animal_pen 206, apotheosis 58, ars 26, justdirethings 20 (含 7 条上游已中文化的同类字段), modularrouters 5, iceandfire 1 上游即中文), 拉丁学名保留 13 条 (productivebees), 剩余 1 条为 iceandfire 上游自带中文.
