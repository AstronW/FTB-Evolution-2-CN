# 1.4.0 剩余汉化工作盘点

本次只读盘点, 未翻译正文或采用上游候选. CFPA 来源版本不限, PR 详见 [缓存审计](cfpa-pr-audit/README.md). 任务书 42/42 章节、4178 键已通过静态检查, 无已知新增待译项; 尚未游戏内验收.

## 语言键与独立分组名称

“原文一致候选”表示找到对应英文源一致的中文, 仍须审校、合入及验证, 不计作已完成. “暂无候选”也包含尚需判断是否保留英文的名称/缩写, 不是已逐条批准的待译清单. 同义表达及未知改名仍可能通过后续人工检索复用.

| 范围 | CFPA 原文一致候选 | PR 原文一致候选 | 需映射/复核/格式修复 | 暂无中文候选 |
| --- | ---: | ---: | ---: | ---: |
| 普通文本 | 4609 | 737 | 689 | 10030 |
| 以语言键承载的手册正文/标题 | 280 | 910 | 90 | 1835 |
| Collapsible Groups 独立 group_lang 名称 | 0 | 235 | 5 | 20 |

合计暂无中文候选 11885 个键/名称; 原文一致的 CFPA/PR 候选 6771 条, 另有 784 条需映射、复核或修复. 这些类别互斥. 建筑装饰范围、语言文件注释、框架开发示例及 Collective 中未安装模组的专属文本已排除.
普通文本暂无候选的英文按命名空间和完整值去重后为 9450 个不同文本, 可供批次工作量参考; 不同上下文仍可能需要不同译法.
已有项目覆盖中另有 16 个键的英文源发生变化, 必须复核旧译; 这与上表可能重叠, 不重复相加. 官方或既有中文的“含汉字”只表示静态候选覆盖, 不代表全部语义正确或正文无英文残留.

## 文档型手册

此表不含上表手册语言键. Markdown/TXT 按页或文件计, Patchouli 按可见字段计, 不能相加为页数. 已完成的 164 页手册原文全部未变, 可复用.

| 格式 | 原文一致候选 | 源已变需适配 | 暂无候选 | 剩余新译/适配英文词约数 |
| --- | ---: | ---: | ---: | ---: |
| Markdown/MDX (页/文件) | 74 | 132 | 305 | 124756 |
| Patchouli (字段) | 502 | 6 | 557 | 8890 |
| Bestiary TXT (页/文件) | 0 | 0 | 1 | 3 |

扣除原文一致候选后的文档工作量约 133649 个英文词: 其中 32164 词有旧译但原文变化, 101485 词暂无对应候选. 不是这些词全部都需要从零翻译. 精确候选本身也需要审校和构建验证. 详见 [文档盘点](remaining-1.4.0-manuals.md).

## 主要缺口

| 模组/范围 | 暂无中文候选语言键 |
| --- | ---: |
| anima [manual_keys] | 997 |
| energizedpower [ordinary] | 395 |
| arsmagicalegacy [manual_keys] | 340 |
| hats [ordinary] | 332 |
| kindredspirits [ordinary] | 331 |
| anima [ordinary] | 299 |
| logisticsnetworks [ordinary] | 277 |
| cakesticklib [ordinary] | 268 |
| collapsible_groups [ordinary] | 246 |
| xycraft_world [ordinary] | 224 |
| occultism [manual_keys] | 217 |
| ftbarmory [ordinary] | 212 |
| travelerstitles [ordinary] | 196 |
| betterfishtanks [ordinary] | 185 |
| occultism [ordinary] | 185 |

文档型手册剩余主要集中于 Nautec、AE2、Stellaris、Kindred Spirits、Colossal Reactors、Auroral 等; 是否列作关键手册需按主线引用和使用门槛判断, 不把所有手册自动提前.

## 统计边界与重跑

- 本地 CFPA 固定提交 `719672954d9df4ea51877e3d5ce2912148273682`, 遍历全部版本目录的 JSON 和旧式 .lang 候选; 不将跨版本候选视为已适配资源包, 不以各版本盲目叠加替代打包规则. PR 同样固定 head SHA.
- 开放 PR 全量检索, 兼容新旧目录布局. 历史关闭但未合并 PR 仅定向检索, 未穷举; 总数与查询范围以 PR 审计为准. 来源版本差异、未知命名空间迁移、页面改名可能仍有未识别的可复用译文.
- 已排除建筑装饰、开发文档、框架示例, 不自动认定所有资源键在当前界面可见; 原生动态生成文本、硬编码文本、图片文字与游戏内加载优先级未穷尽.
- 普通语言扫描含嵌套 JAR 语言文件; 手册文档扫描以顶层 JAR 与 KubeJS 资源为主, 完整方法见各报告. 无 PR 审查通过或语言质量保证.
- JSON 解析异常和宽松恢复已记录于 language-summary.json, 有原生中文但需修复的条目与新译分开. 未改源 JAR.
- 静态候选会高估可用覆盖, 未映射的跨版本译文又可能高估新译量. 本报告是排期基线, 不是最终验收证明.

```bash
python localization/assess_1_4_remaining.py
python localization/assess_1_4_manuals.py
python localization/assess_1_4_group_labels.py
python localization/summarize_remaining_1_4.py
```

输入证据保存于 `cfpa-pr-audit/`, 以上命令只重算本地快照, 不自动刷新 GitHub PR. 普通/手册语言键明细为 `remaining-1.4.0-language-detail.json.gz`, summary JSON 保留分类总量与解析异常.
