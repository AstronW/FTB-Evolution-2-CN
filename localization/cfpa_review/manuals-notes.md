# CFPA 手册候选审校与当前版本适配

目标为 FTB Evolution 2 1.4.0 / Minecraft 26.1.2. 本批属于既有 CFPA 候选审校复用, 不表示所有手册已翻译完成. 仅在项目维护覆盖, 未写入目标游戏, 未做游戏内验收.

## 审校结果

逐单位决定见 [decisions/manuals.json](decisions/manuals.json), 共 714 条: 接受 205 个 Markdown/MDX 文档及 508 个 Patchouli 字段, 拒绝 1 个已禁用文档. 文档来源英文相同 74 页, 变化 132 页(其中 131 页完成复用适配, 1 页拒绝); Patchouli 来源英文相同 502 字段, 变化 6 字段全部完成映射或适配.

| 文档命名空间 | 接受页面 |
| --- | ---: |
| ae2 | 126 |
| extendedae | 45 |
| advanced_ae | 12 |
| appflux | 12 |
| ae2wtlib | 7 |
| ae2netanalyser | 2 |
| little_big_redstone | 1 |

| Patchouli 命名空间 | 接受字段 |
| --- | ---: |
| productivebees | 245 |
| modularrouters | 221 |
| laserio | 41 |
| justdirethings | 1 |

来源范围包括 CFPA 1.20、1.21 和固定 PR 文件, 目标按决定中 `source.target_source` 的当前 JAR 或整合包覆盖逐项核对, 不是整文件跨版本覆盖. CFPA 仓库固定提交为 `719672954d9df4ea51877e3d5ce2912148273682`, 路径、作者及版本保存于每条决定中. 上游许可证见 [CFPA/LICENSE](../../CFPA/LICENSE), 本地格式、内容修订以 `changes` 单列保留.

## 当前源变化及实质修订

- AdvancedAE 量子合成器终端当前 JAR 将整页注释禁用, 拒绝旧版中文页面, 不恢复已下线功能. 拒绝行保留来源与理由, `files/` 不输出该页.
- AE2 输入输出卡页新增方块选取卡, 补齐当前源的说明、图片、配方与导航 item ID. 当前物品 `ae2:chest` 更名为 `ae2:me_chest`, 对组件引用定向修正.
- 当前导航、分类及资源 ID 以当前英文 frontmatter 为准, 只继承可见中文 title. ExtendedAE 的大部分变化是英文语法、大小写与标点润色; AppFlux 与网络分析器等 14 页仅行尾/空白变化, 不重译正文.
- Modular Routers 安全升级 4 个字段由旧页 3/4/5 映射到当前页 2/3/4, 每个字段的当前英文与旧字段英文完全相同; 另有路由器说明的英文冠词修正. Productive Bees 采石蜂已改为复制造访方块, 删除旧版碎片机制并按当前正文适配.
- 修复 AE2 合成 CPU 漏译的单 CPU 单任务与并发示例两段, 神秘方块配方段遗漏, 样板供应器缺失的子部件链接及错误的“只有阻挡模式才可用”含义, 保留源文硬换行. 终端页补齐当前空手取流体行为及 regex 说明.
- 修复 ExtendedAE 未长成的恩特罗芽才掉碎片的漏译否定, 样板误写为样本, 罐装机资源/容器槽位歧义和标签过滤表达式代码格式. 修复 LaserIO/Modular Routers 明显错字及重复词, 保留术语上下文, 不改上游原件.
- 保留 Patchouli `$(modr)` 宏, 移除 CFPA 额外强调/重置宏, 恢复原外链; `$(t:)` 悬停正文汉化时保留 `ecoTimeout` 与 `lowPowerTickRate` 配置键. 中文正文半角化, 不更改代码、URL、JSX 属性及功能控制码.

以下原文勘误逐项有本地证据, 不更改英文原件或配方:

- Productive Bees 煤炭蜂当前 `data/productivebees/recipe/bee_breeding/coal_bee.json` 的亲本为 `productivebees:magmatic` 与 `productivebees:leafcutter_bee`, 保留 CFPA 岩浆蜜蜂及切叶蜜蜂, 修正英文错误的 Blazing/redstone 链接.
- Modular Routers 破坏模块英文指向不存在的 `router/item_router`, 当前 JAR 实际页面为 `router/modular_router`, 保留 CFPA 可用链接.
- AE2 输出总线当前英文页末尾错误引用输入总线配方, 保留 CFPA 的 `export_bus` 配方组件.
- AE2 频道表 x3 的致密线缆数量英文为 92, 按同页基数 32 与三倍模式算得 96, 保留 CFPA 96; 正文仍保留超过 96 个节点及可能降低耗能的限定.

