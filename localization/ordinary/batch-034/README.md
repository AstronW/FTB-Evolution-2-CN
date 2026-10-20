# 第 034 批: 模块化无人机

覆盖 `drones` 的 44 个普通语言键, 对应 38 个不同原文值, 44 键含中文, 0 键为保留的非正文值.

无人机能力, 组装框架与控制器, 旋翼与推进器.

## 验证

- `python localization/ordinary_translation.py batch-034 --build`: 英文源与 JAR 一致, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/drones/lang/zh_cn.json`, 共 44 键; 未修改 JAR, 配方或存档.
