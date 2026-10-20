# 存储与物流完成报告 (第 061-097 批)

按“科技与能源 -> 存储与物流 -> 整合包与 FTB”的顺序, 存储与物流一类已完成. 覆盖 35 个命名空间, 692 个语言键, 其中普通文本 650 键, 手册语言键 42 键.

- 语言键: 692
- 中文值: 651
- 保留的非正文值: 41
- 未完成草稿: 无
- 游戏内验收: 未做

## 逐批明细

| 批 | 命名空间 | 键 | 中文 | 保留 |
|---|---|---:|---:|---:|
| 061 | compressium | 180 | 180 | 0 |
| 062 | stepcrafter | 80 | 80 | 0 |
| 063 | refinedtypes | 75 | 75 | 0 |
| 064 | ftbfiltersystem | 65 | 64 | 1 |
| 065 | pipe_connector | 36 | 36 | 0 |
| 066 | recursiveae2patternprovider | 30 | 30 | 0 |
| 067 | transparentae2 | 19 | 19 | 0 |
| 068 | quantumcubes | 13 | 13 | 0 |
| 069 | refinedstorage | 12 | 10 | 2 |
| 070 | infinitystorage | 11 | 11 | 0 |
| 071 | ae2 | 9 | 2 | 7 |
| 072 | rsrreforged | 8 | 7 | 1 |
| 073 | functionalstorage | 7 | 7 | 0 |
| 074 | integrateddynamicscompat | 7 | 6 | 1 |
| 075 | integratedterminalscompat | 7 | 7 | 0 |
| 076 | integratedterminals | 29 | 24 | 5 |
| 077 | integratedtunnels | 18 | 18 | 0 |
| 078 | sophisticatedcore | 6 | 2 | 4 |
| 079 | dimstorage | 6 | 6 | 0 |
| 080 | advanced_ae | 5 | 0 | 5 |
| 081 | refinedfluidsubstitution | 3 | 2 | 1 |
| 082 | dankstorage | 3 | 2 | 1 |
| 083 | belts | 3 | 3 | 0 |
| 084 | pipez | 3 | 0 | 3 |
| 085 | refinedstorage_jei_integration | 2 | 1 | 1 |
| 086 | extendedae | 2 | 0 | 2 |
| 087 | sophisticatedstorage | 2 | 0 | 2 |
| 088 | laserio | 2 | 1 | 1 |
| 089 | modularrouters | 2 | 0 | 2 |
| 090 | appflux | 1 | 0 | 1 |
| 091 | universalgrid | 1 | 1 | 0 |
| 092 | nodeworks | 1 | 0 | 1 |
| 093 | dimenergy | 1 | 1 | 0 |
| 094 | enderthing | 1 | 1 | 0 |
| 095 | integrateddynamics | 30 | 30 | 0 |
| 096 | integratedterminals | 11 | 11 | 0 |
| 097 | integratedtunnels | 1 | 1 | 0 |

## 关键判断

1. **Compressium 的键名错位**. 上游 `zh_cn.json` 使用 `block.compressium.<material>_<tier>` 键, 而英文源使用 `item.compressium.<material>_<tier>`. 键名不一致, 所以上游那 199 条中文在游戏内无法命中这些物品, 这也是它们被盘点为"暂无中文候选"的原因. 本批补的是 `item.*` 键, 名称照上游既有中文写 (压缩铁块, 压缩钻石块 等), 不另起一套叫法.
2. **AE2 生态的术语以 AE2 官方中文为准**. 样板供应器, 样板编码终端, 智能/致密/包层线缆, 替代品, 均取自 `appliedenergistics2` 自带 `zh_cn`. Step Crafter 与 Nodeworks 的请求器同族, 分别用 分步合成器 / 分步请求器, 与项目既有的 自动合成器 区分开.
3. **只剩格式串的模组不硬翻**. AE2, Advanced AE, Extended AE, Sophisticated Core/Storage, Pipez, Modular Routers, Applied Flux, Nodeworks 等 11 个模组, 缺口里只有单位, 颜色代码, 坐标或模组名, 一律登记为保留值. 这样做同时也让这些条目从"暂无中文候选"中结清, 而不是永远挂着.
4. **`of` 的处理**. AE2 的 `gui.ae2.Of` 上游中文写作 `/`, 但 `ordinary_translation.py` 要求非中文输出必须与原文一致, 因此保留 `of` 并登记为保留值, 不为了一个分隔符去改构建规则.
5. **手册语言键单独一批**. Integrated Dynamics 的保存状态教程, 部件设置, 偏移, 实体化器与网络诊断属于手册正文, 带 `&l` `&o` `&r` 与颜色码. 译文逐条对齐格式码与数字顺序, 并用 无状态, 延迟器, 变量卡箱, 取或默认, 反馈回路 等与已完成的集成动力任务书章节保持一致.

## 未做

- 游戏内验收: 未在目标实例检查名称宽度, 悬停换行, 搜索可达性与格式码渲染.
- 存储类没有剩余的普通文本缺口; 手册文档型内容 (Markdown/Patchouli 页面) 不在本类中.

## 下一类

按原定顺序进入 整合包与 FTB (第 003 类), 缺口最大的是 FTB Quests 120 键与 FTB Echoes 58 键.
