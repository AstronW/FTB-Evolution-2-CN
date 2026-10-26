# 规范术语库

`glossary.json` 是跨任务书、手册与普通文本的**规范术语库**: 每条记录对应一个已裁决的概念, 按模组命名空间 (及任务书章节) 限定适用范围, 并可绑定语言键与禁用变体. 它供查询和自动校验, **不做任何替换**, 也不取代 `TERMINOLOGY.md` 的裁决记录与证据.

## 与其他词表的关系

| 文件 | 角色 |
| --- | --- |
| `TERMINOLOGY.md` | 裁决过程、理由与证据 (人读) |
| `glossary/glossary.json` | 裁决结果的结构化摘要, 可查询、可校验 (本目录) |
| `terms.json`, `manuals/terms.json`, `manuals/nodeworks-terms.json`, `cfpa_review/terms.json`, `manuals_extra/glossaries/` | 各阶段的历史词表, 结构与用途不变; `lookup --legacy` 可一并检索, 结果标为"参考, 未复核" |

一个概念在 `TERMINOLOGY.md` 裁决后, 再登记到本库; 本库条目的 `source` 指回对应章节或批次报告.

## 日常用法

在项目根目录执行:

```bash
python localization/glossary.py lookup 霜噬
```

按英文、中文、条目 ID、语言键或禁用变体检索, 显示规范译名、适用范围、禁用写法、说明、来源及已知问题. 加 `--legacy` 同时检索历史词表:

```bash
python localization/glossary.py lookup "Spirit Attuned" --legacy
```

翻译前想知道某个英文在当前模组里对应哪些语言键、游戏现在显示什么 (需本地 `.minecraft/mods`):

```bash
python localization/glossary.py suggest-keys apotheosis Pinnacle
```

改完译文或词条后校验 (已纳入 `python project.py check`):

```bash
python localization/glossary.py check
```

导出给表格软件或 CAT 工具 (Excel、OmegaT、Trados 等可直接导入 TSV/CSV):

```bash
python localization/glossary.py export --format csv --output glossary.csv
```

`stats` 列出条目数与各命名空间分布.

## 物品名审计

`python localization/audit_item_names.py` 检查说明文本 (任务书、手册、Patchouli、手册语言键与提示) 是否使用游戏当前物品名; 英文提到某个物品名而配对中文缺少其当前译名即失败. 已复核的误报与有意保留登记于 `name-audit-exceptions.json`, 每条须写理由. 规则来源与首轮修正见 `../reports/item-name-alignment-2026-10-23.md`. 发现差异时以游戏名为准修改说明文本源头; 只有原文确实不指该物品, 或已有用户裁决时才登记例外.

## 校验内容

`check` 只读, 依次检查:

1. **结构**: 字段、ID 格式、状态与分类取值; 规范译名须用半角标点; 同一命名空间内同一英文 (同一分类) 不得有两个已批准译名. 不同命名空间允许不同译名, 例如 Occultism 的 Spirit Attuned = 魔灵同调, 匠神工具的 Spirit Attuned = 灵魂调谐.
2. **语言键**: `keys` 中每个键在当前生效中文里的值必须等于规范译名. 解析顺序与发布合并一致: KubeJS 覆盖 → CFPA 审校包 → 手册包 → CFPA 转换包 → 模组 JAR 自带中文. 英文源与记录的 `en` 不同时给出警告, 提示原文已变需复核. 缺少本地 JAR 时找不到的键只警告.
3. **禁用变体**: 在范围内的所有维护产物中查找 `avoid` 写法: KubeJS 与两份资源包的语言文件, 任务书 `lang/zh_cn`, 手册 Markdown/Patchouli JSON, 数据包 wiki. 规范译名本身和 `allow` 中的合法词 (如原版"铁傀儡") 先被屏蔽, 不会误报.
4. **已知问题**: 已登记于 `known_issues` 的命中降为警告, 新出现的命中仍然失败. 问题修复后若不再复现, `check` 会提示删除该记录.

`--strict` 把警告也视为失败, 用于阶段收尾.

## 条目字段

```json
{
  "id": "auroral.frostbite",
  "en": "Frostbite",
  "zh": "霜噬",
  "namespaces": ["auroral", "frostbear"],
  "quest_chapters": ["auroral"],
  "category": "effect",
  "keys": ["effect.auroral.frostbite"],
  "avoid": ["冻伤"],
  "allow": [],
  "note": "Auroral 与 FrostBear 同一效果名",
  "source": "TERMINOLOGY.md#任务书与手册同步 (2026-10-18)",
  "status": "approved"
}
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | `命名空间.概念`, 小写, 全库唯一 |
| `en` / `zh` | 是 | 当前有效英文与规范中文. 保留英文时二者相同并设 `keep_english: true` |
| `namespaces` | 是 | 适用的资源命名空间, 支持 `*` 通配 (`integrated*`); `["*"]` 表示全局, 慎用 |
| `quest_chapters` | 否 | 任务书 `chapters/<名>.json5` 的章节名, 支持通配. 任务书跨模组, 不随命名空间自动纳入 |
| `category` | 否 | `mod_name` `item` `block` `entity` `fluid` `effect` `mechanic` `ui` `material` `tier` `concept` `place` `unit` `proper_noun` |
| `keys` | 否 | 显示该名称的语言键; 只绑定名称键, 不绑定包含该词的句子 |
| `avoid` | 否 | 范围内不得出现的旧译或误译; 不可与规范译名重叠 |
| `allow` | 否 | 包含禁用词但合法的更长写法 |
| `note` / `source` | `source` 必填 | 区分说明与裁决出处 (TERMINOLOGY 章节、批次报告、JAR 键) |
| `status` | 是 | `approved` 为规范; `pending` 为待裁决, 不得作为规范传播 |

## 维护流程

1. **查**: 先 `lookup` 本库与历史词表, 再按 `TERMINOLOGY.md` 查官方中文和 CFPA (含 PR 与跨版本).
2. **裁决**: 在 `TERMINOLOGY.md` 记录决定和证据.
3. **登记**: 在 `glossary.json` 增加或修改条目. 用 `suggest-keys` 找名称键; 只为确有旧译或常见误译的概念写 `avoid`, 并把范围限制到实际命名空间与章节, 避免把同一英文的其他语义误判为错误.
4. **同步**: 修改可维护译文源 (批次 TSV/JSON、任务书 `translations/`、CFPA 决策等), 按对应阶段重新构建. 不直接改生成文件.
5. **校验**: `python localization/glossary.py check`, 再运行阶段检查和 `python project.py check`.

暂时无法修复的不一致写入 `known_issues` (条目 ID、定位片段、原因与源头、发现日期), 不要为让检查通过而删掉 `avoid` 或放宽范围.

## 当前已知问题

无. 2026-10-23 首次校验发现的 4 项 (Apotheosis 顶点/高峰, Witchery 金黄仪式粉笔, MFFS 福特朗) 已修复, 见 `TERMINOLOGY.md` 的"2026-10-23 规范术语库".

`known_issues` 的记录格式:

```json
{"entry": "mffs.fortron", "locations": ["resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN/assets/mffs/lang/zh_cn.json"],
 "reason": "现象与可维护源头", "found": "2026-10-23"}
```
