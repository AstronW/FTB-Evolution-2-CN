# 1.4.1 增量适配

用户授权于检查及 changelog 对照之后实施更新. 只写项目可维护来源、工作副本和发布产物; 游戏内验收另计. `before/` 为本次修改前的 1.4.0 文本快照, 不覆盖历史记录.

## 已落盘

- 任务书: 当前 51 文件, 4181 键, 8192 片段; 源文按新版实际输入快照, 中文通过 build 与 verify_quests. 新增/修改片段见 `quest-deltas.json`, 包含洒水壶说明勘误. 任务结构只更新工作副本输入, 不加入安装载荷.
- 特色文案: 001-004 批原文复核复用, 第 005 批新增 3 个冷却块名. 新源绑定 `../../custom/source-bindings-1.4.1.json`. custom_batches 和 custom_translation 检查通过, 工作副本输出保留新版本逻辑.
- 手册: 8 篇已维护页按新源改写, 4 篇新增页补译, 8 篇 LTX KubeJS 覆盖页纳入. 源哈希, 译文与校验见 `../../manuals_extra/` 及 `core-manual-deltas.json`, `extra-manual-deltas.json`, `new-manual-review.json`.
- 普通语言: 5 个同键英文变化逐条修订, 312 个批次重新绑定, 首次纳入与新增键按第 317-337 批落盘. 记录见 `language-update-review.json`, `new-language-translations.json`, `ordinary-rebind.json`.
- 发布: 汇总包已构建并安装到目标实例, 354 项静态检查通过. 详见 `../../reports/release-pack-1.4.1.md`. 游戏内验收仍未进行.
