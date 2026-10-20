"""Combine reproducible 1.4.0 language and manual candidate inventories."""
from pathlib import Path
import json,collections,gzip
ROOT=Path(__file__).resolve().parent.parent
REPORT=ROOT/'localization/reports'
language=json.loads((REPORT/'remaining-1.4.0-language-summary.json').read_text())
manual=json.loads((REPORT/'remaining-1.4.0-manuals.json').read_text())
groups=json.loads((REPORT/'remaining-1.4.0-group-labels.json').read_text())
detail=REPORT/'remaining-1.4.0-language-detail.json'
if detail.exists():rows=json.loads(detail.read_text())
else:
 with gzip.open(str(detail)+'.gz','rt') as f:rows=json.load(f)
covered={'official_cjk','project_source_match','reviewed_english','reviewed_cfpa_adopted'}
exact={'cfpa_source_match','pr_source_match'}
review={'renamed_key_same_english','same_key_needs_review','official_needs_json_repair'}
summary={}
for category in ['ordinary','manual_keys']:
 counts=language['counts'][category]
 summary[category]={'existing_candidate_or_reviewed_english':sum(counts.get(s,0) for s in covered),'reviewed_cfpa_adopted':counts.get('reviewed_cfpa_adopted',0),'reviewed_candidate_rejected':counts.get('reviewed_candidate_rejected',0),'source_matching_cfpa_candidates':counts.get('cfpa_source_match',0),'source_matching_pr_candidates':counts.get('pr_source_match',0),'requires_mapping_review_or_repair':sum(counts.get(s,0) for s in review),'no_chinese_candidate':counts.get('no_chinese_candidate',0),'distinct_no_candidate_english_within_namespace':len({(r['namespace'],r['english']) for r in rows if not r['excluded'] and r['category']==category and r['state']=='no_chinese_candidate'})}
