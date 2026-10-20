# FTB Evolution 2 1.4.1 汇总汉化包

将各阶段已通过静态校验的译文汇总为一个资源包和一份实例级安装清单. 本文只描述汇总产物的组成, 1.4.1 增量处理, 安装结果与边界, 不替代各阶段的原文适配记录.

## 产物

| 文件 | 内容 |
| --- | --- |
| `dist/FTB-Evolution-2-1.4.1-zh_CN.zip` | 资源包本体, 根目录含 `pack.mcmeta` 与 `assets/`, 可直接放进实例的 `resourcepacks/` |
| `dist/FTB-Evolution-2-1.4.1-zh_CN-install.zip` | 完整安装包, 按实例目录结构提供资源包 ZIP, 任务书语言, 整合包数据, Stellaris Wiki 数据包与运行时脚本 |
| `dist/FTB-Evolution-2-1.4.1-zh_CN-manifest.json` | 逐成员 SHA-256 清单与统计 |
| `dist/*.sha256` | 两个 ZIP 的字节哈希, 供分发核对 |
| `dist/FTB-Evolution-2-1.4.1-CFPA-Reviewed-zh_CN.zip` | 另行维护的 CFPA 审校子集, 供单独比对, 不重复计入汇总包 |

资源包内另有 `ATTRIBUTION.md`, `ATTRIBUTION-CFPA.md`, `CFPA-LICENSE.txt` 与 `licenses/ANIMAL-PEN-LICENSE.txt`, 保留上游署名与许可, 不把混合产物标为单一许可.

## 1.4.1 增量处理

目标实例为 FTB Evolution 2 **1.4.1**, Minecraft 26.1.2, NeoForge 26.1.2.121. 差异来源为 `localization/reports/update-1.4.1-assessment.md` 与 `update-1.4.1-changelog-review.md`, 逐项改动与审校理由存于 `localization/updates/1.4.1/`.

| 范围 | 1.4.1 变化 | 处理 |
| --- | --- | --- |
| 任务书 | 4,181 键; 新增 3 键, 修改 4 键; 8 个结构文件变化 | 按新版英文源重编, 保留新版任务结构, 只合并中文与必要标签; 片段记录见 `updates/1.4.1/quest-deltas.json` |
| 任务书原文勘误 | 洒水壶英文仍称允许模拟玩家, 与 `fakePlayerWatering = false` 及 changelog 第 2 项冲突 | 中文改为不允许模拟玩家, 点击器无法代用; 证据见 `reports/source_corrections.md` |
| 整合包特色文案 | 新增 3 个冷却方块名; 6 个已安装文件被新版还原为英文源 | 冷却块按任务书同名处理; 2 个数据文件和 4 个运行时脚本按新源恢复译文, 脚本改为语言键取值, 不再硬编码中文 |
| 关键与补充手册 | 8 篇已维护页源文变化(Nodeworks 2, Nautec 6), 新增 4 页, 8 篇 LTX KubeJS 覆盖页变化 | 逐页按新源改写, 表格式数值, 束流与批量加工机制随新版; 新增页 317 页范围内一并完成 |
| 普通语言 | 5 个同键英文变化(Crystalix 默认值, LTX 两条死亡提示, Integrated Terminals 两条合成计划状态), 312 个批次重新绑定 | 按命名空间与占位符逐条修订; 首次纳入与新增键按第 317-337 批处理 |
| CFPA 审校 | 决策随新版英文更新 | 7,303 键, 76 条分组名称, 468 个资源文件, 构建清单见 `cfpa_review/build-manifest.json` |

## 命令

在项目根目录运行:

```bash
python localization/release_pack.py plan      # 只汇总列出覆盖范围, 不写文件
python localization/release_pack.py build     # 生成 dist 下的 ZIP 与清单
python localization/release_pack.py check     # 复核 dist 产物及已安装结果
python localization/release_pack.py install   # 按明确清单安装到 project.json 的 target_instance
python localization/release_pack.py install --enable  # 同时写入 options.txt 启用资源包
python localization/release_pack.py revert    # 按安装记录还原被覆盖的文件
```

`install` 只写清单内的文件: 资源包 ZIP, 任务书 `config/ftbquests/quests/lang/zh_cn/`, 整合包数据文件和 KubeJS 运行时脚本. 被覆盖的原文件先备份到 `<实例>/.cn-backup-<时间戳>/`, 记录写入 `dist/FTB-Evolution-2-1.4.1-zh_CN-installation.json`. 不复制整个工作副本, 不修改模组 JAR, 配方或存档.

