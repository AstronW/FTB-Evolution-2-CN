# 第 052 批: Just Dire Fuels

覆盖 `justdirefuels` 的 7 个普通语言键, 对应 7 个不同原文值, 5 键含中文, 2 键为保留的非正文值.

JEI 燃料分类与燃烧参数.

## 验证

- `python localization/ordinary_translation.py batch-052 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/justdirefuels/lang/zh_cn.json`, 共 7 键; 未修改 JAR, 配方或存档.
