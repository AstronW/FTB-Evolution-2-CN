# 第 133 批: loot_journal

## 范围

Merge mode explanation, filter groups and format strings.

- 语言键: 21, 唯一英文文本 16
- 中文值: 18, 保留的非正文值: 3
- 英文源: `.minecraft/mods/loot_journal-neoforge-26.1-6.2.1.jar` 的 `assets/loot_journal/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/loot_journal/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

合并模式四个枚举名 (TYPE_NAMED/TYPE/STRICT/NONE) 保留英文, 说明文字翻译; § 颜色码逐条对齐.

## 待办

游戏内验收未做, 需在目标实例确认界面文案长度, 悬停换行与格式码渲染.
