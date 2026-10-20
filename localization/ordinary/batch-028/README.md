# 第 028 批: Retro Factory Manager 蓝图编辑器

Retro Factory Manager 1.0.3 无任何中文, 也无 CFPA 来源. 本批覆盖全部 148 个原生键, 对应 146 个不同原文值, 145 键含中文; 3 键保留技术标识 `minecraft:dirt`, `c:ores`, `V2`.

内容为 Super Factory Manager 的可视化蓝图编辑器: 节点与引脚, 条件与过滤器, 计时器与红石触发, 标签分组, 导入导出与校验提示.

## 术语

- 与 SFM 官方中文对齐: Factory Manager 工厂管理器, 标签枪, 标签. 本模组因此把 Label 译为标签, 与 SFM 的标签体系同名.
- 物品标签另译: Tags 在过滤器中指物品/方块标签, 统一为物品标签, 与 Label 区分.
- SFML 保持原名, 不展开为超长中文; Blueprint 蓝图, Node 节点, Pin 引脚, Wire 连线, Program 程序.
- Timer 计时器, Redstone Pulse 红石脉冲, Interval 间隔, Offset 偏移, Ticks 刻.
- Round robin 轮询, 三种取值按方块/按标签/关闭.
- Forget 遗忘, If 如果, Input/Output 输入/输出, 与 SFM 语句语义一致.
- 方位缩写按中文单字: 后, 下, 东, 前, 左, 北, 右, 南, 上, 西. 保持单词长度, 避免按钮溢出.

## 格式

- `%s nodes · %s wires · %s%%` 的三处占位符与结尾 `%%` 保留, 译文仅替换说明词.
- `Every %s%s %s` 与 `Every %s global%s %s` 的占位符顺序不变.
- `1 program error` 与 `%s program errors` 分开处理, 不合并为同一模板.
- 快捷键提示 `Ctrl+Z undo · Ctrl+Y redo · Ctrl+C/V/D copy · G snap` 保留全部键名与中点分隔.
- `Forge Energy` 译为 `Forge 能量`: 直接写 `FE 能量` 会与单位保护表冲突, 且原文并未使用 FE 缩写.

## 验证

- `python localization/ordinary_translation.py batch-028 --build`: 英文源与 JAR 一致, 146 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/retrofactorymanager/lang/zh_cn.json`, 共 148 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.
