# 第 048 批: Just Dire Things

覆盖 `justdirethings` 的 10 个普通语言键, 对应 9 个不同原文值, 5 键含中文, 5 键为保留的非正文值.

补界面标签与 Forge 能量显示.

## 验证

- `python localization/ordinary_translation.py batch-048 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/justdirethings/lang/zh_cn.json`, 共 10 键; 未修改 JAR, 配方或存档.
