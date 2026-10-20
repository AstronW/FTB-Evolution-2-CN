# CFPA 跨版本与 PR 审校复用

目标为 FTB Evolution 2 1.4.0 / Minecraft 26.1.2. 本次已逐项审校并构建本地覆盖包, 未写入真实游戏实例, 未进行游戏内测试. 当前产物是适用子集, 不是整份 CFPA 或全部 PR 的合并.

## 完成范围

| 内容 | 纳入产物 |
| --- | ---: |
| 语言键(普通文本及语言键型手册) | 7304 |
| 独立分组名称 | 76 |
| Markdown/MDX 手册 | 205 页 |
| Patchouli 可见字段 | 508 个, 合并至 151 份当前 JSON |

语言与分组共审查 7555 个候选, 540 条采用来源键不同于目标键的映射, 2246 条有本地修订(包含标点规范, 不全部视为语义错误). 所有候选均保存接受/拒绝结论及来源; 对象, 数值或操作变化按当前版本修订.
采用 21 个 PR 的部分条目, 保留作者及 head SHA, 讨论快照见 `pr-discussions.json`. 原文一致不自动视为正确, 未合并或无评论也不代表已获批准. 来源目录覆盖 1.12.2, 1.16, 1.18, 1.18-fabric, 1.19, 1.20, 1.20-fabric, 1.21, 1.21-fabric, 26.1.

## 主要修复与术语

- 修复塔罗牌重复百分号, 动物饮水槽对象错误, 物品/能量/流体描述反向, 延迟器新旧值, 邀请与踢出方向, 左右方位, 段落移位及条件增译.
- 规范 Collapsible Groups 的折叠/分组概念, Cable Tiers 等级, GeoOre 生长阶段, 动态联合值类型与运算符, Neo Vitae 流体名. AE2 耗时分析仪的物品, 界面和手册名称已同步. 详见 `terms.json` 与上级 `TERMINOLOGY.md`.
- 手册修复 CPU 漏译, 样板供应器阻挡模式误译, 页面链接, 宏, 表格与当前版本组件; 补齐少量新增说明, 不以旧版 JSON 整页覆盖当前结构.
- 当前代码核实了 Witchery 残页解锁与 Mystical Agriculture 缓降升级的英文勘误; 配方与字节码证据见 `code-evidence/` 及上级 `reports/source_corrections.md`. 不修改英文源或实际机制.

## 未采用的部分

4 个范围内语言键仍暂不采用:

- `book.witchery.guidebook.ritual.bind_spectral_creatures.bind_spectral_creatures.text`: 当前英文举例为 Trent Effigy, 候选替换成黏土塑像(Clay Effigy). 尚无证据证明这两个名称在当前版本指同一塑像, 不把潜在机制名称错误计为完成.
- `info_book.integrateddynamics.tutorials.logicOperations.text5`: 语言键发生段落移位: 旧 text5 是惰性求值段, 当前 text5 是重新编辑变量卡说明, 候选无可复用正文; 不以错位段落替代新段落.
- `info_book.integrateddynamics.manual.logic_programming.text4`: 语言键对应正文已变: 旧段只介绍搜索和筛选, 当前是加载并修改现有变量卡的操作步骤; 无可复用主体, 留待新译.
- `info_book.integrateddynamics.manual.logic_programming.text6`: 语言键对应正文已变: 旧段是方块/物品形式切换, 当前是有命名器时点击 E 立即命名; 无可复用主体, 留待新译.

另剔除 171 个排除范围候选: 164 条属于 Macaw 等建筑装饰分组, 其余为元数据或未确认玩家用途的诊断文本. 另 1 页量子合成器终端在当前源中已禁用, 不生成其中文页面. 这些不作为已完成译文凑数.

## 维护与构建

