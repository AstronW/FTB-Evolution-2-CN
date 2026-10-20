"""Static remaining-work assessment. Does not modify game resources."""
import collections
import contextlib
import io
import json
import pathlib
import re
import runpy

ROOT = pathlib.Path(__file__).resolve().parent.parent
scope = json.loads((ROOT / 'localization/language_scope.json').read_text())
def exclusion(namespace):
    if namespace in scope['excluded_namespaces']:
        return scope['excluded_namespaces'][namespace]
    return next((reason for prefix, reason in scope['excluded_namespace_prefixes'].items() if namespace.startswith(prefix)), '')
with contextlib.redirect_stdout(io.StringIO()):
    inventory = runpy.run_path(str(ROOT / 'localization/assess_manuals.py'))
langs = inventory['langs']
# Minecraft language keys share a global key space across resource namespaces.
zh = {}
for (namespace, locale), values in langs.items():
    if locale == 'zh_cn':
        zh.update(values)
seen = set()
rows = []
total = collections.Counter()
excluded_total = collections.Counter()
for (namespace, locale), en in langs.items():
    if locale != 'en_us':
        continue
    counts = collections.Counter()
    missing = []
    for key, value in en.items():
        if key in seen or not isinstance(value, str) or not re.search('[A-Za-z]', value):
            continue
        seen.add(key)
        if key.startswith(inventory['prefixes']) or (namespace, key) in inventory['referenced']:
            continue
        translation = zh.get(key)
        state = ('cjk' if isinstance(translation, str) and inventory['cjk'].search(translation)
                 else 'absent' if translation is None else 'latin_or_symbols')
        counts[state] += 1
        if state != 'cjk':
            missing.append(dict(key=key, english=value, zh_cn=translation, state=state))
    reason = exclusion(namespace)
    (excluded_total if reason else total).update(counts)
    rows.append(dict(namespace=namespace, excluded=bool(reason), exclusion_reason=reason, counts=dict(counts), missing_candidates=missing,
                     distinct_missing_english=len({x['english'] for x in missing if x['state']=='absent'})))
result = dict(method='Global language keys, deduplicated across namespaces, excluding recognized handbook keys. CJK presence is candidate coverage only. Absent means no parsed zh_cn key. Latin/symbol values may be legitimate names or units. Mod-generated resources, hardcoded text, images and in-game visibility are not comprehensively assessed.',
              counts=dict(total), excluded_counts=dict(excluded_total), scope=scope,
              namespaces=sorted(rows, key=lambda x:-x['counts'].get('absent',0)))
(ROOT / 'localization/reports/language-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result['counts']))
print('Excluded:', json.dumps(result['excluded_counts']))
for row in [r for r in result['namespaces'] if not r['excluded']][:15]:
    print(row['namespace'], row['counts'], 'distinct', row['distinct_missing_english'])
