# 第 186 批: simple_weather

## 范围

All native keys: client rain and snow particle parameters, wind components and sleep reset

- 语言键: 24, 唯一英文文本 20
- 中文值: 24, 保留的非正文值: 0
- 英文源: `.minecraft/mods/simple_weather-1.1.15.jar` 的 `assets/simple_weather/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/simple_weather/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

雨/雪两组同名参数共用同一译名 (范围/透明度/缩放/存活时长); AABB 保留.

## 待办

游戏内验收未做, 需在目标实例确认键位页面宽度, 悬停换行与命令反馈的可读性.
