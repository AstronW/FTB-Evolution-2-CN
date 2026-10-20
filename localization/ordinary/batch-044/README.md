# 第 044 批: Replication

覆盖 `replication` 的 12 个普通语言键, 对应 11 个不同原文值, 10 键含中文, 2 键为保留的非正文值.

创造物质储罐与任务界面. 保留模组名.

## 验证

- `python localization/ordinary_translation.py batch-044 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/replication/lang/zh_cn.json`, 共 12 键; 未修改 JAR, 配方或存档.
