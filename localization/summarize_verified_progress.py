"""Merge verified batches and reviewed CFPA resources without double counting."""
import gzip
import json
from collections import defaultdict
from pathlib import Path
from reviewed_cfpa_overlay import load_verified_review

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / 'localization/reports'

def read(path):
    return json.loads(path.read_text())

def main():
    language, manuals = load_verified_review()
    with gzip.open(REPORT / 'remaining-1.4.0-language-detail.json.gz', 'rt') as source:
        inventory = json.load(source)
    categories = {r['key']: r['category'] for r in inventory if not r['excluded']}
    languages = defaultdict(set)
    groups = defaultdict(set)
    pages = defaultdict(set)
    fields = defaultdict(set)
    batch_count = 0
    for proof in sorted((ROOT / 'localization/ordinary').glob('batch-*/verification.json')):
        assert read(proof)['status'] == 'passed', proof
        batch_count += 1
        for key in read(proof.parent / 'source-en_us.json'):
            languages[key].add(proof.parent.name)
    batch_keys = set(languages)
    reviewed_language_keys = set()
    for row in language:
        if row['status'] != 'accepted':
            continue
        if row.get('resource_domain') == 'group_lang':
            groups[row['key']].add('cfpa_review')
        else:
            languages[row['key']].add('cfpa_review')
            reviewed_language_keys.add(row['key'])
    project_groups = json.loads((ROOT / 'localization/manuals/group_lang-zh.json').read_text())
    for key in project_groups:
        groups[key].add('project_group_lang')
    paths = {'ftb': 'guides/ftb', 'ftbic': 'ftbic', 'nodeworks': 'nodeworksguide'}
    for page in read(ROOT / 'localization/manuals/source_manifest.json'):
        ns, rel = page.split('/', 1)
        pages[f'assets/{ns}/{paths[ns]}/{rel}'].add('project_manuals')
    original_pages = set(pages)
    for row in manuals:
        if row['status'] != 'accepted':
            continue
        if row['format'] == 'Markdown/MDX':
            pages[row['path']].add('cfpa_review')
        elif row['format'] == 'Patchouli':
            fields[(row['path'], row['field'])].add('cfpa_review')
    ordinary = {key for key in languages if categories.get(key) != 'manual_keys'}
    manual_keys = set(languages) - ordinary
    stats = {
        'ordinary_language_keys': len(ordinary),
        'manual_language_keys': len(manual_keys),
        'all_language_keys': len(languages),
        'group_labels': len(groups),
        'manual_pages': len(pages),
        'patchouli_visible_fields': len(fields),
        'original_batches': batch_count,
        'original_batch_keys': len(batch_keys),
        'reviewed_cfpa_language_keys': len(reviewed_language_keys),
        'batch_cfpa_key_overlap': len(batch_keys & reviewed_language_keys),
        'original_manual_pages': len(original_pages),
        'reviewed_manual_pages': sum('cfpa_review' in v for v in pages.values()),
        'manual_page_overlap': sum(len(v) > 1 for v in pages.values()),
        'batch_keys_classified_as_manual': sum(categories.get(k) == 'manual_keys' for k in batch_keys),
        'batch_keys_outside_latin_inventory_retained_as_ordinary': sum(k not in categories for k in batch_keys),
    }
    assert stats['all_language_keys'] == stats['ordinary_language_keys'] + stats['manual_language_keys']
    data = {'target_pack_version': '1.4.0', 'scope': 'Verified ordinary batches plus reviewed CFPA and project manual pages; excludes quests and pack-custom text to avoid implying full-project totals',
            'in_game_tested': False, 'stats': stats,
            'language_keys': [{'key': k, 'category': 'manual_keys' if k in manual_keys else 'ordinary', 'sources': sorted(v)} for k, v in sorted(languages.items())],
            'group_labels': [{'key': k, 'sources': sorted(v)} for k, v in sorted(groups.items())],
            'manual_pages': [{'path': k, 'sources': sorted(v)} for k, v in sorted(pages.items())],
            'patchouli_fields': [{'path': k[0], 'field': k[1], 'sources': sorted(v)} for k, v in sorted(fields.items())]}
    with gzip.open(REPORT / 'verified-progress-detail.json.gz', 'wt', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False)
    (REPORT / 'verified-progress-summary.json').write_text(json.dumps({k:v for k,v in data.items() if k in ['target_pack_version','scope','in_game_tested','stats']}, ensure_ascii=False, indent=2)+'\n')
    text = f'''# 已通过静态检查的汉化成果合并统计

普通文本与手册的完成量统一包含项目批次和已审校 CFPA, 不再将 CFPA 另列为未计入的增量. 译文资源包保持各自的可维护来源与许可证, 此处合并统计及验收口径.

| 内容 | 去重后已通过数量 |
| --- | ---: |
| 普通语言键 | {len(ordinary)} |
| 手册语言键 | {len(manual_keys)} |
| 独立分组名称 | {len(groups)} |
| 文档型手册页面 | {len(pages)} |
| Patchouli 可见字段 | {len(fields)} |

语言键合计 {len(languages)} 个. 页面、字段和语言键不能直接相加为完成条数.

## 来源及去重核对

- {batch_count} 个已通过普通文本批次: {len(batch_keys)} 键. 其中 {stats['batch_keys_classified_as_manual']} 键按当前内容分类计入手册, 其余 {len(batch_keys)-stats['batch_keys_classified_as_manual']} 键计入普通文本 (包括 {stats['batch_keys_outside_latin_inventory_retained_as_ordinary']} 个不在含拉丁文本扫描集合中的既有名称或格式值).
- CFPA 审校语言: {len(reviewed_language_keys)} 键, 与上述批次重叠 {stats['batch_cfpa_key_overlap']} 键. 其中普通文本 6028 键, 手册语言 1276 键; 分组另计 76 条.
- 文档手册: 原项目 {len(original_pages)} 页 + CFPA 审校 {stats['reviewed_manual_pages']} 页, 重叠 {stats['manual_page_overlap']} 页 = {len(pages)} 页. 此前的 369 页已经是合并量, 不能再加 205 页.
- Patchouli 的 508 个字段分布于 151 个输出文档, 按字段统计, 不称为 508 页.

语言键以完整键名去重 (Minecraft 语言表的全局键); 页面以英文资源路径去重, Patchouli 以路径与字段位置去重. 逐条来源存于 `verified-progress-detail.json.gz`. 兼容旧名称不计当前原生键, 未完成草稿不计完成量.

## 统计边界与验证

这是原普通语言批次与手册的成果合并, 不包括单独统计的任务书 4178 键与整合包自定义文案, 也不是全部模组自带中文的覆盖总量. 不因合并而宣称其他组件已全量适配 1.4.0. 不变更实际游戏资源包或复制安装译文.

统计读取已通过的批次记录, 并通过 `load_verified_review` 校验 CFPA 构建清单、审校决定与产物哈希. 全量静态校验使用 `python project.py check`, 统计重建使用 `python localization/summarize_verified_progress.py`. 静态通过与游戏内验收分开; 游戏内尚未验收.
'''
    (REPORT / 'verified-progress-summary.md').write_text(text)
    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
