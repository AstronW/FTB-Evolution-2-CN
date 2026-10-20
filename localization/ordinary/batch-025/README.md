# 第 025 批: Occultism 官方中文缺口

Occultism 1.256.1 的 JAR 自带 `zh_cn.json`, 4331 个原生键中已有 3943 个中文, 本批补齐其中仍是英文的 185 个普通语言键, 对应 183 个不同原文值, 178 键含中文. 7 个键保留非正文值: 两个 `%s`, `%d/%d`, 三个工作区尺寸 `64x64`/`32x32`/`16x16`, 以及彩虹粉笔的逐字着色彩蛋 `§4H§ca§6p§ep§ay §2P§3r§bi§9d§1e§5!`; 均已登记在 `unchanged_values`.

## 术语

沿用 JAR 内官方中文, 不另立体系:

- Familiar 使魔, Spirit 魔灵, Infused 灌注 (官方灌注镐), Otherworld 异界, Iesnium 艾瑟金属.
- Spirit Attuned 魔灵同调 (官方魔灵同调水晶); Flame of Automation 自动化之火; Pentacle 五芒星阵; Third Eye 第三只眼; True Sight Staff 真视法杖; Spirit Fire 灵火.
- 新增物品按同一构词: 灌注斧/靴子/胸甲/头盔/锄/马铠/护腿/鹦鹉螺铠/锹/矛/剑, 使魔手套, 使魔石板, 虫洞石板, 烈焰膏, 仪式收集器.
- 使魔名: Drikwing 德里克翼, Wingnis 翼尼斯. 二者无官方中文, 按音译处理并保持使魔后缀一致.

`Pentacle Alt` / `Pentacle Eye` / `Pentacle Gear` 对应的仪式类别在 JAR 内没有中文说明, 按已有 `五芒星阵合成/杂项/附身/召唤` 的构词译为五芒星阵祭坛 / 五芒星阵眼 / 五芒星阵装备. 该三项属推断, 已在批次记录中标注, 后续若在手册中出现明确类别名再复核.

## 源文与格式

- `Ritual completed successfully: X.` / `Interruption in the ritual: X.` / `Starting the ritual: X.` 共 18 组按仪式名批量生成, 仪式名与对应物品标题取自同一批译文, 避免同一仪式出现两种叫法.
- 烈焰膏说明为 5 行且末尾带换行, 译文保留相同行数与结尾换行; 虫洞石板、仪式收集器、使魔手套等说明同样保留原行数.
- `§6Dictionary§r §6of§r §6Spirits§r` 的三个 `§6` 颜色码全部保留, 译文以“§6魔灵§r §6词典§r §6中的说明§r”承载书名.
- 数值与百分比未改: `21x9x21` 工作区、`9` 个指南针、`50%`/`30%` 等原样保留.
- 彩虹粉笔的彩蛋字符串不翻译, 逐字配色一旦改写就失去效果.

## 验证

- `python localization/ordinary_translation.py batch-025 --build`: 英文源与 JAR 一致, 183 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/occultism/lang/zh_cn.json`, 共 185 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为仪式提示在聊天栏的换行, 使魔石板界面的按钮宽度, 以及 JEI 中翼尼斯获取说明的颜色分段.
