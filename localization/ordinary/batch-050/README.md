# 第 050 批: Hostile Neural Networks

覆盖 `hostilenetworks` 的 8 个普通语言键, 对应 8 个不同原文值, 0 键含中文, 8 键为保留的非正文值.

全部为数值与格式串, 无正文.

## 验证

- `python localization/ordinary_translation.py batch-050 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/hostilenetworks/lang/zh_cn.json`, 共 8 键; 未修改 JAR, 配方或存档.
