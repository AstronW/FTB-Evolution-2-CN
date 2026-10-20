# 第 054 批: LTX Industries

覆盖 `ltxi` 的 7 个普通语言键, 对应 6 个不同原文值, 4 键含中文, 3 键为保留的非正文值.

死亡消息, JEI 时间与工具提示.

## 验证

- `python localization/ordinary_translation.py batch-054 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/ltxi/lang/zh_cn.json`, 共 7 键; 未修改 JAR, 配方或存档.
