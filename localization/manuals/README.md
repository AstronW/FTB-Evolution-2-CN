# FTB Evolution 2 手册汉化

手册已通过成果统一包含项目翻译与 CFPA 审校: **369 页文档手册** (164 + 205, 无重复)、**1,642 个手册语言键** (原批次 366 + CFPA 1,276) 及 **508 个 Patchouli 可见字段**. 以下 164 页为原项目来源子集, 不代表当前合并总量. [合并统计](../reports/verified-progress-summary.md).

## 1.4.0 剩余手册批次

本轮另完成 305 篇 Markdown/MDX 玩家手册 (Nautec 100, Stellaris 61, Auroral 30, Colossal Reactors 27, Kindred Spirits 18, Horse Powered 14, Neosync 10, Mystian 7, Oritech 7, 其余 31), 共 92805 个英文词. 译文保存在 `../manuals_extra/translations`, 构建后并入同一手册资源包; Stellaris 61 页是服务端数据, 写入 `.minecraft/datapacks/ftb_evolution_cn`.

- 提取/构建/检查: `python localization/manual_extra_translation.py extract|build|check|check-page <page>`
- 独立校验: `python localization/verify_manual_extra.py`
- 范围、来源、检查项和未验收项见 [剩余手册批次报告](../reports/manual-extra-1.4.0.md).
- 已通过 `python project.py check` 与发布包构建/检查; 游戏内翻页, 链接和排版尚未验收.

本批翻译已完成并安装到独立资源包 `FTB-Evolution-2-Manuals-zh_CN`. 所有本批译文使用英文标点. 原英文源, 模组JAR, 配方, 游戏配置与存档未修改; 客户端 options.txt 仅追加启用本资源包.

## 完成范围

| 手册 | 页面 |
|---|---:|
| 发电调整 | 10 |
| 农业杂交 | 4 |
| 技能树 | 6 |
| 敌对生物网络 | 3 |
| FTB工业奇械 | 66 |
| Nodeworks | 75 |
| 合计 | 164 |

覆盖3,638个含英文的可见行片段, 包括标题, 导航, 正文及表格. 另补充四本整合包指南的8条入口名称/提示, 以及168条与手册相关的FTB工业奇械机器名称, 控件和说明语言键, 另有111条Nodeworks语言键. 保留模组名, 电压等级, 单位和原始配置/代码标识.

FTB工业奇械源文件取当前JAR资源, 再叠加KubeJS同路径覆盖, 共66页. 没有以JAR的旧版说明替代整合包改写内容.

## 安装与加载

资源包目录为 `.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN/`. 已在 `.minecraft/options.txt` 的资源包列表末尾选中, 作为高优先级覆盖. 先前列表保存在 `resource_packs_before.json`.

在简体中文下重载资源或重启客户端即可加载. 页面沿用GuideME的 `_zh_cn` 目录约定, 原页面ID, 链接, 图像, 多方块展示和动态能量组件保持不变. 入口名称使用语言键, 并保留英文回退, 不硬改英文模式的显示名称.

当前未操作游戏, 尚未实测游戏内翻页, 多方块渲染, 链接点击和屏幕排版. 原生解析通过不等同于游戏内测试完成.

## 验收证据

- `verification.json`: 164页文件集合, 源文件哈希, 链接目标, 组件标签/属性, 数值, 表格列数, 格式占位符, 入口定义和启用配置检查通过. 383行表格逐行核对列数.
- `native-parser-check.txt`: 使用当前安装的GuideME自带Markdown/MDX解析器, 以与PageCompiler相同的语法扩展解析164页英文和164页中文, 共328页, 全部成功. SLF4J无日志后端提示仅来自独立命令行检查环境.
- `ast-structure-review.json`: 当前为 `[]`. 原文与中文的非文本语法节点数量一致, 包括标题, 表格, 列表, 链接, 组件和强调. 中文标点邻接可能导致粗体失效的位置已修复, 并已统一英文标点.
- 残留英文审查只允许已列明的模组名, 专名, 单位, 按键和代码标识. 检查禁止本批资源中的中文标点.
- 13行有明确本地证据的原文勘误记录于 [source-corrections.md](source-corrections.md), 涉及Powah每桶熔岩发电量, 地热与风力输出, 每种升级上限及储能升级容量. 英文源保持不变.

## 维护与复现

在实例根目录运行:

```bash
python localization/manual_translation.py check
python localization/verify_manuals.py
python localization/verify_manuals_native.py
```

修改译文后用 `python localization/manual_translation.py build` 更新资源包. 单页查看原文片段可使用 `python localization/manual_translation.py show ftbic/energy/batteries.md`.

- `source_manifest.json`: 164页有效英文源的SHA-256.
- `entry_source_manifest.json`: 四个整合包入口定义的SHA-256.
- `translations/`: 按零起始原文行号保存的人工翻译. 不可在原文更新后盲目沿用旧行号.
- `extra_resources/`: 资源包元信息, 指南入口和补充语言文件的可维护来源.
- `extra_language_sources.json`: 168条补充语言键的英文源, 验收时与当前JAR再次比对.
- `source_corrections.json`: 逐行勘误白名单, 同时绑定原文和译文, 不允许静默绕过数值检查.
- `terms.json`: 本批术语参考. 不作为对任意正文进行全局替换的词典.
- `progress.json`: 构建工具生成的实际覆盖状态.

更新整合包或模组后, 若源哈希或英文语言键发生变化, 应先审阅变化, 更新翻译和证据, 再构建. 不修改自动下载的CFPA资源包.

Nodeworks的详细范围及页内链接兼容说明见[NODEWORKS.md](NODEWORKS.md). 全部既有及未来译文使用英文标点, 统一约定见[STYLE.md](../STYLE.md).
