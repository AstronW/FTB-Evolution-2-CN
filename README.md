FTB Evolution 2 简体中文汉化项目. 目标目录为 `~/Projects/FTB-Evolution-2-CN`, 游戏目标实例为 `~/.ftba/instances/ftb evolution 2`.

## 仓库内容与本地依赖

仓库保留译文、术语、构建与检查工具、源文快照、审校证据、工作副本中的文本资源以及 `review/` 审查网页源码. 不提交 CFPA 克隆、模组 JAR、下载的资源压缩包、`dist/` 发布包、Node 依赖、验证缓存或本地助手状态. 上游来源与许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

克隆仓库后, 按本机位置调整 `project.json` 的实例路径, 准备对应版本的游戏实例与 `CFPA/` 检出 (固定提交见 `project.json`). 重新建立 `.minecraft/mods` 和 `.minecraft/quest-inputs/` 所需的本地 JAR 链接; 嵌套 JAR 输入说明见 `localization/vendor/jar-in-jar/README.md`. 原生解析检查还依赖本机 Java 库及解析脚本指定的路径. 完整检查需要这些外部输入, 仅克隆仓库不会自动具备它们. `.minecraft/options.txt` 是历史工作副本的资源包选择快照, 不应覆盖到游戏目录. 发布包按下文命令本地构建; 审查网页的依赖和数据按 `review/README.md` 重新生成.

本项目迁移了已完成的译文、术语表、构建工具、校验工具、源文快照和已有中文产物. 任务书已适配 1.4.0, 包含新增 Replication 章节, 见 [任务书适配记录](localization/reports/quests-1.4.0.md). 普通文本与手册已完成 1.4.0 源文适配: 305 篇剩余 Markdown/MDX 手册全部翻译并通过静态检查, 557 个 Patchouli 可见字段完成; 自定义内容已按 1.4.0 分批适配 (商店、支持对话和语言/运行时提示已通过选定范围检查, FancyMenu 图片内嵌文字等仍未完成), 已审校 CFPA 子集另有 1.4.0 覆盖包; 各组件版本见 `project.json` 的 `component_baselines`. 本轮构建已安装到游戏实例并校验安装文件, 但整包尚未通过游戏内验收.

- `localization/`: 可维护译文、术语、源文清单、构建脚本和历史报告.
- `.minecraft/`: 独立的翻译工作副本, 包含源文和译文, 不是游戏安装目录. 构建不会直接写入 FTB 实例.
- `.minecraft/mods`: 指向 `project.json` 中 `target_instance` 的模组目录, 当前为 FTB App 1.4.0 实例, 仅供读取源文, 不通过此链接修改 JAR. `source_instance` 同步使用当前目标实例; 不含游戏 JAR 的复制分发.
- `.minecraft/quest-inputs/`: 任务书 1.4.0 所需的语言源快照及新实例 Companion JAR 的只读依赖链接; 普通文本与手册已完成本轮 1.4.0 适配, 后续模组更新仍需逐批核对源文和清单.
- `CFPA/`: 用户已克隆的上游仓库. 本次迁移不复制、不覆盖、不更新它. 后续从此目录读取 CFPA, 不要求安装 I18nUpdateMod. `localization/fetch_cfpa.py` 保留为手动下载历史发布资源的辅助工具, 不是使用本地克隆的前置步骤.
- `project.json`: 目标实例路径和当前源文/CFPA 版本记录.

2026-10-19 玩家反馈修复已构建并安装: 同步任务书模组名称, 补齐 Kindred Spirits / Oracle Index 目录与四本 Patchouli 首页, 修复统一材料及极光手册的配方组件引用. 逐项结果, 上游缺配方的例外与验收边界见 [反馈修复记录](localization/feedback_20261019/README.md). 另补齐钠 Sodium 0.9.2 的 105 个界面语言键, 见 [第 316 批](localization/ordinary/batch-316/README.md). Nodeworks 硬编码 UI 按用户要求保留英文; 语言键覆盖数不等于实际界面或配方渲染已全部验收.

按此前 1.4.0 静态盘点范围, CFPA 各版本与固定 PR 快照的已列出待译量为 0, 见 [剩余汉化工作](localization/reports/remaining-1.4.0-summary.md). 报告仍保留批次完成前的候选复用/跨版本适配/暂无候选基线, 便于复核. 305 篇剩余手册的范围、来源、完成量与未验收项见 [剩余手册批次](localization/reports/manual-extra-1.4.0.md); 批次前的模组类型分布见 [按模组类型的剩余分布](localization/reports/remaining-1.4.0-by-mod-type.md).

