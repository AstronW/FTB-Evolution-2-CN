# 第 045 批: Little Big Redstone

覆盖 `little_big_redstone` 的 11 个普通语言键, 对应 10 个不同原文值, 0 键含中文, 11 键为保留的非正文值.

全部为逻辑门符号与格式串, 无正文.

## 验证

- `python localization/ordinary_translation.py batch-045 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/little_big_redstone/lang/zh_cn.json`, 共 11 键; 未修改 JAR, 配方或存档.
