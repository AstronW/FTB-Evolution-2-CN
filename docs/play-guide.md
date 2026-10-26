# FTB Evolution 2 玩法与模组导览

本文根据当前工作副本的任务书 (整合包 1.5.1, `.minecraft/config/ftbquests/quests/`) 整理, 按任务书的章节分组归类整合包主要涉及的模组, 并说明主线目标、推荐起步路线和终局对各模组的需求. 章节名使用本项目当前译文; 模组名有中文时写作 "中文 (English)", 无通行中文时保留英文. 任务数为章节文件中的任务条目数, 仅供衡量篇幅.

## 一、整合包玩法概述

- **沙盒式自由发展**: 任务书只做引导, 不锁进度. 进入世界即可使用全部模组, 从哪个章节开始都可以.
- **出生点金字塔**: 出生在空中的金字塔内, 跳下即可离开 (有缓降). 金字塔已被认领, 内有掮客商店出售初期补给, 露台上有终局挑战排行榜.
- **硬币与商店**: 大多数任务奖励硬币 (个人持有, 不与队伍共享). 村庄、酒馆、庄园、法师塔、女巫小屋、船只等地点会出现不同商人; 探索章节列出了全部商人及地点.
- **领地与区块加载**: 按 M 打开 FTB 地图, 按 C 进入领地界面认领区块 (默认 500 个), Shift + 左键拖动强制加载 (默认 25 个, 需队伍至少一人在线).
- **队伍**: 共享任务进度、领地、区块加载额度和商店进度.
- **常用命令**: `/home` `/sethome` `/back` `/spawn` `/tpa` `/rtp` `/trashcan`; `/events toggle ftb:<事件名>` 开关随机事件 (悦灵交易、山羊、枪手决斗等).
- **营养均衡 (Nutritional Balance)**: 按 N 查看, 本包中只提供增益, 不足无惩罚.
- **灵伴 (Kindred Spirits)**: 初入世界章节即可获得一只伙伴, 羁绊和等级会随时间成长, 建议尽早开始.

**最终目标**: 建造 **FTB天际号**, 在 "Feed The Beast进度" 章节中依次发射各阶段 FTB 组件, 最终交付 **巨兽之心** 通关. 终局几乎会用到整合包中的每个主要模组 (详见第三节).

## 二、推荐起步路线 (主线任务 · 初入世界)

"初入世界" 章节是唯一的引导主线, 顺序大致为:

