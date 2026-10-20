# 第 059 批: Tesseract

覆盖 `tesseract` 的 1 个普通语言键, 对应 1 个不同原文值, 0 键含中文, 1 键为保留的非正文值.

仅通道信息格式串, 保留占位符.

## 验证

- `python localization/ordinary_translation.py batch-059 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/tesseract/lang/zh_cn.json`, 共 1 键; 未修改 JAR, 配方或存档.
