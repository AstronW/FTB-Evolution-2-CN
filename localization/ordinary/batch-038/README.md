# 第 038 批: Stellaris

覆盖 `stellaris` 的 27 个普通语言键, 对应 27 个不同原文值, 27 键含中文, 0 键为保留的非正文值.

Jade 状态, 抽油机与能量配置, 画作名称与字幕.

## 验证

- `python localization/ordinary_translation.py batch-038 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/stellaris/lang/zh_cn.json`, 共 27 键; 未修改 JAR, 配方或存档.
