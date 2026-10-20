# FTB Evolution 2 1.4.1 汉化更新检查

检查日期: 2026-10-20. **需要更新汉化, 当前 1.4.0 产物不能标为已适配 1.4.1.** 本次只检查和记录, 未修改实际游戏目录, 未重绑旧清单, 未构建或安装新版汉化, 未进行游戏内验收.

## 版本与方法

`project.json` 的目标实例现为 FTB Evolution 2 **1.4.1**, FTB 版本 ID `100567`. `instance.json.bak` 记录上次版本为 1.4.0 / `100566`. Minecraft 仍为 26.1.2, NeoForge 仍为 26.1.2.121; 项目及各组件基线仍为 1.4.0.

扫描当前 425 个顶层 JAR 和 130 个嵌套 JAR, 读取英文语言、手册、目录/元数据及 KubeJS 同路径覆盖; 与保存的英文快照、源清单、已审校来源及本地安装记录比较. 嵌套依赖包含 `META-INF/jarjar/` 和 `META-INF/jars/`. 同名语言键按确定性文件顺序比较, 不替代游戏实际加载优先级验证. 不读取旧 Prism 实例.

可复现命令: `python localization/assess_pack_update.py`. 明细见 [机器可读检查报告](update-1.4.1-assessment.json). 普通语言的历史清单未完整纳入嵌套/开发示例资源; 本次新观察到的键不能直接当作版本新增数量或待译数量. 历史完整模组清单未能从官方 API 补取 (HTTP 403), 因而不提供未经证实的完整模组更新总数.

## Changelog 补充核对

后续对用户提供的 48 条更新说明进行交叉检查, 另发现洒水壶任务的英文未变但机制已变: 新版禁止模拟玩家使用, 任务仍称点击器可代用. 因此除下述字符差异外, 还需增加 1 个任务说明勘误. 详见 [Changelog 对照报告](update-1.4.1-changelog-review.md) 和逐项证据.

## 任务书: 新增 3 键, 修改 4 键

旧版 4,178 键中 4,174 键英文不变, 4 键修改, 无删除; 新版共 4,181 键. 6 个语言文件受影响.

| 章节 | 变化 | 汉化处理 |
| --- | --- | --- |
| Gearing Up | 新增 `task.2E0873C81D7EC881.title`: Any Gun Modifier | 补译任务标签 |
| Logistics | 新增 `quest.263A989631CE6F13` 的标题和说明 | 补译 Nodeworks CPU 发热、冷却及邻接加成说明 |
| Ars Magica | 每级魔法提升的魔力池从 25 改为 50 | 更新数值 |
| EvilCraft | 区分移除附魔和移除诅咒的流程 | 更新 3 桶/1 桶血、Blook 使用条件、复仇镐限制 |
| Neo Vitae | 血弹从无弹匣射击描述改为替代弹药完成换弹 | 更新机制说明 |
| Replication | `ptinyd` 修正为 `prints` | 既有中文已按打印理解, 可复用译义, 更新源绑定 |

另有 **8 个既有任务结构文件变化**, 包括 Logistics, EvilCraft, Gearing Up 等. 后续只合并中文语言与必要标签, 保留新版任务结构, 不用旧结构覆盖.

## 整合包特色文案与安装状态

整合包 `ftb` 英文语言新增 **3 个冷却方块名称**: Adamantite Coolant, Aeternium Coolant, Aurichalcum Coolant. 与新增任务的名称同步处理; 既有 1,160 个键源文不变.

当前本地安装记录列出的 126 个文件中, **6 个文件与安装哈希不符**:

- `datapacks/ftb/data/ftb/dialog/issues.json`
- `datapacks/ftb/data/ftb/echo_definitions/wandering_merchant.json`
- `kubejs/server_scripts/systems/echoes/shop_keepers.js`
- `kubejs/server_scripts/systems/ftb_events/commands.js`
- `kubejs/server_scripts/systems/ftb_events/events/event_treasure_goblin.js`
- `kubejs/server_scripts/systems/spawn_pyramid/commands.js`

这些文件当前匹配已保存的英文原版源哈希, 表明原有汉化输出已被还原为英文源, 不是发现了六份新英文逻辑. 已有译文可在新版源与安装清单复核后重新应用. 自定义批次所列 44 个文件/脚本输入中, 43 个匹配旧英文源, 其余 1 个是新增冷却名称的 `ftb/lang/en_us.json`.

