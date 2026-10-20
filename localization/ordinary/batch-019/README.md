# 第 019 批: Kindred Spirits 全部原生普通语言文本

本批覆盖 Kindred Spirits 1.0.9 (MC 26.1.2) 的全部 331 个普通语言键, 对应 322 个不同原文值. 326 个键含中文; 5 个键保留英文模组名 Kindred Spirits, 已登记在 `manifest.json` 的 `unchanged_values`. 手册正文不在本批范围.

模组当前 JAR 只有 `en_us.json` 与 `pt_br.json`, 没有原生中文; 固定 CFPA 提交 `719672954d9df4ea51877e3d5ce2912148273682` 中也没有 `kindredspirits` 目录, 因此本批没有可复用的跨版本候选, 全部为新译. 任务书 `getting_started` 第 161 条已把模组名写作 Kindred Spirits, 本批的 `itemGroup`, `oracle_index` 标题, Jade 插件名, 按键分类与进度根节点沿用同一写法, 不另立中文名.

## 内容

- 9 种灵魂伙伴的实体名与刷怪蛋, 其中 Nightfox 为夜狐, T-Rex 为霸王龙, Mini Player 为迷你玩家, Baby Dragon 为幼龙, Gremlin 为格雷姆林, Quokka 为短尾矮袋鼠, Direwolf 为恐狼.
- 41 个能力名称与说明, 涵盖移动, 治疗, 战斗, 熔炼, 采掘, 增益与伴生效果.
- 羁绊护符界面: 等级, 羁绊, 星数, 威望, 属性, 能力开关, 指令, 攻击性, 体型与皮肤选择.
- 物品悬停, JEI 说明, Jade 显示, 命令反馈, 运行时消息, 字幕与 31 条进度.

## 术语

- bond 统一为羁绊, companion 为伙伴, spirit 为灵魂, 与任务书既有说法一致; bond 不译作链接或契约.
- Kindred Charm 为羁绊护符, prestige 为威望, 其星级称威望星.
- Stay 指令为驻留, 与 Follow 跟随, Wander 游荡并列; 相关说明中的 told to Stay 同作驻留, 不另用停留.
- 三个攻击性档位为被动, 中立, 敌对; 与能力说明中的敌对生物用词统一.
- 能力名保留动作含义而非字面直译, 例如 Crushing Might 为崩解之力, Forge Draft 为熔炉鼓风, Kiln Breath 为窑息.
- 单位与机制名称沿用游戏既有中文: 生命恢复 II, 抗性提升 II, 速度 II, 幸运 I.

## 数值与格式

原文的占位符顺序, 数值顺序, 换行与边界空格均保留. 两处刻意按原文顺序改写句式, 避免占位符或数字次序变化:

- `jei.kindredspirits.battery` 原文先写 2 点闪电伤害再写 3 格范围, 译文同样先伤害后范围.
- `death.attack.kindredspirits.mirror_strike.player` 原文占位符为 `%1$s`, `%2$s`, `%3$s`, 译文改为"被…击中, 事发时正与…战斗"以维持该顺序.

`screen.kindredspirits.bond_feed_wait` 原文以两个空格开头的拼接前缀保留原样.

源文 `death.attack.kindredspirits.mirror_strike` 与 `.player` 中的撇号被双重编码为 `Ã¢â‚¬â„¢`, 属于上游乱码. 译文按语义写作"的倒影", 不沿用乱码, 也不改动 JAR 原文; 该键的中文不构成机制或数值勘误.

## 验证

- `python localization/ordinary_translation.py batch-019 --build`: 英文源与 JAR 一致, 322 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过; 安装内容与构建一致.
- `python project.py check`: 批次 001-019 及任务书, 手册, 自定义内容, CFPA 审校包全部通过.
- 输出为 `.minecraft/kubejs/assets/kindredspirits/lang/zh_cn.json`, 共 331 键; 构建前该路径无本地覆盖, `overlay-before.json` 为空对象.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为羁绊界面在窄屏下的换行, 长能力说明的悬停高度, 字幕与命令反馈的实际显示, 以及霸王龙蛋与伙伴床的 JEI 页面排版.