## PR 审查

- [#5997](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/5997), ChuijkYahus, head `fd82280f683803bcbe917ad7f96fc6c1ef0500e2`: 采用 Little Big Redstone 信号源页. 修复原 PR 从计数器页复制的错误说明, 以及当前配方组件从 `RecipeFor` 到 `Recipe` 的变化. [缓存](pr-discussions.json)只有自动信息, 未发现人工意见, 不视作上游批准.
- [#5734](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/5734), 48004800, head `e3e00543c98952eaa407e15f508da2d401b3e56e`: 采用 Productive Bees `bees/wild/draconic.json` 的 1 个同源字段. 已检查 [人工审查缓存](pr-human-discussions.json)中的手册建议, 涉及其他页面, 未发现对本字段的直接意见. 不视作上游批准.

## 验证与复现

```bash
python localization/cfpa_review_build.py build
python localization/cfpa_review/manuals/validate_native.py
python localization/cfpa_review/manuals/audit_final.py
```

- [原生解析结果](manuals/native-parser-check.txt): 当前目标实例 GuideME 解析 205 页英文与 205 页中文, 合计 410 页成功.
- [AST 未解决差异](manuals/ast-review.json)为 `[]`. [3 项已审定显示差异](manuals/ast-reviewed-differences.json)保留具体节点计数和理由: 处理器页强调拆分、存储分类页额外强调、终端页将同义槽位说明组织为列表. 未为满足计数删除正文. 12 个含表格页面的每行列数及行数与当前英文一致.
- [结构差异](manuals/structural-problems.json)保留 4 项原始观测, 在 [逐项裁决](manuals/structural-reviewed-differences.json)中给出理由, 不抹掉原始差异.
- 508 个 Patchouli 字段运行 `cfpa_review_format.invariant_errors`. 5 字段的 7 项精确例外为: 数字 1 译作单个/一只、2 项页面/亲本 ID 勘误、可见悬停文本汉化. `validation_exceptions` 中逐项记录错误类别与理由, 实际错误集合必须与例外集合完全相等, 不使用通用豁免.
- [最终检查](manuals/final-verification.json)核对全部源文哈希、当前字段内容、输出存在性、决定唯一性及 PR 署名. Markdown 输出另保存 `chinese_sha256`.

## 集成接口

`decisions/manuals.json` 为列表. 构建器仅消费 `status == "accepted"` 的条目:

- 通用: `namespace`, `format`, `path`(当前英文资源路径), `field`(Markdown 为 null), `source`, `english_sha256`, `output_resource_path`, `changes`, `validation_exceptions`.
- Markdown/MDX: `file` 指向 `localization/cfpa_review/manuals/files/assets/...` 的完整中文页面, 目标相对资源根路径用 `output_resource_path`, 不再次自行推导语言目录; `chinese_sha256` 在最终检查写入.
- Patchouli: `english` 与 `chinese` 为字段值, `field` 为点分路径, 如 `pages.2.text`; 从当前英文 JSON 复制结构, 仅写入本批接受字段, 不将旧 CFPA 整个 JSON 覆盖当前文件. `output_resource_path` 已将当前 `en_us` 改为 `zh_cn`. 保留未采用的现有中文字段时需由主构建器按其已有优先策略合并.
- `source.path`、`english_path` 是固定 CFPA 或 PR 缓存文件, `source.target_source` 是当前 JAR/覆盖文件. `english_sha256` 绑定字段或 LF 标准化 Markdown 正文. PR 另含 `pr`, `author`, `head_sha`, `repo_path`, `discussion_evidence`, `review_status`.

已在总集成阶段将 ME 刻耗时分析仪/性能分析与语言覆盖同步, 并将路由器刻周期表述统一为运行间隔. 原 `review.py` 是初稿辅助脚本, 不作为最终构建入口, 不应运行它覆盖已审定文件.

本批仍需在游戏内检查术语显示一致性, 并在游戏内验证资源优先级、中文导航、页内锚点、表格、动态场景、翻页及链接. 本批静态通过不代表完整手册汉化或游戏内验收完成.


最终集成另增加当前 GuideME 内置 SnakeYAML 校验, 修复半角化标题冒号及引号导致的元数据语法问题. 203 页标题等可见标量安全引用, 非显示元数据与当前英文一致, 详见 manuals/yaml-quoting-repairs.json 和 manuals/yaml-metadata-review.json. 原生解析输入哈希绑定最终中文文件.
