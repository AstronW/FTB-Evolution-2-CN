# 第 030 批: Auroral 全部原生语言键

Auroral 冬季扩展无任何中文, 也无 CFPA 来源. 本批覆盖全部 160 个原生键, 对应 152 个不同原文值, 157 键含中文; 3 键保留非正文值: 模组名 `Auroral` 与彩蛋物品 `S'nore` 的原文.

## 术语

- Aurora 极光: 极光灯, 极光碎片, 极光花, 极光末影碎片, 极光鹦鹉螺, 极光雪灵.
- 材料体系: Shimmersteel 微光钢 (微光钢锭, 未精炼微光钢), Shimmerweave 微光编织 (微光布, 微光外衣, 微光护腿, 微光护目镜, 微光冰刀靴).
- 能源: Aura 灵气, Liquid Aura 液态灵气, Glacial Basin 冰川之盆, Aura Level 灵气等级.
- 植物与地形: Glow-Leek 发光韭葱, Hearthwood 炉木, Shimmer Soil 微光土壤, Shimmering Ice 微光冰.
- 状态: Frostbite 霜噬, Frostbite Immunity 霜噬免疫. 与 Minecraft 的“冰冻”区分, 保留伤害型状态语义.
- 其他: Snow Angel 雪天使, Frozen Petals 冻结花瓣, Star-Shot 星弹, 低温酿造台, 锻造模板与微光钢升级.

## 格式

- 数值与百分号保留: `%d/%d` 灵气等级, `+15%`/`+45%` 催化, `7` 个游戏日, `16` 格, `3x`/`5x` 生长, `15%` 生命阈值, `5` 分钟.
- `Aura Level: %d/%d` 的占位符顺序与原文一致.
- 原文 `Magestic` 为拼写错误, 译文按 majestic 的含义写作“威严的”, 不复制拼写错误, 也不作为机制勘误.
- `S'nore` 为双关名称, 保留原文; 模组名 Auroral 与任务书一致保留英文.

## 验证

- `python localization/ordinary_translation.py batch-030 --build`: 英文源与 JAR 一致, 152 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/auroral/lang/zh_cn.json`, 共 160 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.
