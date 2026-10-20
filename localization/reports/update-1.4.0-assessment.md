本次从 FTB Evolution 2 1.3.2 更新到 1.4.0, 属于增量适配, 大部分现有译文可以复用. 当前仅完成检查, 未修改 FTB 新实例, 未在游戏中验证.

旧实例: `/home/astronw/.local/share/PrismLauncher/instances/FTB Evolution 2/.minecraft`.
新实例: `/home/astronw/.ftba/instances/ftb evolution 2`.
版本证据: [旧实例配置](../../instance.cfg), [新实例配置](/home/astronw/.ftba/instances/ftb%20evolution%202/instance.json). Minecraft 仍为 26.1.2, NeoForge 仍为 26.1.2.121.

| 范围 | 比对结果 | 适配工作 |
|---|---|---|
| 任务书 | 4139 个键源文不变, 修改 1 个, 新增 38 个, 删除 2 个 | 合并旧译文, 翻译增量, 按新版结构重新生成和验证 |
| 已完成普通语言批次 001-018 | 10451 个选定键源文不变, 1 个仅删除末尾空格, 174 个不再出现在原语言文件中 | 大部分复用, 更新版本绑定和源清单, 核对 174 个熔融材料键的实际用途 |
| 已翻译 GuideME 手册 | 164 页有效源文全部逐字相同, 无新增页, 4 个自定义入口定义也相同 | 可复用页面及入口, 迁移后检查资源优先级和原生解析 |
| 整合包自定义语言 | 原 1407 个源键中 1394 个不变, 12 个修改, 1 个删除; 新增 9 个 | 更新进度条件和新增物品/仪式文本 |
| 运行时提示 | 已翻译的 4 个脚本与新版未翻译脚本 SHA-256 全部相同 | 可以复用已有提示修改和 ftb_custom 语言文件 |

任务书新增 Replication 章节: 35 个键, 63 个可翻译片段. 章节目录新增 1 个标题片段, Witchery 新增 2 个键/5 个片段, 合计新增 38 个键/69 个片段. Oritech 的粒子加速器任务增加了磁场和速度传感器暂不可用的缺陷说明. Gearing Up 删除一个任务的 2 个语言键. 有 11 个既有章节结构文件发生变化, 因而迁移时只能合并中文语言文件, 不能用旧任务结构覆盖新版. 新版语言键共 4178 个.

自定义语言的 12 处修改均为 Apotheosis 装备进度条件, 新版明确要求 Base Armor Toughness, 译文需要补上基础护甲韧性的含义. 新增 9 个键包含 Replicophiles, Meat Ingot 和召唤集会女巫的名称/仪式/手册说明; 其中 1 个值为空, 不应算作一条正文. Power Armor 的创造电池键随模组删除, 应移出有效范围. 自建 ftb_custom 的 34 个键不是上游删除项, 需要随提示脚本迁移.

已完成普通语言模组中, Hephaestus Tools 新增 9 个键, Stellaris 新增 27 个键. Stellaris 原有的一处变化仅为尾随空格, 不涉及译义. Witchery 的一条死亡信息修正英文拼写, 不在此前选定的补缺范围内, 应检查上游中文是否需要调整. Companion 从原文件移除 174 个熔融材料名称, 不能仅据此判断物品也被删除, 应在注册和运行时显示核对后决定保留兼容键或清理. Nodeworks 和 Roots Classic 的 JAR 未变, 原有绑定这些版本的勘误证据仍可复用.

两个实例各有 421 个启用的顶层 JAR, 400 个内容相同, 18 个更新. 新版增加 Replication 和 Collapsible Groups, EuphoriaPatcher 从旧实例的禁用状态转为启用. 旧实例额外安装的 I18nUpdateMod 未出现在新版中, Power Armor 和 PortingDeadLibs 也未出现. 具体模组及源文差异见 [机器可读明细](update-1.4.0-assessment.json).

| 新增模组语言 | 英文键 | 模组自带中文 CJK 候选覆盖 | 旧 CFPA 也未补上的候选 |
|---|---:|---:|---:|
| Collapsible Groups | 475 | 0 | 475 |
| Replication | 84 | 72 | 12 |

Collapsible Groups 是 JEI 分组管理工具, 不属于用户排除的装饰类模组. 475 个键对应 428 个不同英文值, 建议作为新版适配的优先批次. Replication 的 12 个非中文候选中包含可保留的模组专名, 实际需要新译的正文少于 12 条.

所有模组原生英文键合计增加 650 个. 使用新版自带中文和旧 CFPA 静态检查, 其中 542 个新增键没有 CJK 候选, 包含普通语言及手册语言键, 不可直接当作 542 条待译正文或加到旧剩余量中. Neo Vitae 有 23 条源文更新, Animus NV 有 5 条, 涉及护甲升级说明, 采矿仪式范围和血弹消耗逻辑. 即使既有 CFPA 含中文, 也需复核是否陈旧. Nautec 的 3 个变化是跨模组共享多方块错误提示的全局覆盖变化, 不是其专属语言文件变化. 精确剩余量应在新版 CFPA 合入并重新扫描后给出, 旧版 11475 个缺失键不能直接沿用.

按用户最新要求, CFPA 改为从 [官方 GitHub Releases](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/releases) 下载后随汉化包提供, 不以安装 I18nUpdateMod 为前提. 旧转换包的元信息表明其合并了 1.21 与 26.1 资源, 新方案同样需要两层, 不能只下载很小的 26.1 包就视为替代完整旧覆盖. 已记录公开发布资源及 SHA-256: [sources.json](../vendor/cfpa/sources.json). 下载入口为 `python localization/fetch_cfpa.py`, 会验证 SHA-256 和 ZIP CRC, 保留上游原始压缩包, 下载成功不代表已经合入.

当前环境终端网络被禁用, GitHub 下载尝试失败于 DNS 解析, 尚未下载或合入新版 CFPA. 来源版本已通过官方 GitHub 发布页面核对: [1.21 资源](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/releases/expanded_assets/Snapshot-20260929014058), [26.1 资源](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/releases/expanded_assets/Snapshot-20260917125024). 最终包应保留 CFPA 署名与许可证, 本项目修订译文优先于 CFPA, 继续遵守英文标点约定. CFPA 原始文件应独立保留, 转换和标点调整只作用于构建产物, 并验证 JSON/Markdown 结构和格式参数.

建议后续顺序: 获取并锁定 GitHub CFPA 源资源, 在新版源文上合并任务书与语言覆盖, 补齐本次任务书/自定义提示增量, 复用 164 页手册和 4 个提示脚本, 再补译 Collapsible Groups 等新增语言, 最后重新扫描剩余量并进行游戏内验证. 现有构建工具多数把 `.minecraft` 和旧 JAR 文件名写死, 迁移前需支持新游戏根目录并更新清单. 第 019 批只有提取草稿, 未视作已完成译文. 本次未恢复此前暂停的普通语言翻译目标.