- `decisions/*.json`: 当前可维护的逐条语言/字段裁决, 原始候选嵌于 source, 禁止用只看汉字覆盖率替代审校.
- `manuals/files/`: 已审定的完整 Markdown 页面, 与决定中的 SHA 绑定. `manuals/review.py` 仅为本次初稿辅助, 不是构建入口, 不运行它覆盖最终裁决.
- `inputs/`: 本阶段审校范围和审校前剩余量快照. `inputs/manual-source-manifest.json` 同时绑定原始与 LF 规范化源文哈希, 不静默覆盖源变化.
- `build-manifest.json`: 受工具管理的资源清单, 输出哈希, 裁决文件哈希及逐项格式例外.
- `verification.json`, `negative-checks.json`, `manuals/native-input-hashes.json`: 输出完整性, 结构与源文校验, 拒绝缺裁决/改源文/改占位符的负向检查及原生解析输入绑定.

在项目根目录运行:

```bash
python localization/cfpa_review_build.py build
python localization/cfpa_review_build.py check
python localization/cfpa_review/manuals/validate_native.py
python localization/verify_cfpa_review.py
python project.py check
```

覆盖目录为 `.minecraft/resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN/`, ZIP 为 `dist/FTB-Evolution-2-1.4.0-CFPA-Reviewed-zh_CN.zip`, 附 `.sha256`. ZIP 可重复构建, 根目录直接含 pack.mcmeta 和 assets, 不含模组 JAR. 校验通过不等同于已安装或启用.

真实安装时应按资源加载优先级检查本包与 CFPA 基线, 原有项目人工修订的关系; 不复制整个旧 KubeJS 或任务结构到新实例. 当前仅提供项目产物, 没有自动修改游戏 options.txt.

## 验证边界

205 页英文与 205 页中文使用当前 GuideME 原生解析器成功解析, 12 个含表格页面的结构一致. AST 未解决差异为零; 3 项已审定显示差异与 4 项保护结构勘误单列保留. Patchouli 只合并审定字段及原有中文, 所有其他动作, 资源 ID, 配方组件和 JSON 结构沿用当前英文源. 数字文字等价, 悬停正文与真实源文勘误逐项列明例外, 不使用全局豁免.

静态验证仍不能替代游戏内翻页, 搜索, 动态场景, 中文导航, 按键提示和排版验收. 尚无中文候选的普通文本和其他手册没有借本阶段展开翻译. 最新剩余量见上级 `reports/remaining-1.4.0-summary.md`.

## 来源与许可

CFPA 固定提交为 `719672954d9df4ea51877e3d5ce2912148273682`, 原仓库和 PR 缓存不改. 产物包含 CFPA LICENSE, 逐来源 ATTRIBUTION 以及 Animal Pen 原生修复条目的原许可文件. Animal Pen 的模组元信息标为 GNU GPL 3.0, 作者 BONNe, 不把这部分原生译文改标为 CFPA 许可. 本包说明只标注各来源和修改, 不声称整个混合产物适用单一许可证.


## YAML 元数据最终校验

使用当前 GuideME 内置 SnakeYAML 解析全部英中前置元数据, 并比较导航父节点, 图标, 分类和物品 ID 等非显示字段. 只允许标题/描述/提示文本不同. 半角化引出的标题冒号和引号问题已修复, 203 页可见标量统一安全引用; 详见 `manuals/yaml-quoting-repairs.json` 与 `manuals/yaml-metadata-review.json`. 同一实际错误模式的负向用例会被原生解析器拒绝.

## 归档校验口径

`build-manifest.json` 用 `archive_content_sha256` 记录归档身份, 即按文件名排序后逐成员记录其 SHA-256, 而不是 ZIP 的字节哈希. 不同 zlib 版本重新压缩会改变 ZIP 字节但不改变内容, 字节哈希会让 `check` 在换机或升级 Python 后误报 "Reviewed data changed". 现在 `check` 会逐成员比对归档内容与 `files` 清单, 并校验归档可读性与成员集合, 覆盖范围不弱于原先的整包字节相等. `dist/` 的 `.sha256` 仍记录实际 ZIP 字节哈希, 供分发核对.
