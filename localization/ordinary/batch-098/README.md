# 第 098 批: ftbquests

## 范围

Keybinds, file/chapter/quest settings, click actions, image text, changelog and event log messages.

- 语言键: 120, 唯一英文文本 119
- 中文值: 111, 保留的非正文值: 9
- 英文源: `.minecraft/mods/ftb-quests-neoforge-26.1.2.9.jar` 的 `assets/ftbquests/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/ftbquests/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

界面键位名沿用项目任务书的 章节/任务/奖励/外观 用词; 上游 add_line 与 add_image 两条键值互换, 按值翻译, 不按键名推测.

## 待办

游戏内验收未做, 需在目标实例确认键位名称长度, 悬停换行与格式码渲染.