summary['group_labels']={'reviewed_cfpa_adopted':groups['counts'].get('reviewed_cfpa_adopted',0),'project_translated':groups['counts'].get('project_translated',0),'reviewed_candidate_rejected':0,'source_matching_pr_candidates':groups['counts'].get('pr_source_match',0),'requires_mapping_review_or_repair':groups['counts'].get('same_key_needs_review',0),'no_chinese_candidate':groups['counts'].get('no_chinese_candidate',0)}
summary['manual_documents']={'formats':manual['totals_by_format'],'remaining_words_after_exact_candidates':sum(r['uncovered_before_CFPA_words']-r['cfpa_exact_english_words'] for r in manual['totals_by_format']),'changed_source_words':sum(r['cfpa_changed_english_words'] for r in manual['totals_by_format']),'no_candidate_words':sum(r['cfpa_none_words'] for r in manual['totals_by_format'])}
summary['reviewed_cfpa_adopted_keys_and_labels']=sum(summary[k]['reviewed_cfpa_adopted'] for k in ['ordinary','manual_keys','group_labels'])
summary['reviewed_candidates_still_withheld']=sum(summary[k]['reviewed_candidate_rejected'] for k in ['ordinary','manual_keys','group_labels'])
summary['old_project_source_changed_keys']=language['project_source_changed_keys']
summary['project_manual_source_unchanged_pages']=sum(r['status']=='unchanged' for r in manual['project_source_validation'])
summary['no_candidate_language_keys_and_group_labels']=sum(summary[k]['no_chinese_candidate'] for k in ['ordinary','manual_keys','group_labels'])
summary['source_matching_cfpa_and_pr_key_candidates']=sum(summary[k].get('source_matching_cfpa_candidates',0)+summary[k].get('source_matching_pr_candidates',0) for k in ['ordinary','manual_keys','group_labels'])
summary['review_mapping_repair_key_candidates']=sum(summary[k]['requires_mapping_review_or_repair'] for k in ['ordinary','manual_keys','group_labels'])
summary['project_translated_group_labels']=summary['group_labels']['project_translated']
summary['method_boundary']='Candidate inventory, not final semantic approval. Current local CFPA all versions, all current open PR changed-file lists, targeted historical closed-unmerged PRs. Exact key and English source matches remain subject to terminology, formatting, source-license and runtime checks. Unknown renamed namespaces/pages, hardcoded text, image text and all historical PRs are not exhaustive. Keys, pages and JSON fields are separate units, never added as pages. English word counts are approximate.'
(REPORT/'remaining-1.4.0-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
lines=['# 1.4.0 剩余汉化工作盘点','','已通过成果已将项目批次与 CFPA 审校按内容去重合并, 见 [合并进度](verified-progress-summary.md). 下表的已审校复用列仅是来源子集, 不另加到合并完成量.','','本次盘点已计入通过构建与独立验证的 CFPA 审校复用包; 原始审校前快照保存在 localization/cfpa_review/inputs/. CFPA 来源版本不限, PR 详见 [缓存审计](cfpa-pr-audit/README.md). 任务书 42/42 章节、4178 键已通过静态检查, 无已知新增待译项; 尚未游戏内验收.','','## 语言键与独立分组名称','','“原文一致候选”表示找到对应英文源一致的中文, 仍须审校、合入及验证, 不计作已完成. “暂无候选”也包含尚需判断是否保留英文的名称/缩写, 不是已逐条批准的待译清单. 同义表达及未知改名仍可能通过后续人工检索复用.','','| 范围 | 已审校复用 | 尚未审校的同源候选 | 需映射/格式修复 | 审校后暂不采用 | 暂无中文候选 |','| --- | ---: | ---: | ---: | ---: | ---: |']
for name,key in [('普通文本','ordinary'),('以语言键承载的手册正文/标题','manual_keys'),('Collapsible Groups 独立 group_lang 名称','group_labels')]:
 r=summary[key];lines.append(f'| {name} | {r["reviewed_cfpa_adopted"]} | {r.get("source_matching_cfpa_candidates",0)+r["source_matching_pr_candidates"]} | {r["requires_mapping_review_or_repair"]} | {r["reviewed_candidate_rejected"]} | {r["no_chinese_candidate"]} |')
lines+=['',f'已审校并构建验证的复用包纳入 {summary["reviewed_cfpa_adopted_keys_and_labels"]} 条语言键/分组名称, {summary["reviewed_candidates_still_withheld"]} 条经审校仍暂不采用.\n合计暂无中文候选 {summary["no_candidate_language_keys_and_group_labels"]} 个键/名称; 原文一致的 CFPA/PR 候选 {summary["source_matching_cfpa_and_pr_key_candidates"]} 条, 另有 {summary["review_mapping_repair_key_candidates"]} 条需映射、复核或修复. 这些类别互斥. 建筑装饰范围、语言文件注释、框架开发示例及 Collective 中未安装模组的专属文本已排除.',f'Collapsible Groups 的 {summary["project_translated_group_labels"]} 条独立分组名由本项目新译并已构建到 group_lang 覆盖包, 不计入复用列.',f'普通文本暂无候选的英文按命名空间和完整值去重后为 {summary["ordinary"]["distinct_no_candidate_english_within_namespace"]} 个不同文本, 可供批次工作量参考; 不同上下文仍可能需要不同译法.',f'已有项目覆盖中另有 {language["project_source_changed_keys"]} 个键的英文源发生变化, 必须复核旧译; 这与上表可能重叠, 不重复相加. 官方或既有中文的“含汉字”只表示静态候选覆盖, 不代表全部语义正确或正文无英文残留.','','## 文档型手册','','此表不含上表手册语言键. Markdown/TXT 按页或文件计, Patchouli 按可见字段计, 不能相加为页数. 已有与审校复用的 '+str(summary['project_manual_source_unchanged_pages'])+' 页手册已通过原文哈希复核, 不代表已安装或游戏内验收.','','| 格式 | 原文一致候选 | 源已变需适配 | 暂无候选 | 剩余新译/适配英文词约数 |','| --- | ---: | ---: | ---: | ---: |']
for r in manual['totals_by_format']:
 unit='字段' if r['format']=='Patchouli' else '页/文件'
 lines.append(f'| {r["format"]} ({unit}) | {r["cfpa_exact_english_units"]} | {r["cfpa_changed_english_units"]+r["cfpa_no_english_source_units"]} | {r["cfpa_none_units"]} | {r["uncovered_before_CFPA_words"]-r["cfpa_exact_english_words"]} |')
d=summary['manual_documents']
lines += ['',f'扣除原文一致候选后的文档工作量约 {d["remaining_words_after_exact_candidates"]} 个英文词: 其中 {d["changed_source_words"]} 词有旧译但原文变化, {d["no_candidate_words"]} 词暂无对应候选. 不是这些词全部都需要从零翻译. 精确候选本身也需要审校和构建验证. 详见 [文档盘点](remaining-1.4.0-manuals.md).','','## 主要缺口','','| 模组/范围 | 暂无中文候选语言键 |','| --- | ---: |']
items=sorted(language['namespace_counts'].items(),key=lambda x:-x[1].get('no_chinese_candidate',0))
for ns,c in items[:15]:lines.append(f'| {ns} | {c.get("no_chinese_candidate",0)} |')
lines+=['','文档型手册剩余主要集中于 Nautec、AE2、Stellaris、Kindred Spirits、Colossal Reactors、Auroral 等; 是否列作关键手册需按主线引用和使用门槛判断, 不把所有手册自动提前.','','## 统计边界与重跑','','- 本地 CFPA 固定提交 `'+language['cfpa_commit']+'`, 遍历全部版本目录的 JSON 和旧式 .lang 候选; 不将跨版本候选视为已适配资源包, 不以各版本盲目叠加替代打包规则. PR 同样固定 head SHA.','- 开放 PR 全量检索, 兼容新旧目录布局. 历史关闭但未合并 PR 仅定向检索, 未穷举; 总数与查询范围以 PR 审计为准. 来源版本差异、未知命名空间迁移、页面改名可能仍有未识别的可复用译文.','- 已排除建筑装饰、开发文档、框架示例, 不自动认定所有资源键在当前界面可见; 原生动态生成文本、硬编码文本、图片文字与游戏内加载优先级未穷尽.','- 普通语言扫描含嵌套 JAR 语言文件; 手册文档扫描以顶层 JAR 与 KubeJS 资源为主, 完整方法见各报告. 无 PR 审查通过或语言质量保证.','- JSON 解析异常和宽松恢复已记录于 language-summary.json, 有原生中文但需修复的条目与新译分开. 未改源 JAR.','- 静态候选会高估可用覆盖, 未映射的跨版本译文又可能高估新译量. 本报告是排期基线, 不是最终验收证明.','','```bash','python localization/assess_1_4_remaining.py','python localization/assess_1_4_manuals.py','python localization/assess_1_4_group_labels.py','python localization/summarize_remaining_1_4.py','```','','输入证据保存于 `cfpa-pr-audit/`, 以上命令只重算本地快照, 不自动刷新 GitHub PR. 普通/手册语言键明细为 `remaining-1.4.0-language-detail.json.gz`, summary JSON 保留分类总量与解析异常.']
(REPORT/'remaining-1.4.0-summary.md').write_text('\n'.join(lines)+'\n')
# Preserve full provenance with a compact generated artifact rather than a large JSON.
if detail.exists():
 with detail.open('rb') as source,gzip.open(str(detail)+'.gz','wb') as dest:
  import shutil
  shutil.copyfileobj(source,dest)
 detail.unlink()
print(json.dumps(summary,ensure_ascii=False,indent=2))
