# FTB Evolution 2 手册汉化评估

此文件为历史评估. 当前 1.4.0, CFPA 全版本及 PR 候选的盘点见 [remaining-1.4.0-summary.md](remaining-1.4.0-summary.md) 与 [文档手册明细](remaining-1.4.0-manuals.md).

评估日期：2026-10-17。仅检查和生成评估文件，未开始手册翻译，未改动游戏资源。

## 结论

手册汉化是下一阶段的大项。现有中文资源应先复用，再补缺和对照整合包改动；不能按模组已有中文就认定手册正文已翻译。当前候选缺口约185,942个英文词，其中Markdown/MDX约127,720词，JSON内嵌正文约15,677词，语言键正文约42,542词。词数只是去除部分标记后的估计，不是人工核定净词数，也不是承诺工期。

已扫描426个mods目录条目中的顶层JAR、当前CFPA压缩包和KubeJS assets/data。统计发现1,058份默认语言Markdown/MDX、2,462个Patchouli可见文字字段、8,044条手册相关语言键、80份冰火传说英文TXT。上述单位不同，不能相加称为页数或手册数量。手册框架示例语言键被排除，但Oracle Index开发者文档单列为可选范围。

## 统计口径与限制

- “中文候选”指对应路径/键有中文字符。它仅表明有可复用资源，不代表正文完整、质量通过、版本一致或已在游戏中生效。
- 模组JAR语言文件、CFPA和KubeJS语言文件按键汇总，避免把整合包只覆盖几个键的文件误当作完整词典。页面文件按路径覆盖。
- Patchouli对语言键的引用转入语言键统计，避免重复计算；硬编码正文另计。
- Markdown路径包含目录首页、导航页及部分API文档；英文词数可能包含YAML、代码外的参数、专名及标签。缺中文的短名也列为候选，后续需要人工排除。含中文但夹有英文的已有文件可能仍有漏译，不包含在此缺口内。
- 扫描候选资源不是模拟实际资源优先级。未启动游戏，尚未确认每本手册的入口、旧版内容是否仍可打开、资源包覆盖优先级及分页效果。孤立/测试手册条目先列入清单，实施时确认。
- Ponder演示、截图中的英文、动态生成页面、代码硬编码文字及联网内容未纳入正文词数，需另做运行检查。整合包更新后应重新扫描。

## 优先级和实施批次

1. **先做整合包专属手册**：FTB发电调整10页、杂交4页、技能6页、敌对生物网络3页，共23页，约5,043英文词。与刚完成的任务书关联紧密，先统一术语并建立GuideME翻译和验证流程。
2. **复核整合包覆盖页**：31页LTX、7页Powah、24页FTB工业奇械、1页Colossal Reactors，以及6页Oritech、2页Hephaestus、珠宝指南的定制内容。页面数包含新增和覆写候选；已有中文也须对照当前英文的机制、数值与链接。珠宝指南40个英文页面里36个已有中文候选，仍缺4个。
3. **集中补完主线的大手册**：Nautec约46,106词、Nodeworks约17,133词、Anima约12,097词、FTB工业奇械约11,344词、Stellaris约10,290词、魔法艺术：传承约8,868词、Colossal Reactors约7,441词。这七项约113,279词，占候选缺口约61%。各模组分章节完成，避免一批混合多套术语。
4. **补齐已有中文的增量**：神秘学、巫术、Neo Vitae、Animus、动态联合系列、Apotheosis等。按缺失键补译，然后检查已有译文中的英文段落及版本变化。
5. **其余中小手册与验收**：MFFS、模块化路由器、Kindred Spirits、Auroral、马力等；开发者文档和可选API参考单列，由实际使用需求决定顺序。

## 已有资源可复用情况

AE2与主要附属、Powah、LaserIO、Building Gadgets 2、Just Dyna Things等在本次静态匹配范围内已找到大部分或全部中文候选。Oritech当前是Oracle Index MDX手册：177个默认语言文档中170个有中文候选，另有整合包保留的6页GuideME定制指南，不能只看其中一套。

Nautec当前手册为GuideME Markdown，100页未找到对应中文；模组物品已有中文并不覆盖这些手册页面。Anima为Modonomicon，997条含英文的手册相关语言键未找到中文。Witchery本体977条含英文的手册键中273条有中文候选，704条待复核/补译；Forbidden Magic另有100条候选缺口。

## 技术路线

- 以独立的本地覆盖资源包承载翻译，保留英文源，避免改JAR或直接修改自动下载的CFPA包；确定游戏实际加载顺序后启用。
- GuideME/AE2沿用现有`_zh_cn`目录约定；Oracle Index使用其`translated/zh_cn`机制；Patchouli使用`zh_cn`目录；Modonomicon与Cyclops等以补充语言键为主。特殊TXT手册按当前本地格式处理。
- 不改物品ID、配方、章节依赖、研究条件、模型NBT、链接目标及组件属性。只翻译展示标题、导航、正文与可见提示。
- 原任务书片段编号工具不能直接用于全部手册。需要另建提取清单、源文件哈希、翻译映射和按格式的结构检查；可复用任务书术语与颜色/占位符保护规则。
- 静态验收核对资源路径、语言键、Markdown/MDX链接与标签、数值单位、图片及多方块展示引用；游戏中逐种框架验证入口、中文加载、翻页、导航和链接。

## 额外发现

当前JAR中的`assets/animal_pen/lang/zh_cn.json`和`assets/rootsclassic/lang/zh_cn.json`无法通过标准JSON解析。CFPA可能提供部分替代资源；本次未修改这些文件，也未据此断言运行时必然报错。动物围栏手册本身另有206个候选可见字段缺口。

