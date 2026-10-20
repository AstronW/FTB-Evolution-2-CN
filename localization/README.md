# FTB Evolution 2 任务书汉化

当前任务书目标已更新为 **1.4.0**: 51 个语言文件, 4178 个语言键, 8181 个含英文的源文本片段, 42 个可见章节均已覆盖. 新增 Replication 章节及 Witchery 任务, 补充 Oritech 故障说明, 移除新版已删除的 Power Armor 任务文本. 见 [1.4.0 适配记录](reports/quests-1.4.0.md) 与 [当前进度](PROGRESS.md). 尚未安装到真实游戏或进行游戏内验收. 下文 50 文件/41 章节等数字为 1.3.2 历史完成记录.

标点约定见[STYLE.md](STYLE.md). 已有任务书及手册译文统一使用英文标点, 后续译文同样遵守并由构建工具检查.

手册汉化另见[手册完成记录](manuals/README.md). 已覆盖四本整合包指南, FTB工业奇械, Nodeworks, 以及本轮 1.4.0 剩余 305 篇 Markdown/MDX 手册; 批次范围与验收状态见[剩余手册批次](reports/manual-extra-1.4.0.md).

当前整合包全部任务书文字翻译已完成。50个语言文件已生成，全部41个可见章节均已覆盖；静态验收见[最终检查记录](reports/final-audit.md)。游戏内排版、悬停及链接点击尚未实测。

原文有50个JSON5文件、4,142个键、8,122个含英文的可见文本片段，其中44个文件位于chapters目录；实际任务目录显示41个章节，另有3个额外文件。以当前原文件为准，全部纳入翻译范围。

当前进度见[自动生成的进度表](PROGRESS.md)。该表在每次build或check时更新，不使用手动维护的阶段统计。

## 文件和约定

- 英文源：`.minecraft/config/ftbquests/quests/lang/en_us/`，不修改。
- 中文输出：同级`zh_cn/`；只有完全翻译的单个文件才会生成，其他章节暂时回退英文。
- `translations/`：人工翻译数据，每个文件内使用从0开始的片段编号。编号由原文顺序决定，先使用show命令读取，不能凭旧编号修改已更新的源文件。
- `terms.json`：已确认的完整文本匹配和专名保留表。这里只做完整字符串匹配，不对英文词片进行全局替换。包含本地语言文件用语及本项目选定的章节名，并不等同于CFPA官方术语表。
- `source_manifest.json`：首次开始翻译时的英文文件SHA-256，防止版本更新后误用旧片段编号。
- `reward_labels_source.json`和`reward_labels_zh_cn.json`：任务书引用的45条定制奖励语言键。构建时合并到`.minecraft/kubejs/assets/ftb/lang/zh_cn.json`，保留该文件的其他键。
- `quest_item_names.json`：38条FTB挑战组件及相关名称/描述，保留原JAR语言文件的英文来源，构建时核对并合并到上述中文覆盖文件。
- `quest_extra_labels.json`: 1.4.0 任务书直接依赖的 5 条名称覆盖, 绑定 `.minecraft/quest-inputs/` 中的源语言快照和 SHA-256, 由任务书构建及独立检查同步验证. 其中物质百科覆盖写入 Replication 命名空间, 其余写入 FTB 命名空间.
- `reports/progress.json`：按文件记录剩余片段，实际进度以这里和当前中文输出为准。
- `reports/source_corrections.md`：有本地配方或JAR代码证据的原文勘误；英文源不改动。
- `reports/verification.json`：独立的结构检查结果及保留英文的逐项清单。

提取片段时会解析内嵌JSON文本组件，仅翻译可见文字和show_text悬停文本。点击动作、任务目标、URL、按键绑定、translate语言键、样式等不交给译者修改。空行、图片指令、分页符保持原样。不要把仍需翻译的完整英文段落加入保留表。

现有中文应优先遵循当前游戏的实际名称，例如：FTB工业奇械、神秘学、原初浆凝胶、核源铁、虚空框架、无限粉、硅、末影板、荧光杖、水澜泵、Fortron衍生器。没有可用中文的模组专名可以保留英文。共鸣模组当前没有自带中文，本项目采用谐振者、共鸣潜猎者、水晶怨灵等译名，后续需保持一致。

## 工作命令

在实例根目录运行：

```bash
python localization/quest_translation.py show chapters/power.json5
python localization/quest_translation.py show chapters/power.json5 0 80
python localization/quest_translation.py build
python localization/quest_translation.py check
python localization/verify_quests.py
java --class-path .minecraft/.cache/jij/2e0f73784e6bc4c755e52d485f628d110d397f079d58b118658b903be9aa0533/json5-java-3.0.0.jar localization/ValidateJson5.java .minecraft/config/ftbquests/quests/lang/zh_cn
```

build会验证英文源清单、颜色码、占位符等，并生成完整文件。check核对生成文件与翻译数据完全一致。verify_quests独立核对键、段落、内嵌组件动作/样式、资源ID、命令、奖励占位符等。Java程序用当前FTB Library依赖的json5-java 3.0.0解析中文文件并检查跨文件重复键。Java解析通过不代表已进行游戏内版面和点击操作测试。

每批写入后执行检查，查看保留英文清单，确认只有模组名、人名、命令、按键等有意保留的内容。不能只看所有文件存在就宣告完成；全部可见文字必须经过翻译或明确有理由保留。

## 完成状态

全部章节、额外章节文件、目录和奖励文本均已覆盖。另补充45条定制奖励标签，以及38条任务组件及相关名称/描述。原始英文、任务ID、依赖、奖励结构、配方和玩家进度保持不变。

已完成全量保留英文审查、数字差异复核、重复短文本译名检查，以及结构和JSON5解析检查。原文存在且有本地证据的错误，单独记录在source_corrections.md。

当前未重启或控制游戏，未进行分页、悬停和链接点击实测。游戏仍显示旧文本时，请重新加载资源与任务书，或重启客户端；有权限时可使用FTB Quests的reload命令。更新整合包后，先对照英文源清单处理变化，再重新生成，不要直接复用旧片段编号。
