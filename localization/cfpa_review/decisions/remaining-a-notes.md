# CFPA 候选审校: remaining-a

审校日期: 2026-10-17. 范围是 [remaining.json](../inputs/remaining.json) 的零起始索引 [300, 1400), 共 1100 条. 目标为 `project.json` 中 FTB Evolution 2 1.4.0 / Minecraft 26.1.2 实例的有效英文. 当前 `source` 字段保留完整候选及源键, 不修改 CFPA 上游或游戏实例.

## 结果

- 接受 1097 条, 拒绝 3 条.
- 接受项相对候选原文改动 455 条; 其中除半角标点规范外涉及内容修复或术语统一 218 条.
- 使用当前 [cfpa_review_format.py](../../cfpa_review_format.py) 的 `invariant_errors` 逐条验证所有接受项, 剩余格式 findings = 0. 没有增加数字豁免.
- 逐行结果见 [remaining-a.json](remaining-a.json), 每行含有效英文、采用中文、完整来源和理由. 中文仍是本批候选裁决, 安装与游戏内验收由主流程分别执行.

## 逐项核对发现与修复

1. Collapsible Groups 的 collapse/collapsible 指配方查看器的折叠, 不是合并. 将其界面内 group 统一为“分组”, collapse 为“折叠”, 保留内置支持名称中的模组身份; AE2、RS2 用原缩写防止数字丢失. 修复启用开关语义, 以及更新后不再局限 JEI 的配方查看器描述. 修复名称“没有可用于文件名的 ASCII 字符”被误成“含非 ASCII 字符”, 以及“缺少筛选规则”被误成“缺少物品”. 代码节点 all/any/ComponentPath/HasComponent 及字段名保留, 不当作可执行标识符翻译. 依据为本批输入对应键的当前英文和完整候选源.
2. 动态联合 `tutorials.logicOperations.text6` 映射至旧 `text5` 候选, 其主体为惰性求值, 不是旧同键的显示面板操作段. 保留明确的来源键映射; 当前 text5 的“再次编辑变量卡”没有可复用主体, 拒绝旧候选.
3. 动态联合按当前内容修复“菜单”→“手册”、求值术语、配方/原料值类型、显示面板、NBT 字段 `Book`、列表浮点数 `3.33`/`1.14`、NBT 路径方括号前多余的点. NBT 示例的语法括号经半角规范恢复. 保留变量引用而非预计算的机制, 以及“整数/布尔/实体/流体”等类型含义.
4. 动态联合的部件设置按钮按当前源为左上角; 延迟器列表尾部为最新值; 电池/发电机段落按当前源移除 Tesla 支持断言, 保留 RF. 补回延迟器顶部必须保留变量卡的约束. 压榨产物及红石复位说明按当前英文修复误译, 不加入游戏源没有描述的功能.
5. 动态联合兼容模块中 Thaumcraft Aspect 为要素, Aura Base 为灵气场基值, Aura Flux 为灵气场咒波. 修复“面”“范围轮廓”等错译. Tesla 充满条目的“巫婆”修复为物品, 非空条目的反向“没有能量”修复为“具有能量”; 输出/输入检查描述清楚考虑存储量和容量.
6. FTB Teams 修复“收到邀请”方向和踢出对象/队伍方向, 修复客户端未从服务端收到数据被写成服务端未收到. FTB Backups 恢复确认使用显式参数位置, 保留世界名与备份来源顺序, 并补齐当前英文的路径示例和反斜杠说明. Configured 更新失败提示不误写上传失败, 修复缺失 `%s` 的日志文本为正确的 `%1$s`/`%2$s` 映射.
7. 保留 Compressium 压缩级别的所有数值与倍率; FTBIC 只采用本批的金属材料/矿石通用名称, 不因其它版本出现同英文就覆盖旧机制或数值. Growth Accelerator Tiers 的 buds 为晶芽, 不是生长源母岩. GuideME 的 Invalid guide id set 是“所设 ID 无效”, 不是集合.

## 拒绝项

- `info_book.integrateddynamics.tutorials.logicOperations.text5`: 旧候选主体是已经移到当前 text6 的惰性求值说明, 无当前编辑变量卡说明的可复用主体.
- `info_book.integrateddynamics.manual.logic_programming.text4`: 旧候选介绍搜索/筛选, 当前介绍加载和修改已有变量卡, 不同操作步骤.
- `info_book.integrateddynamics.manual.logic_programming.text6`: 旧候选介绍方块/物品形式转换, 当前介绍通过 Labeller 和 E 按钮命名, 不同机制.

以上均留作后续新译, 不以同键匹配冒充完成.

## PR 意见核对

基于已抓取的 [pr-human-discussions.json](../pr-human-discussions.json) 对采用来源 PR 逐项筛选. PR 2170 对 advanced/machine block 命名、反应堆广播等的意见均不属于本批采用的材料名. 其建议中文全角标点与本项目用户要求相冲突, 本地覆盖遵循 [STYLE.md](../../STYLE.md), 上游文件不改. PR 5446 的 FTB Quests 图片着色、暂停游戏、文件保存路径等审查条目均不是本批采用的 X/Y 轴和按键项; 未将对整个 PR 的 approve 当作这些条目的充分依据. PR 6132 的长篇 Animus 机制评论不涉及本批 sanguine_dynamo 的宝珠绑定/取出两个同义改名提示; 使用当前提示原文核对对象. 其余所采用 PR 在该缓存中未发现相关的人工语义审查意见, 不以“没有意见”代替本文逐条检查.

来源 PR 均固定为以下审校输入所存 SHA, 各条采用范围由 decisions 中 source 指定:

| PR | 作者 | head SHA |
| --- | --- | --- |
| [#2170](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/2170) | zizunsi | `9e8b068bb21436168b6873cd3932b05be814fab6` |
| [#5356](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/5356) | StarDustMTF | `d3d725f7cbe07f558f033511f3c6b7b4795865bf` |
| [#5446](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/5446) | Ironnoob73 | `1fe845555df2b48b9c6cb5c6934710d78ed1a283` |
| [#6101](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/6101) | Don-Trueno | `21561bf6f23465b8d0ad4db3788479a47f966daa` |
| [#6132](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/6132) | ChuijkYahus | `5f17499dd1835a849caef784dafadeed0d90b4d3` |
| [#6159](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/6159) | ChuijkYahus | `761204642e546142d761b89c28864be4bced81a1` |

事实依据为每行固定英文和原始候选, 本文中文术语选择为项目审校裁决; 未启动游戏检查显示、参数实际填充值与加载优先级.