1. 撸树 → 石器 → 铁器 (奖励精妙背包, 按 B 打开); 按住 `` ` `` 连锁采集.
2. 分支并行:
   - **匠神 (Hephaestus)** 冶炼炉: 粗矿双倍产出, 也是便捷的合金来源.
   - **Just Dire Things** 黏液: 用原初浆凝胶把铁块转化为核源铁.
   - **末影接口 (EnderIO)**: 在主世界基岩上点火获取无限粉, 制作虚空框架.
   - 初期供电: 任选一种初期发电机 (也可用马力发电).
   - **Scannable** 扫描器寻矿.
3. 钻石镐 → 下界 → 下界石英熔炼成硅 → 基础电路 (工业奇械、充能能源或 LTX工业任选其一).
4. 合成 **FTB制造机** → 制作钢 (合金炉) → 钢板 + 末影板 (需要压板机) → 酿液桶发酵火箭燃料 (10,000 mB, 需 40,000 mB 水) → **FTB天际号**.
5. 章节末尾的 "科技模组 / 魔法模组 / 冒险 / 存储与资源" 四个任务分别链接到对应章节组, 之后按兴趣展开.

另有可选福利: 完成 "初始住宅" 可从五座预建房屋中任选一座直接放置.

## 三、终局: Feed The Beast进度

FTB制造机无需选择配方, 放入材料自动匹配; 每刻都需要外部供能. 天际号需要 5×5×6 的露天空地, 物品从控制台侧面与背面的舱口输入, 流体从蓝色符文侧输入, 能量从绿色符文侧输入. 五条路线可分给不同队员.

### 第一阶段: 分支组件 (五条路线)

| 路线 | 分支组件 | 前置部件 | 涉及模组 |
| --- | --- | --- | --- |
| 狩猎 | 狩猎旗帜 | 猎人印记 (头颅装配机, 宝石粉、镶孔符石、朦胧之心、虚空之泪); 龙之遗物 (焦黑铸件台 + 龙之骨 + 龙炎钢); 三场首领试炼 | 末影接口 (EnderIO), 神化 (Apotheosis), 圣遗物 (Reliquary), 匠神 (Hephaestus), 冰火传说 (Ice and Fire); 首领: 凋灵 → 雷霆君王 (Thunder Relics) 或霜熊 → 魔法艺术守护者或巫术首领 |
| 物流 | 认知阵列 | 逻辑晶格 (水晶装配器, 高级处理器/工程处理器, 物流节点, 激光节点, 变量卡); 存储矩阵 (反应仓, 64k存储组件/16k ME存储组件, 模块化路由器, 高级计算机) | 应用能源2 (Applied Energistics 2), ExtendedAE, AdvancedAE, 精致存储 (Refined Storage), Logistics Networks, LaserIO, 动态联合 (Integrated Dynamics), 模块化路由器 (Modular Routers), ComputerCraft: Tweaked |
| 材料 | 地脉锭 | 量子合金晶格 (电弧炉, 镀钨板岩钢锭, 蚀空合金块, 钷); 复合外壳板 (装配器, 铱合金, 坚韧合金块, 钛块, 海蓝钢块) | LTX工业 (LTX Industries), Just Dire Things, 奥瑞科技 (Oritech), 工业奇械 (FTB Industrial Contraptions), 巨型反应堆 (Colossal Reactors), 海蓝科技 (Nautec) |
| 能源 | 动力矩阵 | 充能电池 (充能台, 钻石晶体块, 能量水晶, 晶化合金电容; 每个需 20,000,000 FE); 燃料核心 (反物质构建机, LTX 装配机, 虚炎煤炭, 反应堆棒, 过充水晶) | Powah, 工业奇械, 末影接口, LTX工业, Just Dire Things, 巨型反应堆, 奥瑞科技 |
| 魔法 | 奥术秘典 | 符文板 (纯化温特姆粉, 日光石, 生长粉末, 精炼邪恶, 幽魂粉末, 恶魔之心); 束缚精华 (狱火锻炉, 注灵石板, 火灵灵髓, 艾瑟金属锭, 永恒合金块) | 魔法艺术: 传承 (Ars Magica Legacy), 根源魔法 (Roots Classic), 巫术 (Witchery), Neo Vitae, 神秘学 (Occultism), FTB Armory |

### 第二阶段: 组合组件 (每种需 1,000,000 FE/t 持续一分钟)

| 组合组件 | 关键材料 | 涉及模组 |
| --- | --- | --- |
| 星图 | 戴斯块, 重力操纵器, 星光板, 诺维特锭, 月球爬行者尖刺簇, 超致密反物质, 福特朗衍生器 | 群星 (Stellaris), 工业奇械, 模块化力场 (MFFS) |
| 深渊透镜 | 无瑕海棱水晶, 深海钢镀板, 共鸣碎片, 激光引导线圈, 海妖甲壳, 海洋金锭 | 海蓝科技 (Nautec), 圣遗物 |
| 活体培养物 | 现实虚拟处理器, 究极精华块, 觉醒终极精华, 有机钢锭, 末地钢锭, 超导体, 结晶青金石 | LTX工业, 神秘农业 (Mystical Agriculture) 及 Mystical Agradditions, 奥瑞科技, 末影接口, 充能能源 (Energized Power) |
| 灵魂契约 | 狱锻块, 晶体簇, 暗黑充能宝石块, 坚韧的诺言 III, 艾瑟金属锭, 调谐之石, 蓝色水晶 | Neo Vitae, 邪恶工艺 (EvilCraft), 神秘学, 巫术, Anima |
| 因果锚 | 时间水晶, 悖论机器, 速子吸收器, 新星 77/HX, 沉重核心, 永恒合金块 | Just Dire Things, 奥瑞科技, LTX工业, FTB Armory |

### 第三、四阶段

- 装配组件 (5,000,000 FE/t 持续一分钟): 巨兽核心、巨兽心智、巨兽之魂.
- 巨兽之心 (40,000,000 FE/t 持续三分钟), 连同流体与能量交付后发射即通关; 奖励巨兽奖杯和第一批创造物品.
- "持续进贡" 为可重复任务, 适合挂机工厂持续产出.

**结论**: 能源 (FE 产能) 贯穿终局, 越往后越吃发电; 时间水晶等需要长时间生长的材料应尽早布置.

## 四、按章节分类的模组

### 1. 主线与通用

| 章节 | 任务数 | 主要模组 | 说明 |
| --- | --- | --- | --- |
| 欢迎 | 11 | FTB Quests, FTB Chunks, FTB Teams | 整合包自有系统: 金字塔, 硬币, 领地, 队伍, 命令 |
| 实用技巧 | 31 | 滑翔伞 (Paraglider), 传送石碑 (Waystones), 工具皮带 (Tool Belt), Simple Magnets, 铁喷气背包 (Iron Jetpacks), Trash Cans, 建筑师魔杖 (Architect's Building Wand), Crafting Station, Comforts, Magnum Torch, FTB Ultimine | 日常便利功能; 很多按键默认未绑定 (包括打开任务书), 到按键设置里搜索 |
| 初入世界 | 36 | 原版, 匠神, Just Dire Things, 末影接口, 精妙背包, 灵伴 (Kindred Spirits), Scannable | 引导主线, 通向 FTB天际号 |
| Feed The Beast进度 | 59 | 几乎全部主要模组 | 终局挑战, 见第三节 |

### 2. 科技模组

| 章节 | 任务数 | 模组 | 定位与要点 |
| --- | --- | --- | --- |
| 末影接口 | 48 | 末影接口 (EnderIO) + EnderIO Evolution | 合金炉、导管、电容、头颅装配机、灵魂绑定; 无限粉起步 |
| 充能能源 | 56 | 充能能源 (Energized Power) | 按机器框架逐级解锁, 直到传送器、天气控制器; 本包移除燃煤引擎, 第一阶框架需要钢 |
| 匠神 | 28 | 匠神 (Hephaestus) | 冶炼炉熔铸、双倍矿物、浇铸工具 (类似匠魂) |
| 工业奇械 | 39 | FTB工业奇械 (FTB Industrial Contraptions) | 综合科技 (类似 IC2): 矿物增产、电压等级、核能、反物质、量子盔甲; 本包直接使用 FE |
| LTX工业 | 49 | LTX工业 (LTX Industries) | 科幻科技: 矿物加工链、化学、电路、武器炮塔; 钛起步 |
| 奥瑞科技 | 66 | 奥瑞科技 (Oritech) + Oritech Things | 多方块机器 + 插件, 粒子加速器、核反应堆; 本包镍/铀/铂由整合包矿石提供 |
| 海蓝科技 | 147 | 海蓝科技 (NauTec 2) | 海洋科技: 深海探索、激光、细菌培养、潜艇; 篇幅最大的科技章节, 终局深渊透镜依赖它 |
| 群星 | 58 | 群星 (Stellaris) | 太空: 钛、火箭、航天服、月球, 终局星图依赖它 |
| Powah | 37 | Powah | 七级能源 (发电机、充能台、反应堆); 本包修改了反应堆配方, 水不再可用于冷却 |
| 巨型反应堆 | 13 | 巨型反应堆 (Colossal Reactors) | 自由设计的反应堆 + 涡轮机 |
| 动态联合 | 42 | 动态联合 (Integrated Dynamics), Integrated Tunnels, Integrated Terminals | 编程式自动化网络, 上手难但上限高 |
| Just Dire Things | 85 | Just Dire Things + Just Dyna Things | 凝胶转化方块产出模组金属, 强力工具、传送枪、时间操控 |
| 敌对神经网络 | 15 | 敌对神经网络 (Hostile Neural Networks) | 用数据模型模拟生物掉落和矿石产出 |
| 模块化力场 | 17 | 模块化力场 (MFFS) | 力场投射与防护, 终局需要福特朗 |
| XyCraft | 13 | XyCraft Machines / XyCraft World | 荧光、储罐、提取机等小型机器 |

### 3. 魔法模组

| 章节 | 任务数 | 模组 | 定位与要点 |
| --- | --- | --- | --- |
| Neo Vitae | 93 | Neo Vitae (血魔法续作) + Animus 附属 | 命血祭坛、符文、仪式、恶魔意志 |
| 神秘学 | 77 | 神秘学 (Occultism) | 召唤魔灵、粉笔仪式、维度存储; 从打草找魔鬼之梦种子开始 |
| 巫术 | 62 | 巫术 (Witchery: Just Another Witchery Remake) + Forbidden Magic | 种植奇异植物、炼药锅、娃娃、吸血鬼/狼人/巫妖化 |
| Anima | 53 | Anima | 骨头与水晶构建的灵魂魔法, 魔像、造神 |
| 魔法艺术 | 50 | 魔法艺术: 传承 (Ars Magica Legacy) | 自定义法术、亲和、守护者首领; 用液态源质池转化书本获得纲要 |
| 邪恶工艺 | 29 | 邪恶工艺 (EvilCraft) | 收集生物血液, 暗黑宝石起步 |
| 根源魔法 | 23 | 根源魔法 (Roots Classic) | 简单的自然魔法与仪式 |
| 圣遗物 | 19 | 圣遗物 (Reliquary) | 用怪物稀有部件制作遗物; 本包部件无合成配方, 需亲手击杀 |

### 4. 资源与物流

| 章节 | 任务数 | 模组 | 定位与要点 |
| --- | --- | --- | --- |
| 通用存储 | 217 | 应用能源2 (Applied Energistics 2), AdvancedAE, ExtendedAE, Applied Flux, Applied Oritech, 精致存储 (Refined Storage) 及其扩展, 精妙存储 (Sophisticated Storage), 精妙背包 (Sophisticated Backpacks), 功能性存储 (Functional Storage), Dank Storage, Enderthing, DimStorage | 背包、箱子到数字化存储与自动合成; 任务最多的章节 |
| 资源生产 | 163 | 神秘农业 (Mystical Agriculture) 及 Mystical Agradditions / Mystical Automation, 资源蜜蜂 (Productive Bees) + Mystian Apiary, Mob Flow Utilities, Geore, Easy Villagers, Just Another Mining Dimension (采矿维度), Dimensional Resources, 神化刷怪笼 | 种出/养出/挖出资源; 采矿维度是 Replication 的前置 |
| Replication | 23 | Replication | 物质复制; 本包只能复制基础材料 |
| 物流 | 87 | 模块化路由器 (Modular Routers), Nodeworks, LaserIO, Pipez, Logistics Networks, MoreRed, Super Factory Manager, ComputerCraft: Tweaked, Pylons, Entangled, Item Collectors, 动态联合 | 物品、流体、能量传输与红石逻辑 |
| 能源生产 | 41 | Powah, 工业奇械, 奥瑞科技, 充能能源, 海蓝科技, Horse Powered 等 | 跨模组的发电路线, 按初期/中期/后期/终局和燃料/热能/太阳能分类 |
| 高效农业 | 16 | Productive Farming | 作物性状 (生长速度、产量) |
| 实用工具 | 33 | Iron Furnaces, Utilitarian, Modular Drones, NeoSync, Fertilization, Shrink, Crafting on a Stick, ElevatorMod | 不构成独立路线的便利模组 |

### 5. 探索与战斗

| 章节 | 任务数 | 模组 | 定位与要点 |
| --- | --- | --- | --- |
| 整装待发 | 113 | 神化 (Apotheosis) + Apothic Enchanting, Iron's Artifice, Iron's Gems 'n Jewelry, 突变怪物 (Mutant Monsters), Baubley Heart Canisters, Artifacts, Mining Gadgets, Building Gadgets 2, FTB Armory, 灵伴 | 装备、附魔、词缀与宝石、枪械、饰品; 战斗向玩家的核心章节 |
| 探索 | 85 | 原版结构, 冰火传说, 巫术, Thunder Relics, 探险者指南针 (Explorer's Compass) 等 | 地牢、首领竞技场、商人位置; 冰火生物不会在出生点 2,000 格内生成 |
| 冰火传说 | 60 | 冰火传说 (Ice and Fire) | 养龙、龙钢锻造、神话生物装备 |
| 烹饪与酿造 | 105 | Cooking for Blockheads, Pantry for Blockheads, Agritech: Evolved, Starcatcher, Horse Powered, Animal Pen 等 | 厨房、种植盆、钓鱼、马力机械、酿造 |
| 极光 | 28 | Auroral | 围绕北极光的寒冷生物群系小型发展线 |
| 共鸣 | 22 | Resonance | 紫水晶装备, 共鸣效果增伤 |
| 建筑与装饰 | 48 | FramedBlocks, Chisel, Macaw 系列, Glassential, Connected Glass, Better Fish Tanks, Crystalix 等 | 纯装饰与建筑, 与进度无关 |
| 悬赏板 | 49 | 原版生物与首领, Gateways to Eternity, 神化 | 击杀与游玩时长成就, 奖励硬币 |

## 五、游玩建议

1. **先走初入世界**, 把 FTB制造机、天际号做出来, 顺便接触匠神、Just Dire Things、末影接口三个早期模组.
2. **尽早搭建发电与存储**: 终局每阶段所需功率呈数量级增长; 能源生产章节可作为发电升级路线图, 通用存储章节的 AE2 或精致存储二选一即可 (终局两边都有可用配方, AE2 的处理器用量更少).
3. **按兴趣选主攻方向, 但终局要求全覆盖**: 第三节的五条路线分别对应 狩猎/战斗、物流、材料、能源、魔法, 多人游玩时可以分工.
4. **耗时项目早布置**: 时间水晶母岩、神秘农业高阶精华、Neo Vitae 祭坛升级、海蓝科技细菌培养等都需要时间积累.
5. **战斗准备**: 狩猎路线需击败凋灵、雷霆君王或霜熊、魔法首领; 整装待发章节的神化附魔与装备能大幅提升战力.
