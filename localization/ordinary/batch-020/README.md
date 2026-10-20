# 第 020 批: Anima 全部普通语言键

本批覆盖 Anima 1.0.3 (NeoForge, MC 26.1.2) 中尚无中文的 299 个普通语言键, 对应 294 个不同原文值. 298 个键含中文; `advancement.anima.root.title` 的 Anima 为模组名, 按任务书既有写法保留英文, 已登记在 `manifest.json` 的 `unchanged_values`. JAR 内共 1296 个原生键, 其余 997 个属于手册正文, 按阶段顺序单独处理.

该 JAR 没有原生中文, 固定 CFPA 提交 `719672954d9df4ea51877e3d5ce2912148273682` 也没有 `anima` 目录, 因此全部为新译. 术语不另行拟定, 直接沿用已完成的 `chapters/anima.json5` 任务书译文, 以便物品名, 进度名与任务正文在游戏中一致.

## 内容

- 31 条进度及其标题, 覆盖水晶, 玻璃工艺, 部件与电路, 魔像, 骨笼抽取, 灵魂之井, 法术, 灌注, 萨隆铁, 神魂, 造神与崇拜, 自动化, 献祭和肉身重构.
- 4 个实体, 2 个状态效果, 1 个附魔和 1 个按键.
- 40 个方块, 含机器, 神像, 玻璃器皿, 水晶与神系建筑.
- 约 60 个物品, 含魂骨与萨隆铁两条装备线, 灵魂九类, 模具, 桶装熔融物与法器类工具.

## 术语

本批沿用任务书既定译名, 并按同一体系补齐任务书未直接出现的名称:

- Soulbone 魂骨, Crystallized Soulbone 结晶魂骨, Soulbone Splinter 魂骨碎片, Soulbone Conduit 魂骨导体.
- Saronite 萨隆铁, Raw Saronite 粗萨隆铁, Saronite Ingot 萨隆铁锭; 工具名依次为萨隆铁剑, 镐, 斧, 锹, 锄.
- Blue Crystal 蓝色水晶, Yellow Crystal 黄色水晶, Blue/Yellow Gem 蓝色/黄色宝石, 熔融态为熔融蓝色水晶与熔融黄色水晶.
- Soul Well 灵魂之井, Soul Stone 魂石, Soul Relay 灵魂中继器, Soul Forge 灵魂锻炉.
- Golem 魔像, Workshop Golem 工坊魔像, Golem Fabricator 魔像制造器, Golem Part Assembler 魔像部件装配台, Soul Leash 灵魂缰绳.
- Foci 法器, Spell Book 法术书, Infusion Table 灌注台, Research Table 研究台, The Necronomicon 死灵之书.
- Deity 神祇, Pantheon 万神殿, Deity Shrine 神祇神龛, Deity Hammer 神祇之锤, Deity Fabricator 神祇制造器, Offering Plate 供奉盘, Plinth 基座, Priest Rod 祭司杖.
- 九类灵魂按任务书为温和, 掠食, 厄运, 狂乱, 水生, 末影, 炼狱, 睿智, 神魂.
- 玻璃器皿按功能命名: Funnel 漏斗, Decanter 醒酒瓶, Splitter 分流器, Gourd 葫芦瓶, Spiral 螺旋管; 吹制站 Blow Mold 为吹制模台, 各 `*_mold` 物品为对应模具, 以区分台与模具.

任务书未出现而由本批确定的名称为醒酒瓶, 分流器, 葫芦瓶, 螺旋管, 吹制模台, 合成共振器, 凝聚石板, 灵魂传送门, 灵魂触须, 灵魂幽光与宇宙之神, 已记入 `TERMINOLOGY.md`, 后续手册沿用, 不再另立别名.

## 源文核对

`block.anima.soul_altar` 的当前英文值为 Research Table, 而 `block.anima.dark_altar` 为 Altar of Souls. 本批按键面英文翻译, 分别得到研究台与灵魂祭坛, 不凭键名改写语义, 也不改动 JAR. 该差异属于上游命名, 未按勘误处理.

`item.anima.crystal_shard` 的英文物品名是 Blue Crystal, 与 `item.anima.blue_gem`(Blue Gem) 区分, 译文分别为蓝色水晶与蓝色宝石, 与任务书的宝石/水晶用法一致.

## 数值与格式

原文占位符, 数字顺序, 换行与边界空格均保留; 本批没有格式代码, 单位或拼接前缀. `enchantment.minecraft.lunge` 属于跨命名空间键, 游戏会将其并入统一语言表, 与 26.1.2 原版无同名键冲突.

## 验证

- `python localization/ordinary_translation.py batch-020 --build`: 英文源与 JAR 一致, 294 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/anima/lang/zh_cn.json`, 共 299 键; 构建前该路径无本地覆盖, `overlay-before.json` 为空对象.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为进度界面的标题长度, 神系建筑的方块名在 Jade/JEI 中的显示, 以及灵魂类物品名与任务书引用是否完全一致.
