# 第 041 批: XyCraft Machines

覆盖 `xycraft_machines` 的 14 个普通语言键, 对应 14 个不同原文值, 13 键含中文, 1 键为保留的非正文值.

能量选择器, 代理方块, 过滤网与配方名.

## 验证

- `python localization/ordinary_translation.py batch-041 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/xycraft_machines/lang/zh_cn.json`, 共 14 键; 未修改 JAR, 配方或存档.
