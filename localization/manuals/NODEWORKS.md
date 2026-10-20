# Nodeworks 手册汉化完成记录

当前模组为 `nodeworks-0.9.21.jar`. 已完成75页, 共2,144个含英文的可见行片段, 包括正文, 标题, 表格和Lua示例中的讲解注释. API类型, 方法名, 参数, 资源ID和示例输出字面量按原文保留.

| 部分 | 页数 |
|---|---:|
| 概览与入门 | 2 |
| 物品与方块 | 43 |
| 网络机制 | 6 |
| 搭建示例 | 7 |
| Lua API参考 | 17 |
| 合计 | 75 |

另补充当前JAR的全部111条语言键, 包括物品/方块名称, 容器标题, 提示, 消息, 字幕和按键名称. 手册与新增语言文件均使用英文标点, 术语沿用现有任务书, 例如天青石母岩, 脚本终端和卡片编程器.

译文安装于现有独立资源包 `FTB-Evolution-2-Manuals-zh_CN`, 路径为 `assets/nodeworks/nodeworksguide/_zh_cn/`. 未改动JAR和英文源, 未修改Lua可执行语句. 该资源包仍位于启用列表末尾.

## 校验

- 当前全部164页中文手册及英文源均通过当前GuideME自带解析器, 共解析328页.
- 对照原文的标题, 表格, 列表, 链接, 组件和强调节点数量一致. 新增的命名锚点单独核对.
- 所有可执行代码行及注释前的语句保持原样; 仅翻译讲解注释. 全部手册合计检查565行代码.
- Nodeworks的93个页内链接均能找到实际命名锚点. 译文保留原链接目标, 为中文标题添加558个锚点别名, 包括大小写兼容和原文遗留链接的兼容别名.
- 锚点使用本地GuideME的 `ATagCompiler` 支持的 `<a name="..." />` 形式, 不将英文锚点显示为标题文字.
- 原文 `storage_card.md#configuring-priority`, `network.md#channel-getall` 和 `variable-handle.md#increment--decrement` 与现有标题不完全对应. 在对应位置添加兼容别名, 不修改原链接.
- 格式占位符, 数值, 组件属性, 图片/结构引用, 表格列数和语言键覆盖检查通过.

证据见 `verification.json`, `native-parser-check.txt`, `ast-structure-review.json` 和 `nodeworks-anchor-links.json`. 未进行游戏内翻页, 点击或画面排版测试. 重载资源或重启客户端后可查看.
