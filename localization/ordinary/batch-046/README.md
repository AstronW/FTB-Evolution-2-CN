# 第 046 批: MFFS

覆盖 `mffs` 的 10 个普通语言键, 对应 10 个不同原文值, 6 键含中文, 4 键为保留的非正文值.

力场系统, 加固模块与权限提示.

## 验证

- `python localization/ordinary_translation.py batch-046 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/mffs/lang/zh_cn.json`, 共 10 键; 未修改 JAR, 配方或存档.
