# 1.4.0 手册文档剩余量静态盘点

重跑: 在项目根目录运行 `python localization/assess_1_4_manuals.py`.

> 2026-10-18 更新: 本表列出的 305 篇剩余 Markdown/MDX 已全部完成, 见 [剩余手册批次](manual-extra-1.4.0.md); Patchouli 557 个字段已完成; Bestiary 唯一剩余项为 `example.txt` 空白模板, 已排除. 当前文档型手册缺口为 0. 下表保留批次完成前的静态盘点, 不再代表当前剩余量.

此报告不含 lang/*.json 中承载的手册正文; 这些语言键由总盘点另计. Markdown/MDX 与 TXT 按文档计, Patchouli 按可见 JSON 字段计, 不得相加称为页面数.

输入见 [project.json](../../project.json)、[手册源清单](../manuals/source_manifest.json)、[范围名单](../language_scope.json). 使用当前实例 /home/astronw/.ftba/instances/ftb evolution 2 的 425 个启用顶层 JAR 及 KubeJS 同路径覆盖; 未将旧实例或旧 CFPA 压缩包视作新版已覆盖. CFPA 扫描本地全部版本目录, 锁定提交 719672954d9df4ea51877e3d5ce2912148273682.

## 项目已译页源文复核

369 页已有/审校复用清单中找到 369 页, 原文完全相同 369 页. 这证明既有译文可复用, 不代表已安装或游戏内验收.

## 各组候选与缺口

“已有”指项目源哈希不变或模组自带对应中文含汉字. “精确”指 CFPA 配套英文与当前原文逐字一致. “无英文”无法核验, “已变”必须适配. 所有 CFPA 项仅为待审候选.

| 分组 | 单位 | 总量 | 已有候选 | 剩余 | CFPA 精确 | 无英文 | 已变 | 无候选 | 剩余英文词约数 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| advanced_ae | documents | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |
| ae2 | documents | 126 | 126 | 0 | 0 | 0 | 0 | 0 | 0 |
| ae2netanalyser | documents | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| ae2wtlib | documents | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| animal_pen | visible_JSON_fields | 206 | 0 | 206 | 0 | 0 | 0 | 206 | 2333 |
| apotheosis | visible_JSON_fields | 557 | 499 | 58 | 0 | 0 | 0 | 58 | 801 |
| appflux | documents | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |
| arsmagicalegacy | visible_JSON_fields | 26 | 0 | 26 | 0 | 0 | 0 | 26 | 368 |
| auroral | documents | 30 | 0 | 30 | 0 | 0 | 0 | 30 | 5094 |
| colossal_reactors | documents | 27 | 0 | 27 | 0 | 0 | 0 | 27 | 7441 |
| dimresources | documents | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 207 |
| drones | documents | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 683 |
| energymeter | documents | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 1694 |
| extendedae | documents | 45 | 45 | 0 | 0 | 0 | 0 | 0 | 0 |
| ftb | documents | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 |
| ftbic | documents | 66 | 66 | 0 | 0 | 0 | 0 | 0 | 0 |
| hephaestus | documents | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 484 |
| horsepowered | documents | 14 | 0 | 14 | 0 | 0 | 0 | 14 | 3714 |
| iceandfire | documents | 80 | 79 | 1 | 0 | 0 | 0 | 1 | 3 |
| iceandfire | visible_JSON_fields | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| irons_jewelry | documents | 40 | 36 | 4 | 0 | 0 | 0 | 4 | 132 |
| justdirethings | visible_JSON_fields | 608 | 602 | 6 | 0 | 0 | 0 | 6 | 12 |
| justdynathings | documents | 35 | 35 | 0 | 0 | 0 | 0 | 0 | 0 |
| kindredspirits | documents | 18 | 0 | 18 | 0 | 0 | 0 | 18 | 7375 |
| laserio | visible_JSON_fields | 187 | 187 | 0 | 0 | 0 | 0 | 0 | 0 |
| little_big_redstone | documents | 26 | 26 | 0 | 0 | 0 | 0 | 0 | 0 |
| logisticsnetworks | documents | 21 | 18 | 3 | 0 | 0 | 0 | 3 | 957 |
| ltxi | documents | 67 | 66 | 1 | 0 | 0 | 0 | 1 | 358 |
| mffs | visible_JSON_fields | 242 | 0 | 242 | 0 | 0 | 0 | 242 | 5007 |
| modularrouters | visible_JSON_fields | 226 | 221 | 5 | 0 | 0 | 0 | 5 | 130 |
| mystianapiary | documents | 7 | 0 | 7 | 0 | 0 | 0 | 7 | 1455 |
| nautec | documents | 100 | 0 | 100 | 0 | 0 | 0 | 100 | 46106 |
| neosync | documents | 10 | 0 | 10 | 0 | 0 | 0 | 10 | 2411 |
| nodeworks | documents | 75 | 75 | 0 | 0 | 0 | 0 | 0 | 0 |
| oracle-index | documents | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 572 |
| oritech | documents | 177 | 170 | 7 | 0 | 0 | 0 | 7 | 1222 |
| powah | documents | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 |
| productivebees | visible_JSON_fields | 258 | 245 | 13 | 0 | 0 | 0 | 13 | 26 |
| recursiveae2patternprovider | documents | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 786 |
| replication | documents | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| simpleteleporters | documents | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 1147 |
| stellaris | documents | 61 | 0 | 61 | 0 | 0 | 0 | 61 | 10313 |
| trainingdummy | documents | 3 | 0 | 3 | 0 | 0 | 0 | 3 | 654 |

## 方法边界

- 对照路径保留完整 CFPA 来源版本及文件, 详见同名 JSON. 不因版本不同跳过检索, 但仅额外尝试 GuideME /guides/{namespace}/guide/ 到旧 /guide/ 的目录迁移对应, 未做任意改名页面的语义映射. 精确候选也仍需术语与格式验收.
- 自带中文仅以对应字段/文档含汉字识别, 混合中文与未译英文可能仍有遗漏, 因此这是乐观候选覆盖而非完成声明.
- Building Gadgets 2 已由主线程依据当前模组元信息列入建筑工具排除名单, 不在主表中. 排除路径保留于 JSON 的 ignored_paths.
- 已通过 build-manifest 与 verification 双重校验的 CFPA 审校包按逐页/字段决定计入项目覆盖; 未启用不代表已安装到真实游戏. 其他额外资源包及运行时资源优先级未验收; 同名 JAR 路径冲突按文件名排序取值, 与实际加载顺序可能不同.
- 英文词数去掉代码块和常用标记, 只用于工作量近似; 不等于需逐词重新翻译.
- 手册重要性尚需结合任务引用与使用门槛划分, 本报告不擅自将所有手册列作关键手册.
- Patchouli 可见字段的值若精确命中当前启用 JAR 的英文语言键集合, 则作为语言键引用单列于 JSON 的 language_key_references, 不计入本表正文; 因此不会与语言键盘点重复. 当前引用集合不对未解析引用作猜测. JSON 的引用记录带当前文档路径、字段路径、语言键、来源和排除范围标记.
- 已排除 credits、readme、Computercraft 开发/终端帮助及 modonomicon/cyclopscore 框架示例资源; EnderIO 明确标注 Test Entry/Test Category 的占位示例及 Oracle Index 的 developer 开发文档也排除. Oracle Index 的 search/user_guide 两页为玩家使用指南, 保留.
- 未翻译任何正文, 未改动游戏、CFPA 或现有译文.

解析错误数: 0. 已纳入 file-cache-index.json 中固定 head SHA 的未合并 PR 文档候选; PR 编号、作者、提交及来源见 JSON. 未审查批准采用. 若 PR 未修改配套英文且基线 SHA 与本地 CFPA 一致, 允许以该基线英文核验; 否则无法核验即单列.

## 分格式汇总

| 格式 | 文档总数 | 计量单位总数 | 原始剩余单位 | 原始剩余词数 | 精确 CFPA/PR 候选单位 | 精确候选词数 | 扣除精确候选后词数 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Markdown/MDX | 1053 | 1053 | 305 | 92805 | 0 | 0 | 92805 |
| Patchouli | 607 | 2311 | 557 | 8677 | 0 | 0 | 8677 |
| Bestiary TXT | 80 | 80 | 1 | 3 | 0 | 0 | 3 |

以上扣除只用于估算新增翻译量, 精确候选仍需裁决、格式复核和合入. PR 不会因未合并而跳过, 本次发现对原始缺口直接相关的 PR 文档为 #6142 AE2 import/export card、#5196 AE2 storage cells 和 #5997 Little Big Redstone battery; 候选均在 JSON 标明英文核验结果.
