# 第 036 批: Cable Tiers

覆盖 `cabletiers` 的 38 个普通语言键, 对应 38 个不同原文值, 38 键含中文, 0 键为保留的非正文值.

分级接口与自动合成器配置, 方向与导入模式.

## 验证

- `python localization/ordinary_translation.py batch-036 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/cabletiers/lang/zh_cn.json`, 共 38 键; 未修改 JAR, 配方或存档.
