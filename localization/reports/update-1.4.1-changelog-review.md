# 1.4.1 Changelog 与汉化影响交叉检查

日期: 2026-10-20. 已对用户提供的 48 条更新说明逐项分类, 并对洒水壶、法术配置/消耗、Wonderland 配方、Apotheosis 中文及实际模组文件进行本地交叉核对. 本次未修改译文或游戏目录, 未运行游戏测试. 其余程序修复按日志判断汉化影响, 不表示已逐项复现修复效果.

原文保存于 [Changelog 快照](update-1.4.1-changelog-source.txt), 每条对应判断、核对范围和源文件哈希保存于 [逐项审查明细](update-1.4.1-changelog-review.json). 日志链接的 GitHub issues 未打开, 本报告不引用其中未读取的内容.

## 新发现: 英文不变, 洒水壶说明仍然过时

Changelog 第 2 项说明 Mystical Agriculture 洒水壶不再支持模拟玩家. 当前实例 `config/mysticalagriculture-common.toml` 明确为 `fakePlayerWatering = false`.

但新版英文任务 `quest.1CFEC4265CAAA0D8.quest_desc` 仍说本包允许模拟玩家使用洒水壶, Just Dire Things 的 Clicker 可以代劳. 项目 `localization/translations/chapters/resource_generation.json` 的片段 `140` 同样保留此说明.

因此首次检查中的 **3 个新增键、4 个原文修改键仍准确, 但还需增加 1 个“源文未变化、机制已改变”的说明勘误**. 后续应单独记录原文勘误依据, 将中文适配为新版不允许模拟玩家/机器代用的含义, 并按现有源文校验流程维护例外证据. 本次不直接更改英文源或游戏配置.

这也说明 4,174 个英文不变键只能视为可复用候选, 不能自动推断其机制描述全部仍正确.

## 已包含或可以复用

- Nodeworks 冷却任务和方块名称、血弹描述、魔力成长 25→50、Any Gun Modifier、EvilCraft 净化器及 Replication 拼写修正, 均已包含在首次检查中.
- Apotheosis 的基础盔甲韧性、FTB Skyline 和前置世界等级条件已由本项目 `custom/batches/batch-003` 处理. 当前上游中文与项目在措辞、术语、标点上有差异, 不因此整文件覆盖或重复翻译. 本次确认项目已有对应内容; 全部术语冲突仍须按当前英文和既定裁决逐条复核.
- Wonderland 配方已按当前实例核对: 胸甲增加 `ltxi:laser_tech_part` x1, 护腿增加 `ltxi:logic_core` x2, 靴子增加 `ltxi:impulse_tech_part` x2. 当前中文护甲页未写死旧配料清单, 不需要借汉化修改配方.
- 法术数据已核对: Falling Star / Fire Rain / Blizzard 为 250 mana + 75 burnout; Daylight / Moonrise 为 400 + 100. 配置中 Falling Star 伤害为 16, Fire Rain / Blizzard 伤害为 3, 间隔为 5 tick. 通用配置名称无需因为数值变化重译; 显示数值由新版配置/数据提供, 后续检查手册动态组件是否正确加载.

## 需要保留新版逻辑的变化

任务前置、粉笔提交条件、NBT/组件匹配、奖励箱内容、Boss 生成、矿物统一、配方及种子可用性等变化, 通常不产生新的语言键. 不能把它们遗漏为“与更新无关”, 也不能通过复制旧任务结构、旧配方或旧数据覆盖来安装汉化. 后续合并和验收必须使用新版逻辑.

检索未发现任务书仍推荐 Blazing / Spirited Crystal 种子的说明; 不能把对应水晶名称、Powah 使用说明或仍存在的蜜蜂路线一起删除. 洒水壶任务本身已经引用 Mystical Agriculture, Farming for Blockheads 洒水壶的禁用不要求替换此任务的物品名称.

## 日志与实际输入的区别

日志写 Witchery 更新到 0.5.24, 但当前实际主 JAR 是 `witchery-0.5.25+mc26.1.2.jar`. 版本绑定应按实际输入进行. 当前未发现 Wakes 顶层 JAR, 与旧 Wakes 输入路径失效一致; 不应为了让旧批次检查通过而装回旧模组.

日志没有逐项展开本轮已发现的 Nautec / Nodeworks 手册和其他模组语言变化. 首次检查中 8 篇已维护页面变化、4 篇新页面候选和普通语言来源适配仍需保留, 不能仅按 changelog 缩减范围.
