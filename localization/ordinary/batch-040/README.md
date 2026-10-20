# 第 040 批: XyCraft Core

覆盖 `xycraft_core` 的 19 个普通语言键, 对应 19 个不同原文值, 18 键含中文, 1 键为保留的非正文值.

多方块组件与标签名称, 保留 XyCraft.

## 验证

- `python localization/ordinary_translation.py batch-040 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/xycraft_core/lang/zh_cn.json`, 共 19 键; 未修改 JAR, 配方或存档.
