# 第 051 批: Fusion

覆盖 `fusion` 的 8 个普通语言键, 对应 8 个不同原文值, 8 键含中文, 0 键为保留的非正文值.

资源包版本警告界面.

## 验证

- `python localization/ordinary_translation.py batch-051 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/fusion/lang/zh_cn.json`, 共 8 键; 未修改 JAR, 配方或存档.
