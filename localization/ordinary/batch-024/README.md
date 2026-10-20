# 第 024 批: Collapsible Groups 分组管理器与规则编辑器

Collapsible Groups 2.0.0-beta4 的 JAR 只有 `en_us.json` 与 `zh_tw.json`, 没有简体中文; 固定 CFPA 提交中该命名空间也没有可复用条目. 本批覆盖 246 个原生普通语言键, 对应 237 个不同原文值, 237 键含中文, 9 键保留非正文值: `KubeJS`, `%s (KubeJS)`, `ID`, `patch`, `%s`, `%s · %s` 与两个 `iconIds[n]` 字段名, 已登记在 `unchanged_values`.

内容为管理器界面, 分类管理, 批量操作, 规则编辑器 (条件类型, 命名空间/标签/路径/组件匹配), 外观编辑器, 配置页与各类确认提示.

## 术语与取舍

`zh_tw.json` 存在但不直接转写; 按本项目既有裁决与大陆用词确定, 并与 `TERMINOLOGY.md` 的 Collapsible Groups 条目一致:

- Group 分组 (繁体作群組), Category 分类, Manager 管理器, Batch actions 批量操作. 不用群组, 避免与 FTB 队伍概念混淆.
- Rule 规则, Condition 条件, Subgroup 子分组; Rules mode 规则模式.
- Tag 标签, Namespace 命名空间, Path 路径, Exact Stack 精确堆叠, Component 组件.
- 不翻译技术标识: `ID`, `KubeJS`, `patch`, `iconIds[0]`, `iconIds[1]`. `patch` 是 JSON 补丁节点类型, 不译作补丁以免误解为整合包补丁.
- Source category 来源分类, 与内置/自定义/资源包三类徽标区分.

## 格式

- 两条多行原文保留换行数量: Iron's Apothic 配置说明为两行, 搜索语法提示为四行; TSV 中以 `\n` 转义保存.
- 占位符与顺序全部保留, 包括 `%1$s · %2$s rules`, `Showing %s / %s · Selected %s`, `Exported %s keys to %s` 与 `New copy of "%s"`.
- `%s (Built-in)` 等徽标改为 `%s (内置)`, 括号内用中文但保持半角括号.
- 数字区间 `0 to 2147483647` 原样保留, 未改写为科学计数或范围缩写.

## 验证

- `python localization/ordinary_translation.py batch-024 --build`: 英文源与 JAR 一致, 237 个值全覆盖, 占位符, 数值顺序, 格式代码, 单位, 换行与边界空格检查通过.
- 输出为 `.minecraft/kubejs/assets/collapsible_groups/lang/zh_cn.json`, 共 246 键; 构建前无本地覆盖.
- 未修改 JAR, CFPA 资源, 配方或存档.

游戏内尚未验收. 待验收项为规则编辑器长说明的换行与截断, 分类侧栏宽度, 批量选择条的位置, 以及 `%1$s · %2$s 条规则` 在窄按钮中的显示.
