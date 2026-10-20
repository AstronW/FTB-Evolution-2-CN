# 第 039 批: Ender IO

覆盖 `enderio` 的 19 个普通语言键, 对应 19 个不同原文值, 17 键含中文, 2 键为保留的非正文值.

导管名称, 过滤槽位与名单标签. 保留 µI 与 mb 单位写法.

## 验证

- `python localization/ordinary_translation.py batch-039 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/enderio/lang/zh_cn.json`, 共 19 键; 未修改 JAR, 配方或存档.
