# 第 037 批: NeoSync

覆盖 `neosync` 的 28 个普通语言键, 对应 28 个不同原文值, 24 键含中文, 4 键为保留的非正文值.

躯壳存储与零点构造器, 命令与 JEI 说明. 保留占位格式串.

## 验证

- `python localization/ordinary_translation.py batch-037 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/neosync/lang/zh_cn.json`, 共 28 键; 未修改 JAR, 配方或存档.
