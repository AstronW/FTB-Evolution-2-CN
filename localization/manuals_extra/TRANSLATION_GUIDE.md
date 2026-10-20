# 剩余手册翻译工作说明

本目录处理 1.4.0 中尚未覆盖的 305 篇 Markdown/MDX 手册. 译文按整页保存在 `translations/<原路径>`, 构建时写入资源包或数据包. 不要修改 `.minecraft/mods` 中的 JAR, 不要修改 `sources/` 快照, 也不要改动其他批次的译文.

## 文件位置

- 英文源快照: `localization/manuals_extra/sources/<原路径>`
- 中文译文: `localization/manuals_extra/translations/<原路径>` (目录结构与源相同)
- 当前模组名称对照: `localization/manuals_extra/glossaries/<group>.json`
- 源清单与目标路径: `localization/manuals_extra/source_manifest.json`
- 单页检查: `python localization/manual_extra_translation.py check-page <原路径>`

## 硬性规则

1. 只翻译玩家可见正文和标题. 保留 Markdown/MDX 结构, 标题层级, 列表标记, 表格列数, 空行和组件位置.
2. 保留所有资源 ID, 物品/方块/实体 ID, 命令, 代码块, 内联代码, 链接目标, 图片路径, `<...>` 组件标签, `$(...)` 宏, 数字, 单位, 占位符 (`%s`, `%d`, `{0}`) 和引用标记 (`[ref=...]`, `[item=...]`).
3. 所有自写中文使用英文半角标点 (`,` `.` `:` `;` `!` `?` `(` `)` `[` `]` `"` `'`). 禁止 `，。：；！？（）【】“”‘’、` 等全角标点.
4. 代码块内容原样保留, 不翻译代码, 不翻译命令. 注释除非有明显玩家可见说明, 否则也保留.
5. frontmatter 只翻译 `title`, 以及 `navigation` 下的 `title`; 保留 `icon`, `parent`, `position`, `item_ids`, `categories` 等字段和顺序.
6. 术语优先使用 `glossaries/<group>.json` 中当前游戏/CFPA 已用的中文名称. 没有中文名称的模组名, 专名, 缩写可保留英文. 同一页内同一概念只用一个译名.
7. 不增删句子, 不写攻略补充, 不改数值和机制. 原文有歧义时按上下文直译, 并在译文中保留原有条件与步骤.
8. 每页译完后运行单页检查, 必须输出 `PASS`. 不要运行全量 `check`, 因为其他页面可能仍在翻译中.

## 常见结构

- GuideME 组件: `<ItemLink id="..."/>`, `<BlockImage .../>`, `<ItemImage .../>`, `<SubPages .../>`, `<Color ...>...</Color>`, `<Column ...>...</Column>`. 标签原样保留, 只翻译标签之间的自然语言.
- Stellaris: `[item=stellaris:...]` 是物品嵌入标记, `[ref=stellaris:...]Text[ref]` 中只翻译 `Text`, 保留标记.
- Oracle Index MDX: 常用 `related_items`, `[text](./path)` 链接. 只翻译链接文字, 保留目标.
- 表格: 保留每行的 `|` 数量和分隔行. 表头与单元格正文翻译.

## 推荐流程

1. 读 `sources/` 下整页原文.
2. 读 `glossaries/<group>.json`, 查物品/方块名称.
3. 在 `translations/` 下建同名文件, 整页翻译.
4. 运行 `python localization/manual_extra_translation.py check-page <原路径>`.
5. 按报错修复, 直到 `PASS`.

## 已有示例

`localization/manuals_extra/translations/assets/colossal_reactors/guides/colossal_reactors/guide/` 下有四页已通过检查的示例.
