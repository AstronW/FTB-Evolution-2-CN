# 第 026 批: Better Fish Tanks 全部原生语言键

Better Fish Tanks 1.3.0 的 JAR 只有 `en_us.json`, 另有德语与西班牙语, 没有中文, 也无对应 CFPA 命名空间. 本批覆盖全部 185 个原生键, 对应 177 个不同原文值, 184 键含中文; 唯一保留英文的是创造模式标签页名 `Better Fishtanks`, 已登记在 `unchanged_values`.

内容为鱼缸方块与界面, 水族师工作台与村民, 各类鱼食容器, 鱼袋, 六档鱼卵, 以及大量装饰性方块.

## 术语

- Aquarist 水族师: 工作台为水族师工作台, 村民为水族师, 指南为水族师指南. 不译作养鱼人或水族爱好者, 保持职业名一致性.
- Fish Tank 鱼缸; Tank Floor 缸底; Tank Upgrades 鱼缸升级; Fish Bag 鱼袋.
- 鱼食: Flakes 薄片饲料, Pellets 颗粒饲料, Pellet Mix 混合颗粒, mini Shrimp 小虾, dried Kelp 干海带; 容器统一为 X容器.
- 鱼卵档位沿用稀有度既有译名: 普通, 罕见, 稀有, 史诗, 异域, 传说.
- 装饰方块按尺寸与材质组合: 微型/小型/中型树枝, 微型/小型石块, 洞穴结构, 沉船残骸, 塔楼.
- 木材沿用原版: 橡木, 云杉, 白桦, 丛林, 金合欢, 深色橡木, 红树, 樱花, 竹; Stripped 统一为去皮.
- 石材: 石头, 花岗岩, 闪长岩, 安山岩, 深板岩, 凝灰岩, 方解石, 滴水石; 矿物: 紫水晶, 钻石, 绿宝石, 青金石, 红石.

## 批量构词

装饰方块 120 余条由固定模式生成, 以减少同一系列出现不一致:

- `Cave Structure (石材, 矿物)` → `洞穴结构 (石材, 矿物)`.
- `Tiny/Small Stone (石材)` → `微型/小型石块 (石材)`.
- `Tiny/Small/Medium Branch (木材)` 与 `… Stripped Branch` → 对应尺寸 + 去皮与否 + `(木材)`.
- `Shipwreck (Stripped X)` → `沉船残骸 (去皮X)`.
- `X Egg Chance: N%` → `X鱼卵几率: N%`, 百分比数值不变.

## 格式与拼接

- `Fish: %s` 与 `Water: %s` 同时用于界面与悬停, 译文保持一致, 占位符与顺序不变.
- 产卵说明拆为两条键: `要让鱼缸中的鱼产卵,` 与 `需要给它们喂食.`, 分两行显示后仍是一句完整的话.
- 水量单位保留括注: `百分比 (%)`, `桶 (B)`, `毫桶 (mB)`.
- 创造模式标签页保留模组名 `Better Fishtanks`; 装饰页为 `Better Fishtanks | 装饰`.

## 验证

- `python localization/ordinary_translation.py batch-026 --build`: 英文源与 JAR 一致, 177 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/betterfishtanks/lang/zh_cn.json`, 共 185 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为鱼缸界面标签宽度, 工作台 JEI 页面的鱼卵几率对齐, 以及长装饰名在物品栏中的截断.
