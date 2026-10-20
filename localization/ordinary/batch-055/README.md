# 第 055 批: ComputerCraft

覆盖 `computercraft` 的 3 个普通语言键, 对应 3 个不同原文值, 2 键含中文, 1 键为保留的非正文值.

掌上电脑升级名称, 保留 HTTP.

## 验证

- `python localization/ordinary_translation.py batch-055 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/computercraft/lang/zh_cn.json`, 共 3 键; 未修改 JAR, 配方或存档.
