# 有证据的原文勘误

## 1.4.0 CFPA 复用期间核实的勘误

- Mystical Agriculture 的 `SlowFallingAugment` 当前构造器使用 `AugmentType.BOOTS`, 非潜行时施加 `MobEffects.SLOW_FALLING`. 手册英文所说护腿与阻止缓慢均不符代码; 中文改为靴子并获得缓降. 字节码和 JAR 哈希见 `../cfpa_review/code-evidence/slow-falling.txt` 与 `../cfpa_review/code-evidence/jar-manifest.json`.
- Witchery 的 `TornPageItem.use` 消耗残页, 解锁 `vampire/1..9` 进度并显示 `witchery.add_page.*`; 指南页面条件绑定相同研究门槛, 未向钥匙物品写入页面. 中文消息据此为已解锁相应页面, 不照搬源文不明对象 key. 证据见 `../cfpa_review/code-evidence/torn-page.txt` 与 `vamp_1.json`.
- Productive Bees 煤炭蜂当前配方 `data/productivebees/recipe/bee_breeding/coal_bee.json` 的亲本为 `magmatic` 与 `leafcutter_bee`; 手册中的 Blazing/redstone 不符. 中文采用对应当前配方的岩浆蜂与切叶蜂, 保留逐项格式例外及来源记录.
- AE2 输出总线页末尾错误引用 `import_bus` 配方, 本地中文使用同页实际对象 `export_bus`. 频道页三条致密线缆的容量为 32×3=96, 修正英文 92 的算术错误. 详细当前源差异及裁决见 `../cfpa_review/manuals-notes.md`.

以上均只修正本地汉化文案或展示引用, 不修改原英文, 模组 JAR, 配方或玩法逻辑.

## 1.4.0 Replication 介绍中的拼写错误

- `chapters/replication.json5` 的 `quest.095B11E487F642F2.quest_desc` 首段原文为 `Replication ptinyd items out of raw matter`.
- 同段后句明确写出 `the network can print copies on request`, 后续任务也说明分解, 扫描和复制流程. 中文按上下文译为用原始物质打印物品, 不将 `ptinyd` 当作术语保留.
- 英文源文件和哈希保留原样; 新源快照见 `.minecraft/config/ftbquests/quests/lang/en_us/chapters/replication.json5`.

## Powah岩浆发电机每桶熔岩产能

- 英文能源总览（chapters/power.json5）第5个片段（从0计）写每桶10,000 FE。
- 英文Powah专章（chapters/powah.json5）第5个片段写每100 mB产出10,000 FE，即每桶100,000 FE。
- 当前Powah-7.0.4-alpha.jar内data/powah/data_maps/fluid/magmator_fuel.json给熔岩设置energy_produced=10000。
- 同JAR的owmii.powah.block.magmator.MagmatorBlockEntity.postTick字节码以100 mB为一份，能量为实际消耗量×energy_produced÷100。因此每桶应为100,000 FE。
- 本地datapacks与KubeJS目录未发现对应magmator_fuel覆盖文件。
- 中文能源总览已拆开说明：Powah为100,000 FE，另两种熔岩发电机保持原文的10,000 FE。英文源与游戏数据未改动。

## Energized Power合金炉炼钢用煤量

- 英文getting_started.json5片段216写合金炉每锭需要三个煤，与energized_power.json5片段65的一个煤矛盾。
- 当前整合包datapacks/ftb/data/energizedpower/recipe/alloy_furnace/steel_ingot.json明确要求一个铁锭标签物品和count=1的煤炭标签物品。
- 中文入门任务已按当前数据包更正为一个煤，英文原文和配方未改动。

## 神秘学彩虹粉笔的替代范围

- 英文occultism.json5片段160写可替代非基础粉笔，但括号列出白、灰、淡灰、黑这四种基础粉笔；片段165又把替代基础粉笔当作虚空粉笔的升级能力。
- 当前occultism-26.1.2-neoforge-1.256.1.jar的英文语言键book.occultism.dictionary_of_spirits.crafting_rituals.craft_master_chalks.spotlight.text明确写彩虹粉笔可替代任意粉笔；spotlight2.text说明虚空粉笔能力与彩虹相同，仅变色范围为白至黑。物品自身auto_tooltip也写可替代任意粉笔符文。
- 中文160明确包含基础粉笔，165说明两者替代能力相同。英文与游戏数据未改。

## 2026-10-18 喷气背包任务模组误指

`chapters/tips_and_tricks.json5` 的源文 `&aSimply Jetpacks&r adds flight without needing to get an &dElytra&r.` 指向当前实例不存在的模组名. 1.4.0 实际安装 `IronJetpacks-26.1.2-9.0.3.jar`, 命名空间 `ironjetpacks`, 元数据名 `Iron Jetpacks`. 按玩家反馈更正为 `&a铁制喷气背包&r让你无需获得&d鞘翅&r也能飞行.`. 保留原始英文源, 不改任务结构与飞行机制. JAR 哈希及版本绑定见 `../client_fixes/mod-names.json`.
