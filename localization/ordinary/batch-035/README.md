# 第 035 批: 能量计

覆盖 `energymeter` 的 42 个普通语言键, 对应 41 个不同原文值, 41 键含中文, 1 键为保留的非正文值.

外部显示器, 图表与红石控制, 保留 Shift.

## 验证

- `python localization/ordinary_translation.py batch-035 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/energymeter/lang/zh_cn.json`, 共 42 键; 未修改 JAR, 配方或存档.
