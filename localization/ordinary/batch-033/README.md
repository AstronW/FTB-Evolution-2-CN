# 第 033 批: Oritech

覆盖 `oritech` 的 78 个普通语言键, 对应 76 个不同原文值, 60 键含中文, 18 键为保留的非正文值.

共振器系列, 资源节点, 方块破坏器提示与配置项. 保留 Oritech, NBT, 数值单位与缩写.

## 验证

- `python localization/ordinary_translation.py batch-033 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/oritech/lang/zh_cn.json`, 共 78 键; 未修改 JAR, 配方或存档.
