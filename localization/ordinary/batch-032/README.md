# 第 032 批: 无线红石开关 (重制版)

覆盖 `malisisswitchesreborn` 的 135 个普通语言键, 对应 115 个不同原文值, 132 键含中文, 3 键为保留的非正文值.

绿石与绿石催化剂, 能量连接器, 各类无线开关与传感器. 保留 Shift 与两个格式串.

## 验证

- `python localization/ordinary_translation.py batch-032 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/malisisswitchesreborn/lang/zh_cn.json`, 共 135 键; 未修改 JAR, 配方或存档.
