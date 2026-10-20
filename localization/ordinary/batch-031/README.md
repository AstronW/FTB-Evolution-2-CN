# 第 031 批: MORE Red 官方中文缺口

MORE Red 自带 `zh_cn.json` 仅 22 键, 其余 121 个普通语言键仍为英文. 本批补齐这 121 键, 全部含中文. 门电路与红石线等既有条目沿用官方译名, 未改动.

## 术语

- 既有官方译名: 更多红石电路, 红石合金锭, 石底座, 红石线柱, 红石线轴, 二极管与各类门电路.
- 机械传动: Axle 传动轴, Clutch 离合器, Gear 齿轮, Gearshifter 换挡器, Windcatcher 捕风器, Alternator 交流发电机, Extractor 提取器, 石磨.
- 物流与过滤: Distributor 分配器, Loader 装载器, Filter 过滤器, Multifilter 多重过滤器, Osmosis Filter 渗透过滤器, Shunt 分流器.
- 线缆体系: Cable 线缆, Tube 管道, Bundled Cable 集束线缆, Cable Junction 线缆接点, Cable Relay 线缆中继器, Redwire Junction/Relay 红石线接点/中继器.
- 木材沿用原版: 橡木, 云杉, 白桦, 丛林, 金合欢, 深色橡木, 红树, 樱花, 苍白橡木, 绯红, 诡异.

## 批量构词

- 11 种木材 × 5 种部件共 55 条, 全部按“木材 + 部件”生成, 例如金合欢传动轴, 诡异换挡器.
- 16 种颜色 × 线缆/管道共 32 条, 按“颜色 + 线缆/管道”生成, 例如淡蓝色线缆, 黄绿色管道.
- 生成方式避免同一系列出现“深色橡木”与“深橡木”这类不一致.

## 格式

- 进度标题保留原意的趣味性: Humble Bundle 作谦逊捆绑包, Taste the Rainbow 作尝尝彩虹, Square Hole 作方孔.
- 无占位符与数值; 未改动物品 ID 或配方.

## 验证

- `python localization/ordinary_translation.py batch-031 --build`: 英文源与 JAR 一致, 121 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/morered/lang/zh_cn.json`, 共 121 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.
