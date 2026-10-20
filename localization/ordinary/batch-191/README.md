# 第 191 批: buildguide

## 范围

All native keys: async generation, persistence, random colors and shape/property labels

- 语言键: 10, 唯一英文文本 10
- 中文值: 10, 保留的非正文值: 0
- 英文源: `.minecraft/mods/BuildGuide-26.1.2-0.4.9.jar` 的 `assets/buildguide/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/buildguide/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

异步/多线程 与 持久化 按技术含义直译; 多棱锥 与 螺旋 为形状名.

## 待办

游戏内验收未做, 需在目标实例确认键位页面宽度, 悬停换行与命令反馈的可读性.