旧 1.4.0 资源包 ZIP 仍被选中, 其文件哈希与安装记录一致. 这仅说明旧包仍存在并启用, 不代表覆盖了新版新增内容或已通过游戏内验收.

## 手册

对核心、补充、CFPA 与 Patchouli 共 1,381 条源文件记录进行比较 (不同清单可能重复引用同一资源, 不将记录数当作独立页数). 排除 CRLF/LF 差异和既存覆盖差异后, **8 篇已维护手册源文发生变化**:

- Nodeworks 2 篇: `items-blocks/recipe_sets.md`, `lua-api/card-handle.md`.
- Nautec 6 篇: `getting_started/deep_oceans.md`, `eye_of_the_sea.md`, `stronger_beams.md`, `utilities.md`, `laser_chemistry/budding_prismarine.md`, `mixer.md`. 包括海晶石母岩生成位置、海之眼生物群系搜索范围、混合器束流与批量加工机制等实际变化.

对照既有页面路径清单另发现 **4 篇英文页面候选**: LTX Industries 的 `fundamentals/upgrade_station.md`, Nautec 的 `deep_engineering/abyssal_enchanter.md`, `deep_sea_reservoir.md`, `laser_chemistry/osmosis_filter.md`. 需检查新版自带中文及既有来源后确定补译量.

另有 8 篇 LTX Industries 的 KubeJS 手册英文覆盖变化 (工具及 7 篇武器页). 它们不在上述 8 篇已维护翻译源变更中, 需核对新版官方中文与组件支持, 不直接计为 8 篇待译正文.

发现两个**既存有效源绑定差异**, 不计为本次新增: Animal Pen 的鹦鹉页和 Productive Bees 的采石蜂页. 当前 KubeJS 英文覆盖与项目工作副本一致, 但与 Patchouli 原 JAR 源清单不同. 后续应按整合包实际覆盖源复核, 不能直接把原 JAR 清单视作有效英文.

356 条 CFPA 手册来源记录源哈希保持匹配. Nodeworks 硬编码 UI 继续按既定范围保留英文.

## 普通语言与来源绑定

历史全局英文清单内观察到 **5 个同键英文变化**:

- Crystalix: 法杖属性提示的默认值从 false 改为 true.
- LTX Industries: 两条死亡提示改变格式参数与措辞, 其中 lightfrag 从 3 个参数改为 2 个.
- Integrated Terminals: 两条合成计划状态说明从“不允许配方”改为“目标不接受输入并稍后重试”的含义.

需按对应命名空间和实际含义更新译文, 特别检查死亡提示的参数编号; 不用旧格式字符串直接覆盖.

Nautec 新机器、Productive Bees、Integrated Terminals 等另有新观察到的语言键. 明细保留了原文、来源和自带中文候选, 尚未逐项审校 CFPA 跨版本/PR, 不将候选数作为精确待译数. 共享附魔等级键、元数据和嵌套依赖等也不能都计为新增正文.

**42 个普通语言批次的 JAR 绑定失效**, 主要是原文件名已不存在. 这些是需要重新核对的批次数, 不等于 42 个模组或 42 条译文错误. 任务名称的 Companion 依赖链接、客户端模组名映射、近期反馈清单和 CFPA 版本断言也需重新适配. 不为获得通过结果而改名伪装旧 JAR 或直接替换哈希.

## 静态检查与后续顺序

已执行 `python project.py check`: **334 项检查, 278 通过, 56 失败**. 完整命令和错误输出保存于 [静态检查结果](update-1.4.1-static-check.json). 旧历史报告保持原状. 失败包含旧 JAR/链接缺失、源文变更、原生解析结构变化及明确的 1.4.0 版本断言; 不能据此声称 56 处翻译错误, 也不能声称新版全量通过.

后续按任务书 → 整合包特色内容 → 关键手册 → 普通语言 → 其余手册适配. 完成源文差异审阅后更新快照与绑定, 保留可复用译文及已有术语裁决, 重新构建和全量检查, 再生成 1.4.1 发布产物并按清单安装. 游戏内显示、任务悬停、手册链接/组件、资源加载及交互仍需单独验收.
