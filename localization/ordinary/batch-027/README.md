# 第 027 批: Just Dyna Things 官方中文缺口

Just Dyna Things 2.0-alpha 的 JAR 自带 `zh_cn.json`, 239 个原生键中已有 171 个中文. 本批补齐其余 163 个普通语言键, 对应 162 个不同原文值, 159 键含中文; 4 键保留时间手杖倍率 `8x`, `1x`, `2x`, `4x`, 已登记在 `unchanged_values`.

## 术语

材料名全部取自 Just Dire Things 官方中文, 保持同一整合包内一致:

- Ferricore 核源铁, Blazegold 烈焰金, Eclipse Alloy 蚀空合金, Celestigem 苍穹晶.
- Goo 凝胶: Primogel 原初浆, Blazebloom 烈焰蕾, VoidShimmer 虚空辉, Shadowpulse 暗影脉.
- Paradox 悖论, Void Crystal 虚空水晶, Time Wand 时间手杖.
- 本模组新增: 高级能量传输器, 高级刻速器, 简易刻速器, 流体混合器, 不稳定流体, 破坏手杖, 抽象悖论.
- 光源手杖, 拾取手杖, 交换手杖为 Just Dire Things 没有的变体, 按同类手杖构词; Light Wand 不译作灯杖.
- Ticker 统一为刻速器, 与时间手杖的加速语义一致; Tick rate 为刻速, Ticks 为刻.
- 铁砧与太阳能板按材料前缀: 核源铁砧, 烈焰金砧, 蚀空合金砧, 苍穹晶砧; 对应太阳能板同理.

## 格式

- 配置项 70 余条按“对象 + 属性”批量统一, 例如每刻能量, 最大能量存储, 忽略修理冷却, 需要白天, 需要看见天空.
- 保留 `§` 颜色码及顺序, 例如 `§7`, `§a`, `§c`, `§4§l`, `§8§o`.
- 保留全部数值与单位: `%s/tick`, `FE/刻`, `MB/刻`, `16x`, `Y 高度`.
- `FE/ticks` 与 `MB/ticks` 的原文复数写法未改, 仅译单位后的词.

## 验证

- `python localization/ordinary_translation.py batch-027 --build`: 英文源与 JAR 一致, 162 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/justdynathings/lang/zh_cn.json`, 共 163 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.
