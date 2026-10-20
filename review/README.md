# 汉化审查网页

按模组分组对照英文原文与当前生效的中文译文, 支持折叠、搜索、过滤和审查标记. 只读取源文与发布包, 不写游戏实例.

## 使用

```bash
python review/export.py          # 重新生成对照数据 (发布包或模组更新后运行)
npm --prefix review/app install  # 首次
npm --prefix review/app run dev  # http://localhost:5178
```

## 数据来源

`export.py` 按游戏资源优先级分层合并 (低 → 高): 模组 JAR (含 jar-in-jar) → 实例 `kubejs/assets` → `dist/FTB-Evolution-2-1.4.0-zh_CN-install.zip`.

| 类型 | 英文 | 中文 |
| --- | --- | --- |
| 语言键 (含 `group_lang`) | 各层 `en_us.json` 合并 | 各层 `zh_cn.json` 合并, 项目译文覆盖上游时另显示上游原译 |
| GuideME / Oracle Index 手册 | 原路径 `.md/.mdx` | `_zh_cn/` 或 `translated/zh_cn/` 对应页, 整页对照 |
| Patchouli 手册 | `en_us/**.json` 可见字段 | `zh_cn/` 同一 JSON 路径; 值为语言键的字段由语言键覆盖 |
| Stellaris Wiki | JAR `data/stellaris/wiki` | 发布包数据包同路径 |
| 任务书 | 实例 `config/ftbquests/quests/lang/en_us` | 发布包 `zh_cn`, 否则实例现有 `zh_cn` |
| 整合包特色内容 | `localization/custom/batches/*/sources` 快照 | 发布包或工作副本输出; JSON 按字段, 脚本按改动行 |

来源标签: 项目译文 = 本项目发布包; 整合包自带 = 实例 kubejs/任务书原有中文; 模组自带 = JAR 内 `zh_cn`; 缺失 = 无中文. 排除范围按 `localization/language_scope.json` 标记, 默认隐藏.

页面统计的"缺失"是全部英文键的直观对照, 未按阶段报告的可见性/保留规则扣除, 不替代 `localization/reports` 中的剩余量结论.

## 审查标记

保存在 `review/marks.json`, 每条记录标记时英中文本的哈希. 原文或译文变化后该标记显示为"已过期", 可用状态过滤找出重新审查. 重新导出数据不会清除标记.
