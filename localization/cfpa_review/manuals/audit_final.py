"""Validate the reviewed CFPA manual decisions against their pinned target inputs."""
import collections
import hashlib
import json
import pathlib
import sys
import zipfile

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'localization'))
from cfpa_review_format import invariant_errors

rows = json.loads((ROOT / 'localization/cfpa_review/decisions/manuals.json').read_text())
issues = json.loads((BASE / 'structural-problems.json').read_text())
reviewed = []
for issue in issues:
    path, field = issue['path'], issue.get('field')
    row = next(r for r in rows if r['path'] == path and r['field'] == field)
    if path.endswith('/export_bus.md') and issue['type'] == 'tags':
        # This is a page-local recipe source typo, not a blanket component bypass.
        expected = collections.Counter(x.replace('id="import_bus"', 'id="export_bus"') for x in issue['en'])
        actual = collections.Counter(x for x in issue['zh'] if not x.startswith('<a name=') and x != '</a>')
        assert expected == actual, issue
        reason = '当前英文输出总线页误用输入总线配方; 修正为本页 export_bus 配方, 其他组件逐项相同'
    else:
        exceptions = row['validation_exceptions']
        assert issue['type'] == 'patchouli_macros' and any(e['error'] == 'Patchouli controls' for e in exceptions), issue
        reason = next(e['reason'] for e in exceptions if e['error'] == 'Patchouli controls')
    reviewed.append({**issue, 'reviewed_reason': reason})

seen = set()
for row in rows:
    identity = (row['path'], row['field'])
    assert identity not in seen, identity
    seen.add(identity)
    source_path = pathlib.Path(row['source']['target_source'])
    raw = (zipfile.ZipFile(source_path).read(row['path']).decode() if source_path.suffix == '.jar' else source_path.read_text()).replace('\r\n', '\n')
    if row['format'] == 'Patchouli':
        obj = json.loads(raw)
        for part in row['field'].split('.'):
            obj = obj[int(part)] if isinstance(obj, list) else obj[part]
        assert obj == row['english'], identity
        source_text = obj
        errors = invariant_errors(source_text, row['chinese'])
        assert set(errors) == {e['error'] for e in row['validation_exceptions']}, (identity, errors)
    else:
        source_text = raw
        if row['status'] == 'accepted':
            output = ROOT / row['file']
            assert output.is_file(), output
            row['chinese_sha256'] = hashlib.sha256(output.read_bytes()).hexdigest()
    assert hashlib.sha256(source_text.encode()).hexdigest() == row['english_sha256'], identity
    assert row['output_resource_path'].startswith('assets/'), identity
    if row['source'].get('pr'):
        assert row['source']['head_sha'] and row['source']['author']
        assert row['source']['review_status'] == 'local_reviewed_with_cached_discussion'

(BASE / 'structural-reviewed-differences.json').write_text(json.dumps(reviewed, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'localization/cfpa_review/decisions/manuals.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
result = {
    'decision_units': len(rows),
    'accepted_documents': sum(r['format'] == 'Markdown/MDX' and r['status'] == 'accepted' for r in rows),
    'accepted_patchouli_fields': sum(r['format'] == 'Patchouli' and r['status'] == 'accepted' for r in rows),
    'rejected_documents': sum(r['status'] == 'rejected' for r in rows),
    'reviewed_structure_exceptions': len(reviewed),
    'patchouli_fields_with_exact_exceptions': sum(bool(r['validation_exceptions']) for r in rows if r['format'] == 'Patchouli'),
    'target_sources_fresh': True,
    'unique_decisions': True,
    'game_tested': False,
}
(BASE / 'final-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
