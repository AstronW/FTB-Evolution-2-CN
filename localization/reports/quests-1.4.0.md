# 1.4.0 任务书汉化与验收

目标: FTB Evolution 2 1.4.0 / Minecraft 26.1.2. 仅适配任务书及直接依赖的名称, 其余组件继续保留 1.3.2 基线. 构建产物位于项目工作副本, 未写入实际游戏实例, 未进行游戏内验收.

## 本次完成

- 新增 Replication 章节: 35 个语言键, 63 个可翻译片段, 覆盖矿石获取, 网络布置, 分解, 物质储存, 扫描, 样板, 复制及升级.
- 新增章节目录标题 1 键, Witchery 的巫师会任务 2 键 / 5 片段. 合计新增 38 键 / 69 片段.
- 适配 Oritech 既有粒子加速器任务的新增故障说明, 明确磁场与速度传感器在此版本的缺陷.
- 移除新版已删除的 Power Armor 任务 2 键. 保留其余有效键的既有译文, 并将 4 个旧说明中的金黄粉笔统一为金黄仪式粉笔.
- 补充任务直接引用的 5 个名称覆盖: Replicophiles, Summon Coven Witch 的 3 个名称键, MatterOpedia. 官方中文和 CFPA 的对比裁决见 `../TERMINOLOGY.md` 与 `quests-1.4.0-terms.json`.
- 源文 `ptinyd` 按上下文译为打印, 原英文未改; 证据见 `source_corrections.md`.

## 产物与可复现输入

- 可维护译文: `localization/translations/`; 任务词表: `localization/terms.json`.
- 中文任务书输出: `.minecraft/config/ftbquests/quests/lang/zh_cn/`, 共 51 文件 / 4178 键 / 8181 个已解决源片段, 可见章节 42/42.
- 源文与任务结构已从实际 1.4.0 实例快照到工作副本, 130 个原始文件逐字节一致. 只更新项目副本, 不改实际游戏结构或任务逻辑.
- 旧版原文, 译文映射, 词表与源清单保存在 `localization/archive/quests-1.3.2/`. 增量明细见 `quests-1.4.0-source-delta.json`, 更新后的哈希清单为 `localization/source_manifest.json`.
- `localization/quest_item_names.json` 的 38 个标签已对照新版 Companion JAR 逐项核对原文, 并改绑 `.minecraft/quest-inputs/` 下指向新版 JAR 的依赖链接. 其他组件的旧版 `.minecraft/mods` 依赖保持原用途.
- `localization/quest_extra_labels.json` 保存 5 个补充名称的英文, 中文, 输入快照 SHA-256 和输出路径. 输入快照在 `.minecraft/quest-inputs/`, 构建时校验原文及哈希, 生成到 `.minecraft/kubejs/assets/` 的对应命名空间. 不复制或分发模组 JAR.
- CFPA 的复用保留来源, 上游许可证见 `CFPA/LICENSE`, 为 CC BY-NC-SA 4.0. 本批采用 1.21 版本的“物质百科”名称并用于新版本覆盖, 未改上游原件, 未采用未核验的 PR 内容.

## 验收

在项目根目录执行:

```bash
python localization/quest_translation.py build
python localization/quest_translation.py check
python localization/verify_quests.py
python project.py check
```

任务书构建及独立检查通过. 校验覆盖键与顺序, 段落数量, 内嵌文本组件动作/样式, 资源 ID, 命令, 格式码, 占位符, 英文标点, 奖励标签, 组件名称及新增名称覆盖.

额外对全部 39 个新增/修改键逐叶核对数字与搜索表达式, 包括 `earth>10`, `nether=20`, `quantum<6`, `!earth`, `*metallic`. 对所有源文未变的键核对旧译复用, 仅允许上述 4 项粉笔名称规范化. 结果见 `quests-1.4.0-verification.json`.

使用实际 1.4.0 实例缓存中的 json5-java 3.0.0 运行 `ValidateJson5.java`, 51 文件 / 4178 个语言键解析成功且无跨文件重复键. 结果另存 `quests-1.4.0-json5-parser-check.txt`.

全项目静态检查同时覆盖其他组件的已完成批次, 不代表其他组件已适配 1.4.0. 第 019 批普通文本仍是未完成草稿, 不计入完成范围.

后续安装只采用此阶段已验证的中文文件和名称覆盖, 名称覆盖须按键合并, 不将旧版任务结构或整个 KubeJS 目录复制到新实例. 游戏内仍需验证章节显示, 分页, 悬停, 名称覆盖优先级和任务链接; 此前不宣称游戏内完成.
