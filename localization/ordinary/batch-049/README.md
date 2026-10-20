# 第 049 批: Hephaestus Tools

覆盖 `hephaestus_tools` 的 9 个普通语言键, 对应 8 个不同原文值, 9 键含中文, 0 键为保留的非正文值.

全能工具与三种精通说明. Lv30 保留原写法以维持数值解析.

## 验证

- `python localization/ordinary_translation.py batch-049 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/hephaestus_tools/lang/zh_cn.json`, 共 9 键; 未修改 JAR, 配方或存档.
