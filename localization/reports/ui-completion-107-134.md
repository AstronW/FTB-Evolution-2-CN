# 界面与信息显示完成报告 (第 107-134 批)

按类别推进顺序, 界面与信息显示一类已完成主体部分. 覆盖 27 个命名空间.

- 语言键: 1104
- 中文值: 934
- 保留的非正文值: 170
- 排除: HoloSigns 69 键 (纯装饰玻璃告示牌, 已写入 `language_scope.json`)
- 未完成草稿: 无
- 游戏内验收: 未做

## 逐批明细

| 批 | 命名空间 | 键 | 中文 | 保留 |
|---|---|---:|---:|---:|
| 107 | travelerstitles | 196 | 154 | 42 |
| 108 | mezz_config_gui | 184 | 172 | 12 |
| 109 | jearchaeology | 156 | 156 | 0 |
| 110 | another_config_manager | 113 | 112 | 1 |
| 112 | bhmenu | 57 | 57 | 0 |
| 113 | torohealth | 55 | 55 | 0 |
| 114 | fancymenu | 46 | 13 | 33 |
| 115 | oracle_index | 45 | 41 | 4 |
| 116 | jade | 27 | 5 | 22 |
| 117 | resourcefulconfig | 32 | 31 | 1 |
| 118 | fancytabsections | 13 | 13 | 0 |
| 119 | enchdesc | 11 | 0 | 11 |
| 120 | iris | 8 | 6 | 2 |
| 121 | peekaboo | 8 | 7 | 1 |
| 122 | jei | 8 | 0 | 8 |
| 123 | moreoverlays | 5 | 5 | 0 |
| 124 | betteradvancedtooltips | 5 | 5 | 0 |
| 125 | eclipseui | 10 | 10 | 0 |
| 126 | colorblindness | 8 | 8 | 0 |
| 127 | fzzy_config | 17 | 0 | 17 |
| 128 | configured | 2 | 1 | 1 |
| 129 | ae2netanalyser | 1 | 0 | 1 |
| 130 | betteradvancements | 1 | 1 | 0 |
| 131 | appleskin | 1 | 0 | 1 |
| 132 | emojiful | 21 | 20 | 1 |
| 133 | loot_journal | 21 | 18 | 3 |
| 134 | ali | 53 | 44 | 9 |

## 关键判断

1. **Traveler's Titles 是最大的一批, 也是最容易做错的一批**. 196 键里 35 个是十六进制标题色 (`ffffff`, `4e518b` 等), 直接把颜色值当正文翻译会把维度标题颜色全部改坏. 剩下的 152 条是维度名与生物群系名; 语义透明的按义翻译 (灰烬荒原, 炼狱沙丘, 幽暗地域, 妖精荒野), 虚构专名音译并记入 `TERMINOLOGY.md` (多弥斯, 格拉西姆, 奥姆尼穹, 万灵乡, 静和境).
2. **配置界面两强用同一套词**. MezzConfig GUI 184 键与 Another Config Manager 113 键都在描述"改配置"这件事, 统一为 待应用的更改/应用/放弃/重置/撤销/默认值, 避免同一个动作在两个配置界面里叫两个名字.
3. **格式串模组一律不硬翻**. JEI (8), Fzzy Config (17), Enchantment Descriptions (11), FancyMenu (27/40), Jade (16/21) 的缺口大多是按键组合, 位置拼接与颜色码, 登记为保留值. 界面上多一个英文单词, 好过拼接后错位.
4. **一处必须绕开的半角化陷阱**. Another Config Manager 原文用 `0–255` (en dash), 若照抄会被 `assert_ascii` 拒绝; 若改成 `0-255`, 校验器会把 `-255` 当成负数, 数字序列与原文不符. 最终写作 `0 到 255`, 既满足半角标点又保持数字序列.
5. **HoloSigns 排除**. 69 键全部是 16 色染色玻璃告示牌与悬挂告示牌的四种形态, 没有任何功能文本; 按 `AGENTS.md` 的建筑装饰范围规则不新增翻译, 已写入 `language_scope.json` 并单列, 不计入剩余缺口.
6. **Jar-in-jar 的处理**. Resourceful Config 的 32 键来自 authme 内嵌的 JAR, 现有抽取脚本按普通 JAR 打开会失败; 本批解包出副本用于校验, 批次清单记录真实来源路径 (`.minecraft/mods/authme-...jar!META-INF/jars/...`).

## 未做

- 游戏内验收: 未检查维度标题的显示长度与颜色, 配置界面长描述换行, JEI 标签宽度, Wiki 页面排版.

## 下一类

进入 农业与食物 (1,087 键), 优先 Mob Flow Utilities 183 与 Productive Farming 171.