FTB定制手册的入口定义（例如`kubejs/assets/ftb/guideme_guides/power.json`）还包含英文display_name/tooltip文本。这类入口也应随正文一起翻译，但未并入上面的正文词数。

## 逐项清单

以下字段/键的候选数用于定位工作，不能理解为实际页面数。“缺口词数”同样为粗估。

| 内容组 | 单位数 | 中文候选 | 缺口候选 | 缺口英文词约数 |
|---|---:|---:|---:|---:|
| advanced_ae [Markdown] | 13 | 13 | 0 | 0 |
| ae2 [Markdown] | 126 | 126 | 0 | 0 |
| ae2netanalyser [Markdown] | 2 | 2 | 0 | 0 |
| ae2wtlib [Markdown] | 7 | 7 | 0 | 0 |
| anima [language keys] | 997 | 0 | 997 | 12,097 |
| animal_pen [Patchouli] | 206 | 0 | 206 | 2,333 |
| animusnv [language keys] | 709 | 692 | 17 | 383 |
| apotheosis [Patchouli] | 557 | 499 | 58 | 801 |
| apotheosis [language keys] | 3 | 3 | 0 | 0 |
| appflux [Markdown] | 12 | 12 | 0 | 0 |
| appliedcooking [language keys] | 14 | 13 | 1 | 2 |
| arsmagicalegacy [Patchouli] | 26 | 0 | 26 | 368 |
| arsmagicalegacy [language keys] | 497 | 0 | 497 | 8,500 |
| auroral [Markdown] | 30 | 0 | 30 | 5,094 |
| betterfishtanks [language keys] | 21 | 0 | 21 | 202 |
| buildinggadgets2 [Patchouli] | 147 | 147 | 0 | 0 |
| colossal_reactors [Markdown] | 27 | 0 | 27 | 7,441 |
| dimresources [Markdown] | 2 | 0 | 2 | 207 |
| drones [Markdown] | 2 | 0 | 2 | 683 |
| enderio [Patchouli] | 4 | 0 | 4 | 21 |
| energizedpower [language keys] | 301 | 241 | 60 | 676 |
| energymeter [Markdown] | 2 | 0 | 2 | 1,694 |
| evilcraft [language keys] | 213 | 212 | 1 | 49 |
| evilcraftcompat [language keys] | 25 | 0 | 25 | 585 |
| extendedae [Markdown] | 45 | 45 | 0 | 0 |
| ftb [Markdown] | 23 | 0 | 23 | 5,043 |
| ftbic [Markdown] | 66 | 0 | 66 | 11,344 |
| hephaestus [Markdown] | 2 | 0 | 2 | 484 |
| horsepowered [Markdown] | 14 | 0 | 14 | 3,714 |
| iceandfire [Bestiary] | 80 | 79 | 1 | 3 |
| iceandfire [Patchouli] | 1 | 0 | 1 | 0 |
| integrateddynamics [language keys] | 264 | 153 | 111 | 3,958 |
| integratedterminals [language keys] | 61 | 0 | 61 | 1,929 |
| integratedtunnels [language keys] | 67 | 44 | 23 | 829 |
| irons_jewelry [Markdown] | 40 | 36 | 4 | 132 |
| justdirethings [Patchouli] | 608 | 601 | 7 | 16 |
| justdynathings [Markdown] | 35 | 35 | 0 | 0 |
| kindredspirits [Markdown] | 18 | 0 | 18 | 7,375 |
| laserio [Patchouli] | 187 | 187 | 0 | 0 |
| little_big_redstone [Markdown] | 26 | 25 | 1 | 56 |
| logisticsnetworks [Markdown] | 21 | 18 | 3 | 957 |
| ltxi [Markdown] | 67 | 66 | 1 | 358 |
| mffs [Patchouli] | 242 | 0 | 242 | 5,007 |
| modularrouters [Patchouli] | 226 | 0 | 226 | 7,105 |
| mystianapiary [Markdown] | 7 | 0 | 7 | 1,455 |
| mysticalagradditions [language keys] | 14 | 14 | 0 | 0 |
| mysticalagriculture [language keys] | 159 | 155 | 4 | 73 |
| mysticalautomation [language keys] | 23 | 23 | 0 | 0 |
| nautec [Markdown] | 100 | 0 | 100 | 46,106 |
| neosync [Markdown] | 10 | 0 | 10 | 2,411 |
| neovitae [language keys] | 1638 | 1595 | 43 | 1,184 |
| nodeworks [Markdown] | 75 | 0 | 75 | 17,133 |
| occultcooking [language keys] | 14 | 0 | 14 | 267 |
| occultism [language keys] | 1499 | 1260 | 239 | 2,850 |
| oracle-index [Markdown] | 6 | 0 | 6 | 1,920 |
| oritech [Markdown] | 177 | 170 | 7 | 1,222 |
| powah [Markdown] | 28 | 28 | 0 | 0 |
| productivebees [Patchouli] | 258 | 245 | 13 | 26 |
| recursiveae2patternprovider [Markdown] | 6 | 0 | 6 | 800 |
| refinedcooking [language keys] | 26 | 25 | 1 | 2 |
| simpleteleporters [Markdown] | 5 | 0 | 5 | 1,147 |
| starcatcher [language keys] | 422 | 0 | 422 | 1,244 |
| stellaris [Markdown] | 61 | 0 | 61 | 10,290 |
| trainingdummy [Markdown] | 3 | 0 | 3 | 654 |
| witchery [language keys] | 977 | 273 | 704 | 6,925 |
| witchery_forbidden_magic [language keys] | 100 | 0 | 100 | 787 |

复现：在实例根目录运行`python localization/assess_manuals.py`。机器清单见[manual-inventory.json](manual-inventory.json)，其中记录每个候选的资源路径、来源与中文来源。
