# 第 021 批: Energized Power 官方中文缺口

Energized Power 3.0.1 的 JAR 自带 `zh_cn.json`, 1789 个键齐全, 但其中 395 个仍是英文占位, 即本批范围; 对应 321 个不同原文值, 388 个键含中文. 另有 7 个键保留非正文值: 模组名 Energized Power, 画作作者 JDDev0, 以及 `%dx %s`, `%s / %s`, `• %s: %s` 三个纯格式串. 这些已登记在 `manifest.json` 的 `unchanged_values`.

本批只输出这 395 键, 不改写 JAR 内既有的 1394 条中文. 覆盖列表, 精英电池箱, 精英充电器与放电器, 精英动力炉与自动合成器, 精英压模, 涡轮传送带系列, 特高压变压器, 经验存储与汲取, 机器配置器界面及升级模块名称.

## 术语

沿用 JAR 内官方中文的既有体系, 不另立译名:

- 机器等级 Basic 基础, Hardened 硬化, Advanced 高级, Elite 精英; 与官方 `基础机器框架`, `高级机器框架`, `强化高级机器框架` 的层级一致.
- Press Mold 压模, 依据官方 `压模制造机`; 按产物分齿轮压模, 棒材压模, 线材压模.
- Pressurized Fluid Pipe 加压流体管道, 与官方 `铜流体管道`, `钢流体管道` 保持同一结构.
- 电压等级沿用官方 LV 低压, MV 中压, HV 高压, EHV 超高压, 本批 UHV 为特高压, 格式与官方 `超高压变压器 (1 转 n)` 一致.
- 传送带等级沿用官方 基础, 高速(Fast), 极速(Express), 本批 Turbo 为涡轮.
- 升级模块沿用官方 `升级模块`; 本批新增物品弹出, 物品吸取, 充能速度, 能量产出, 经验提取, 能量容量, 能量效率, 提取深度, 提取范围, 熔炉模式, 月光, 范围, 速度等类别.
- 经验相关: XP Drain 经验汲取, XP Storage 经验存储, XP Extraction 经验提取, Liquid XP 液态经验, XP Yield 经验产出.

## 任务书术语同步

任务书原文把该机器称为自动合成机, 而 JAR 内官方中文对 `auto_crafter` 与 `advanced_auto_crafter` 使用自动合成器. 按项目规则, 术语裁决后同步游戏名称与任务书, 因此把 `translations/chapters/energized_power.json` 中 5 处 自动合成机 改为 自动合成器, 涉及三种等级与一处章节标题. 只改名称, 未改数值, 配方或任务结构.

## 标点与格式

本批自行编写译文使用英文标点; JAR 内既有官方中文的全角标点保持原样, 不做批量改写. 因此同一命名空间内会出现两种标点风格, 属于上游资源与本项目覆盖的分工, 不是本批输出不一致.

`%dx %s`, `%s / %s`, `• %s: %s`, `%.2fx 流体消耗`, `%d / %d 级` 等格式串按原样保留, 占位符顺序, 数字顺序与末尾空格均未改动. `Machine configuration stored for: ` 与 `Status: ` 的末尾空格保留, 以保证界面拼接正确.

## 验证

- `python localization/ordinary_translation.py batch-021 --build`: 英文源与 JAR 一致, 321 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/energizedpower/lang/zh_cn.json`, 共 395 键; 构建前该路径无本地覆盖, `overlay-before.json` 为空对象.
- 任务书改动后通过 `localization/verify_quests.py`.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为升级模块长名称在物品栏与悬停中的宽度, 机器配置器界面的输入输出方向标签, 以及经验存储的 `%d 级` 显示.
