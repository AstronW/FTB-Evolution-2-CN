# 1.4.0 剩余手册文档汉化

本批次处理 `localization/reports/remaining-1.4.0-manuals.json` 中仍未覆盖的 Markdown/MDX 玩家手册页. 目标是从独立源快照翻译, 构建到现有手册资源包与一个 Stellaris 数据包, 并用项目原有 GuideME 解析器复核结构.

## 范围

| 分组 | 页数 | 英文词约数 | 交付位置 |
| --- | ---: | ---: | --- |
| Nautec | 100 | 46106 | `assets/nautec/guides/nautec/guide/_zh_cn/` |
| Stellaris | 61 | 10313 | `datapacks/ftb_evolution_cn/data/stellaris/wiki/infos/` |
| Auroral | 30 | 5094 | `assets/auroral/auroral/_zh_cn/` |
| Colossal Reactors | 27 | 7441 | `assets/colossal_reactors/guides/colossal_reactors/guide/_zh_cn/` |
| Kindred Spirits | 18 | 7375 | `assets/oracle_index/books/kindredspirits/translated/zh_cn/docs/` |
| Horse Powered | 14 | 3714 | `assets/horsepowered/guides/horsepowered/guide/_zh_cn/` |
| Neosync | 10 | 2411 | `assets/neosync/guides/neosync/guide/_zh_cn/` |
| Mystian Apiary | 7 | 1455 | `assets/mystianapiary/guides/mystianapiary/guide/_zh_cn/` |
| Oritech | 7 | 1222 | `assets/oracle_index/books/oritech/translated/zh_cn/content/` |
| 其他 GuideME/Oracle 小手册 | 31 | 约 7700 | 各自 `_zh_cn` 或 `translated/zh_cn` |

合计 305 页, 92805 个英文词. 建筑装饰模组不在范围内; 该批不含 Patchouli 字段, 因为 557 个可见字段已由 `patchouli_translation.py` 完成.

## 完成状态

- 305/305 页已翻译, 92805/92805 个英文词覆盖.
- 244 页通过 GuideME 原生 Markdown/MDX 解析器; 61 篇 Stellaris 页面使用 Stellardown 语法, 由标记/链接/数字/表格检查覆盖.
- `python project.py check` 全部通过, 包括任务书, 旧手册, 普通语言, 自定义内容, Patchouli, CFPA 审校和新手册批次.
- `python localization/release_pack.py build` 与 `check` 通过; 资源包 1322 个成员, 安装包 1443 个成员; Stellaris 61 页作为 `datapacks/ftb_evolution_cn` 随安装包分发.
- 2 处源文硬换行造成的伪列表差异已单独复核记录, 未在译文中复现伪列表.
- 未进行游戏内验收.

## 维护方式

- 源快照: `localization/manuals_extra/sources/<原路径>`, 由 `python localization/manual_extra_translation.py extract` 从当前实例 JAR/KubeJS 覆盖重新生成, 并记录 SHA-256.
- 译文: `localization/manuals_extra/translations/<原路径>`, 整页保存. 原始 JAR 与 CFPA 资源不修改.
- 构建: `python localization/manual_extra_translation.py build`, 写入 `.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN` 与 `.minecraft/datapacks/ftb_evolution_cn`.
- 单页检查: `python localization/manual_extra_translation.py check-page <原路径>`.
- 全量检查: `python localization/manual_extra_translation.py check` 与 `python localization/verify_manual_extra.py`.
- 术语: `localization/manuals_extra/glossaries/<group>.json` 只收录当前 JAR/项目普通语言/已审校 CFPA 已存在的中文名称, 不作为全局替换字典.
- 工作说明: `localization/manuals_extra/TRANSLATION_GUIDE.md`.

## 检查项

- 页面源哈希与清单一致; Stellaris 以外的页面通过 GuideME 原生 Markdown/MDX 解析器.
- frontmatter 仅翻译 `title` 与 `navigation.title`; 非显示字段保持原值.
- 标题层级, 列表标记, 表格形状, 引用块, 组件标签, 链接目标, 内联代码, 数字, 宏, 占位符和 Stellaris `[ref=...]` 标记必须保留.
- 中文正文使用英文半角标点; 禁止 `…`, `—`, `–` 和全角标点.
- 本地链接必须仍能解析到当前模组页面.

## 未完成与未验收

- 游戏内翻页, 链接点击, 多方块渲染, 表格排版, 资源包/数据包加载优先级均未实测.
- FancyMenu 主菜单图片内嵌文字是图片资源, 不在本批语言正文范围.
- Stellaris Wiki 使用服务端数据包覆盖, 不是资源包; 多人服务器需由服主安装, 且同一数据包会影响该服务器的所有语言玩家.
- 后续模组或整合包更新后, 需重新 `extract` 并核对源哈希, 不能直接沿用旧页.

## 术语同步

本批发现任务书 Auroral 章节仍使用旧译名 (冻伤/寒冷酿造台/微光织物/冰川盆), 与当前游戏内名称不一致. 已同步为 霜噬/低温酿造台/微光编织 (织物物品为 微光布)/冰川之盆, 并重建任务书语言文件; 详见 `localization/TERMINOLOGY.md`.
