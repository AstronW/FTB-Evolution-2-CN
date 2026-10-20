# 第 056 批: Iron Furnaces

覆盖 `ironfurnaces` 的 3 个普通语言键, 对应 3 个不同原文值, 0 键含中文, 3 键为保留的非正文值.

三个坐标标签, 保留原文与尾部空格.

## 验证

- `python localization/ordinary_translation.py batch-056 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/ironfurnaces/lang/zh_cn.json`, 共 3 键; 未修改 JAR, 配方或存档.