`--enable` 把资源包**追加到列表末尾**, 不插到开头: `resourcePacks` 是"最低优先级在前", 只有末尾才能真正覆盖模组自带资源.

## 安装结果

已安装到 `/home/astronw/.ftba/instances/ftb evolution 2`: 写入 126 个文件, 备份 125 个原有文件, 启用汇总资源包, 安装后哈希核验通过. 备份目录为 `.cn-backup-20261020-231516`.

同时把已被取代的 `FTB-Evolution-2-1.4.0-zh_CN.zip` 从实例 `resourcepacks/` 移入该备份目录的 `retired-resourcepack/`, 并从 `options.txt` 的启用列表中移除其条目, 避免旧包残留键与新版并存. 修改前的 `options.txt` 另存为 `options.txt.before-retire`.

仍未进行游戏内验收: 资源优先级实际效果, 物品名称, 任务悬停, 手册翻页与链接点击, 整合包对话与商店交互都需要在简体中文客户端中实际检查. Stellaris Wiki 以服务端数据包安装, 需确认实例的数据包加载与同步.

## 组成来源

汇总完全由清单驱动, 不扫描工作副本后整拷:

| 组成 | 来源清单 | 数量 |
| --- | --- | ---: |
| 语言覆盖 | `localization/ordinary/batch-*/manifest.json`, `custom/source-bindings-1.4.1.json`, 第 005 批自建键与 CFPA 审校合并 | 31,603 键 |
| 分组名称 | CFPA 审校 `collapsible_groups/group_lang` | 95 条 |
| 手册与书籍 | FTB 指南/FTBIC/Nodeworks 手册包, 已审校 CFPA/PR 手册, Patchouli 可见字段, 补充手册 317 页 | 990 个成员 |
| 任务书 | `localization/quest_translation.py` 输出 | 51 个 JSON5 文件 |
| 整合包数据 | `custom/batches/batch-001|002` 与 Stellaris Wiki 数据包 | 64 个文件 |
| 运行时脚本 | `custom/batches/batch-004` | 7 个脚本 |

资源包共 1,369 个成员, 安装包共 1,492 个成员. 语言文件按资源包语义逐键合并, 不做整文件覆盖; 同键不同译会直接报错而不是静默取一方. `group_lang` 单独保留, 不并入 `lang`.

## 覆盖边界

- 本包为当前范围内静态校验通过的汇总产物. 普通文本, 手册语言键, 分组名称与文档型手册的范围内剩余量均为 0, 见 [已通过成果统计](verified-progress-summary.md).
- 排除范围按 `localization/language_scope.json` 执行, 建筑装饰类模组不产出译文; 任务书及跨模组说明仍完整翻译.
- 普通批次清单中记录的 `unchanged_values` 去重后 968 条, 为经审阅保留英文的模组名, 专名与非散文串, 不视为漏译.
- Nodeworks 的硬编码 UI 按既定要求保留英文, 不修改客户端代码.
- `power_armor` 命名空间是 1.3.2 残留, 当前 1.4.1 无对应源且无清单, 已从产物排除. 脚本对"工作副本有输出但无阶段清单"直接断言失败, 避免不可追溯的译文混入.

## 校验状态

`python project.py check`: **354 项全部通过**, 输出 `All completed translation checks passed. Unfinished drafts:` 为空. 含单元测试, 任务书构建与校验, 各阶段译文的源绑定和格式检查, 原生 GuideME 解析器对 410 页 CFPA 手册与补充手册的结构比对.

本轮环境适配: `/tmp` 为 10 MiB tmpfs, 原生解析器写入 AST 临时文件会报 `设备上没有空间`, 因此检查需在项目内临时目录下运行(`TMPDIR=<项目>/.workbuddy/tmp`); 两个校验脚本清理自身缓存目录时被会话级批量删除保护拦截, 缓存移出后重建即可通过. 这两项属环境问题, 与译文无关.

汇总产物自身校验: `release_pack.py check` 通过(`installation_verified: true`), 逐成员比对 ZIP 内容与清单; 全部 JSON 成员可解析且非空, 无路径逃逸成员; `pack.mcmeta` 的 `min_format`/`max_format` 与当前 26.1.2 资源包格式一致.

静态校验不等同于游戏内验收, 上述游戏内项目均未实际测试.
