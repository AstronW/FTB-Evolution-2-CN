# 当前实例输入切换

2026-10-17: `project.json` 的 `source_instance` 和 `target_instance` 统一为 `/home/astronw/.ftba/instances/ftb evolution 2`. 已读取该实例的 `instance.json`, 确认为 FTB Evolution 2 1.4.0 / Minecraft 26.1.2 / NeoForge 26.1.2.121.

`.minecraft/mods` 已改指该实例的 `mods` 目录. `.minecraft/` 其余源文快照与现有译文保留, 不把旧版工作副本误标为已全量适配 1.4.0. 未改实际游戏文件, 未安装译文, 未进行游戏内验收.

执行 `python project.py check`: 任务书、现有手册、自定义文本、运行时提示、GuideME 原生解析和 CFPA 审校包检查通过. 普通语言有 10 个批次失败: batch-002, batch-003, batch-004, batch-005, batch-006, batch-007, batch-010, batch-011, batch-016, batch-017. 原因均为清单引用的旧版 JAR 文件名在新版实例中不存在. 这些批次需在普通语言阶段对照当前有效源文逐项适配, 不修改源哈希或创建旧文件名别名来强行通过. 这是切换当时的检查结果. 后续已完成这 10 个批次的输入适配, 详见 `ordinary-1.4.0-rebind.md`; `project-migration-verification.json` 为最近一次重跑结果. 自定义等旧快照检查通过仍不代表新版适配完成.

执行顺序已在根目录 `AGENTS.md` 和 `README.md` 同步为: 任务书 → 整合包特色内容 (商店、NPC 对话及相关交互和提示) → 关键手册 → 普通汉化文本 → 其他手册 → 全量收尾.

Java 手册解析器仍使用本机 Prism libraries 中的通用 Java 依赖, 不是旧实例模组或游戏内容输入; 该工具链缓存依赖尚未迁移.