已通过成果按内容统一统计为: 普通语言 25,840 键、手册语言 3,475 键、分组名称 95 条、文档手册 369 页 (原批次), 另有本轮 305 篇 Markdown/MDX 与 92,805 个英文词、Patchouli 可见字段 508 个及新增 Patchouli 缺口 557 字段, 均包含已审校 CFPA, 不重复相加. 任务书和整合包自定义文案另计. 来源与去重见 [合并进度](localization/reports/verified-progress-summary.md) 与 [剩余手册批次](localization/reports/manual-extra-1.4.0.md).

CFPA 审校复用包已独立构建, 包含语言键, 分组名称及手册覆盖, 来源和修复见 [审校记录](localization/cfpa_review/README.md). 构建使用 `python localization/cfpa_review_build.py build`, 校验使用 `python localization/cfpa_review_build.py check`, ZIP 输出到 `dist/`, 不写入真实游戏目录. 这只是已审校的适用子集, 不是将全部 CFPA 或 PR 直接合并.

各阶段已通过部分可汇总为一个安装用的汉化包, 组成、命令与覆盖边界见 [汇总汉化包记录](localization/reports/release-pack-1.4.0.md). 汇总产物为 `dist/FTB-Evolution-2-1.4.0-zh_CN.zip`(资源包) 与 `dist/FTB-Evolution-2-1.4.0-zh_CN-install.zip`(含任务书语言、整合包数据、Stellaris Wiki 数据包与运行时脚本的完整安装包). 本轮已重新构建并通过 `release_pack.py check`; 本轮已安装到目标实例并启用资源包, 安装后哈希核验通过, 备份记录见 `dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json`. 安装使用 `python localization/release_pack.py install`, 可选 `--enable` 同时写入 options.txt; 还原使用 `python localization/release_pack.py revert`. 安装按明确文件清单执行并先备份被覆盖的文件, 不复制整个工作副本.

在项目根目录运行:

```bash
python project.py info
python project.py check
python localization/release_pack.py plan
python localization/release_pack.py build
python localization/release_pack.py check
python localization/release_pack.py install
```

check 会检查任务书、手册、自定义语言、运行时提示、305 篇剩余手册批次以及已完成的语言批次第 001-316 批, 另运行 GuideME 原生解析器. 当前无未完成的源文提取稿. Java 解析依赖本机 Prism libraries 中已有的 Gson、Guava 和 SLF4J, 路径仍由现有解析脚本读取. 切换新版模组导致的 10 个旧批次检查失败已修复: 逐批核对新版源文并重新绑定 JAR, 新增待处理键与旧兼容键单列; 详见 [批次输入适配记录](localization/reports/ordinary-1.4.0-rebind.md).

执行顺序: 任务书 → 整合包特色内容 (商店、NPC 对话及相关交互和提示) → 关键手册 → 普通汉化文本 → 其他手册 → 全量收尾. 阶段范围及验收要求见 `AGENTS.md`.

继续工作时先按新版 1.4.0 调整原文和清单, 再更新相关译文. `.minecraft/mods` 已切换为新版模组输入, 旧批次可能因 JAR 文件名或源文变化而检查失败; 必须审阅差异并适配, 不强行覆盖源哈希, 也不要把工作目录整体复制到游戏实例. 各语言键、任务书和运行时脚本需按更新评估增量合并. 发布与安装命令见上文, 安装前先核对目标实例和备份记录.

所有本项目译文使用英文标点. 普通语言翻译继续排除 Chisel 和装饰类模组, 详见 `localization/language_scope.json`. 保留物品 ID、任务 ID、点击动作、占位符、命令、原始英文、配方和存档.

CFPA 当前本地检出为提交 `719672954d9df4ea51877e3d5ce2912148273682`, 提交日期 2026-09-29, 已包含 26.1 目录及其打包配置. 已审校子集另存独立覆盖包, 其余仓库资源仍未全量构建或验证. 后续继续核对仓库分支/版本和打包继承规则, 保留上游署名及 LICENSE; 本项目人工修订优先. 原下载包仍保留在工作副本中, 仅供复现旧版覆盖和差异审查, 不是新的 CFPA 基线.

项目已迁移至当前目录. 原项目、游戏实例和现有 CFPA 均未删除或修改. 安装记录见 `migration-installed.json`, 检查结果见 `localization/reports/project-migration-verification.json`. 迁移时补齐了任务章节结构, 用于正确统计可见章节进度.

整合包特色内容正在按小批次翻译并及时落盘: 当前第 001-004 批记录与未完成项见 [特色内容进度](localization/custom/README.md), 不以已有语言键全覆盖代表图片菜单、对话资源或游戏内验收已全部完成.
