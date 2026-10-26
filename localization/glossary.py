"""Canonical terminology base: lookup, consistency check and export.

`glossary/glossary.json` holds one record per decided concept, scoped by
namespace (and optionally quest chapter).  It is a reference and a checker,
never a replacement dictionary: nothing here rewrites translations.

  python localization/glossary.py lookup <text> [--legacy]
  python localization/glossary.py check [--strict]
  python localization/glossary.py suggest-keys <namespace> <English>
  python localization/glossary.py export [--format tsv|csv] [--output PATH]
  python localization/glossary.py stats
"""
from __future__ import annotations

import argparse
import collections
import csv
import fnmatch
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MC = ROOT / '.minecraft'
BASE = ROOT / 'localization/glossary'
GLOSSARY = BASE / 'glossary.json'

FIELDS = {'id', 'en', 'zh', 'namespaces', 'quest_chapters', 'keys', 'category', 'avoid',
          'allow', 'keep_english', 'note', 'source', 'status'}
REQUIRED = {'id', 'en', 'zh', 'namespaces', 'source', 'status'}
STATUSES = {'approved', 'pending'}
CATEGORIES = {'mod_name', 'item', 'block', 'entity', 'fluid', 'effect', 'mechanic', 'ui',
              'material', 'tier', 'concept', 'place', 'unit', 'proper_noun'}
ID_PATTERN = re.compile(r'^[a-z0-9_*]+(\.[a-z0-9_]+)+$')

# Project-maintained Chinese outputs, in the same first-wins order the release
# merge uses (KubeJS overlays, reviewed CFPA, manuals).
LANG_OUTPUTS = [
    MC / 'kubejs/assets',
    MC / 'resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN/assets',
    MC / 'resourcepacks/FTB-Evolution-2-Manuals-zh_CN/assets',
]
CFPA_CONVERTED = MC / 'resourcepacks/Minecraft-Mod-Language-Modpack-Converted-26.1.2.zip'
QUEST_LANG = MC / 'config/ftbquests/quests/lang/zh_cn'
MANUAL_ROOTS = [
    MC / 'resourcepacks/FTB-Evolution-2-Manuals-zh_CN/assets',
    MC / 'resourcepacks/FTB-Evolution-2-CFPA-Reviewed-zh_CN/assets',
    MC / 'datapacks/ftb_evolution_cn/data',
]
LEGACY = {
    'terms.json (任务书)': ROOT / 'localization/terms.json',
    'manuals/terms.json (手册)': ROOT / 'localization/manuals/terms.json',
    'manuals/nodeworks-terms.json': ROOT / 'localization/manuals/nodeworks-terms.json',
}
CFPA_TERMS = ROOT / 'localization/cfpa_review/terms.json'
EXTRA_GLOSSARIES = ROOT / 'localization/manuals_extra/glossaries'
LINE_KEY = re.compile(r'^\s*"([^"]+)"\s*:')


def load_glossary(path=GLOSSARY):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_schema(data):
    """Return a list of structural errors; an empty list means usable data."""
    errors = []
    seen = set()
    scoped = {}
    for index, entry in enumerate(data.get('entries', [])):
        where = entry.get('id', f'#{index}')
        unknown = set(entry) - FIELDS
        missing = REQUIRED - set(entry)
        if unknown:
            errors.append(f'{where}: unknown fields {sorted(unknown)}')
        if missing:
            errors.append(f'{where}: missing fields {sorted(missing)}')
            continue
        if not ID_PATTERN.match(entry['id']):
            errors.append(f'{where}: id must look like namespace.concept')
        if entry['id'] in seen:
            errors.append(f'{where}: duplicate id')
        seen.add(entry['id'])
        if entry['status'] not in STATUSES:
            errors.append(f'{where}: status must be one of {sorted(STATUSES)}')
        if entry.get('category') and entry['category'] not in CATEGORIES:
            errors.append(f'{where}: unknown category {entry["category"]}')
        if not entry['namespaces'] or not all(isinstance(n, str) for n in entry['namespaces']):
            errors.append(f'{where}: namespaces must be a non-empty list')
        if entry.get('keep_english') and entry['zh'] != entry['en']:
            errors.append(f'{where}: keep_english requires zh == en')
        for variant in entry.get('avoid', []):
            if variant == entry['zh'] or (variant in entry['zh'] and not entry.get('allow')):
                # A forbidden substring of the canonical term would flag every use.
                errors.append(f'{where}: avoid variant "{variant}" overlaps the canonical term')
        if re.search(r'[，。：；！？（）【】“”‘’、]', entry['zh']):
            errors.append(f'{where}: canonical term must use ASCII punctuation')
        # One approved meaning per English term inside one namespace.
        if entry['status'] == 'approved':
            for namespace in entry['namespaces']:
                marker = (namespace, entry['en'].casefold(), entry.get('category'))
                other = scoped.get(marker)
                if other and other[1] != entry['zh']:
                    errors.append(f'{where}: conflicts with {other[0]} for "{entry["en"]}" in {namespace}')
                scoped.setdefault(marker, (entry['id'], entry['zh']))
    return errors


class Resources:
    """Lazy view of effective zh_cn / en_us language values."""

    def __init__(self):
        self._zh = {}
        self._en = {}
        self._jars = None

    def _jar_index(self):
        if self._jars is None:
            self._jars = collections.defaultdict(list)
            for jar in sorted((MC / 'mods').glob('*.jar')) if (MC / 'mods').is_dir() else []:
                try:
                    with zipfile.ZipFile(jar) as archive:
                        for name in archive.namelist():
                            match = re.match(r'assets/([^/]+)/lang/(zh_cn|en_us)\.json$', name)
                            if match:
                                self._jars[(match[1], match[2])].append((jar, name))
                except (OSError, zipfile.BadZipFile):
                    continue
        return self._jars

    def _jar_lang(self, namespace, language):
        values = {}
        for jar, member in self._jar_index().get((namespace, language), []):
            try:
                with zipfile.ZipFile(jar) as archive:
                    for key, value in json.loads(archive.read(member)).items():
                        values.setdefault(key, (value, f'jar:{jar.name}'))
            except (OSError, ValueError, zipfile.BadZipFile):
                continue
        return values

    def zh(self, namespace):
        if namespace not in self._zh:
            values = {}
            for root in LANG_OUTPUTS:
                path = root / namespace / 'lang/zh_cn.json'
                if path.is_file():
                    for key, value in json.loads(path.read_text(encoding='utf-8')).items():
                        values.setdefault(key, (value, str(path.relative_to(ROOT))))
            if CFPA_CONVERTED.is_file():
                with zipfile.ZipFile(CFPA_CONVERTED) as archive:
                    member = f'assets/{namespace}/lang/zh_cn.json'
                    if member in archive.namelist():
                        for key, value in json.loads(archive.read(member)).items():
                            values.setdefault(key, (value, 'cfpa-converted'))
            for key, value in self._jar_lang(namespace, 'zh_cn').items():
                values.setdefault(key, value)
            self._zh[namespace] = values
        return self._zh[namespace]

    def en(self, namespace):
        if namespace not in self._en:
            values = {}
            path = MC / f'kubejs/assets/{namespace}/lang/en_us.json'
            if path.is_file():
                for key, value in json.loads(path.read_text(encoding='utf-8')).items():
                    values[key] = (value, str(path.relative_to(ROOT)))
            for key, value in self._jar_lang(namespace, 'en_us').items():
                values.setdefault(key, value)
            self._en[namespace] = values
        return self._en[namespace]


def key_namespace(key):
    """Best guess of the asset namespace: `item.<ns>.x` style, else the first segment."""
    parts = key.split('.')
    return parts[1] if len(parts) > 2 else parts[0]


def text_units():
    """Yield (scope, location, text) for every maintained Chinese output.

    scope is a namespace, or `quest:<chapter>` for quest-book chapters.
    """
    for root in LANG_OUTPUTS:
        for path in sorted(root.glob('*/lang/zh_cn.json')):
            namespace = path.parent.parent.name
            for key, value in json.loads(path.read_text(encoding='utf-8')).items():
                if isinstance(value, str):
                    yield namespace, f'{path.relative_to(ROOT)}:{key}', value
    for path in sorted(QUEST_LANG.rglob('*.json5')):
        scope = 'quest:' + path.stem if path.parent.name == 'chapters' else 'quest:_' + path.stem
        key = ''
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            match = LINE_KEY.match(line)
            if match:
                key = match[1]
            yield scope, f'{path.relative_to(ROOT)}:{number} {key}', line
    for root in MANUAL_ROOTS:
        for path in sorted(root.rglob('*')):
            if path.suffix not in {'.md', '.mdx', '.json'} or path.name == 'zh_cn.json' and path.parent.name == 'lang':
                continue
            parts = path.relative_to(root).parts
            if path.suffix == '.json' and 'zh_cn' not in parts:
                continue
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                yield parts[0], f'{path.relative_to(ROOT)}:{number}', line


def in_scope(entry, scope):
    namespaces = entry['namespaces']
    if '*' in namespaces:
        return True
    if scope.startswith('quest:'):
        chapter = scope[len('quest:'):]
        return any(fnmatch.fnmatch(chapter, pattern) for pattern in entry.get('quest_chapters', []))
    return any(fnmatch.fnmatch(scope, pattern) for pattern in namespaces)


def find_avoided(entry, text):
    """Return forbidden variants present in text once canonical/allowed uses are masked."""
    masked = text
    for allowed in sorted([entry['zh'], *entry.get('allow', [])], key=len, reverse=True):
        masked = masked.replace(allowed, '\0')
    return [variant for variant in entry.get('avoid', []) if variant in masked]


def known_issue(data, entry_id, location):
    """Return the recorded issue covering this finding, if any."""
    for issue in data.get('known_issues', []):
        if issue['entry'] == entry_id and any(part in location for part in issue['locations']):
            return issue
    return None


def check(strict=False):
    data = load_glossary()
    errors = validate_schema(data)
    warnings = []
    entries = data['entries']
    ids = {entry['id'] for entry in entries}
    for issue in data.get('known_issues', []):
        if issue.get('entry') not in ids or not issue.get('locations') or not issue.get('reason'):
            errors.append(f'known issue {issue.get("entry")}: needs an existing entry, locations and reason')
    used_issues = set()
    resources = Resources()
    jar_available = (MC / 'mods').is_dir() and any((MC / 'mods').glob('*.jar'))

    for entry in entries:
        for key in entry.get('keys', []):
            # Key shape does not always reveal the asset namespace, so also try the entry scope.
            candidates = [key_namespace(key)] + [n for n in entry['namespaces'] if '*' not in n]
            namespace = next((n for n in candidates if key in resources.zh(n)), candidates[0])
            found = resources.zh(namespace).get(key)
            if not found:
                (errors if jar_available else warnings).append(
                    f'{entry["id"]}: key {key} not found in effective zh_cn')
                continue
            value, origin = found
            if value != entry['zh']:
                message = f'{entry["id"]}: {key} shows "{value}" ({origin}), glossary says "{entry["zh"]}"'
                issue = known_issue(data, entry['id'], f'{origin}:{key}')
                if issue:
                    used_issues.add(id(issue))
                    warnings.append('known issue ' + message)
                else:
                    errors.append(message)
            english = resources.en(namespace).get(key)
            if english and english[0] != entry['en']:
                warnings.append(f'{entry["id"]}: English source of {key} is now "{english[0]}", '
                                f'glossary records "{entry["en"]}"; review before reuse')

    avoiders = [entry for entry in entries if entry.get('avoid')]
    hits = collections.defaultdict(list)
    for scope, location, text in text_units():
        for entry in avoiders:
            if in_scope(entry, scope):
                for variant in find_avoided(entry, text):
                    hits[(entry['id'], variant)].append(location)
    for (entry_id, variant), locations in sorted(hits.items()):
        known = []
        for location in locations:
            issue = known_issue(data, entry_id, location)
            if issue:
                used_issues.add(id(issue))
                known.append(location)
        fresh = [location for location in locations if location not in known]
        if known:
            warnings.append(f'known issue {entry_id}: "{variant}" still in {len(known)} recorded place(s)')
        if fresh:
            sample = '; '.join(fresh[:3]) + (f' (+{len(fresh) - 3})' if len(fresh) > 3 else '')
            errors.append(f'{entry_id}: avoided variant "{variant}" in {len(fresh)} place(s): {sample}')
    for issue in data.get('known_issues', []):
        if id(issue) not in used_issues:
            # Fixed issues must be removed so the record stays truthful.
            warnings.append(f'known issue {issue["entry"]} no longer reproduces; remove it from known_issues')

    pending = sum(entry['status'] == 'pending' for entry in entries)
    if pending:
        warnings.append(f'{pending} pending entries are not canonical yet')
    for line in warnings:
        print('WARN ' + line)
    for line in errors:
        print('FAIL ' + line)
    failed = errors or (strict and warnings)
    print(f'{"FAILED" if failed else "PASSED"}: {len(entries)} entries, '
          f'{sum(len(e.get("keys", [])) for e in entries)} bound keys, '
          f'{len(errors)} errors, {len(warnings)} warnings')
    return 1 if failed else 0


def legacy_rows():
    for label, path in LEGACY.items():
        for english, chinese in json.loads(path.read_text(encoding='utf-8')).items():
            yield label, english, chinese, ''
    for record in json.loads(CFPA_TERMS.read_text(encoding='utf-8'))['records']:
        yield 'cfpa_review/terms.json', record['english'], record['chinese'], record['namespace']
    for path in sorted(EXTRA_GLOSSARIES.glob('*.json')):
        # Keyed by language key: {"en": ..., "zh": ...}.
        for key, pair in json.loads(path.read_text(encoding='utf-8')).items():
            if isinstance(pair, dict) and pair.get('en') and pair.get('zh'):
                yield f'manuals_extra/glossaries/{path.name}', pair['en'], pair['zh'], key


def lookup(query, legacy=False):
    folded = query.casefold()
    found = False
    data = load_glossary()
    for entry in data['entries']:
        haystack = [entry['id'], entry['en'], entry['zh'], *entry.get('avoid', []), *entry.get('keys', [])]
        if any(folded in value.casefold() for value in haystack):
            found = True
            flag = '' if entry['status'] == 'approved' else ' [待定]'
            print(f'{entry["en"]} = {entry["zh"]}{flag}  ({entry["id"]}; 范围 {", ".join(entry["namespaces"])})')
            if entry.get('avoid'):
                print(f'  不用: {", ".join(entry["avoid"])}')
            if entry.get('note'):
                print(f'  说明: {entry["note"]}')
            print(f'  来源: {entry["source"]}')
            for issue in data.get('known_issues', []):
                if issue['entry'] == entry['id']:
                    print(f'  已知问题: {issue["reason"]}')
    if legacy:
        for label, english, chinese, scope in legacy_rows():
            if folded in english.casefold() or folded in chinese.casefold():
                found = True
                print(f'[参考, 未复核] {english} = {chinese}  ({label}{"; " + scope if scope else ""})')
    if not found:
        print('未找到. 先查官方中文/CFPA, 按 TERMINOLOGY.md 流程裁决后再登记.')
    return 0


def suggest_keys(namespace, english):
    resources = Resources()
    matches = [(key, value) for key, (value, _) in resources.en(namespace).items()
               if value.casefold() == english.casefold()]
    if not matches:
        print(f'{namespace}: 无 en_us 值等于 "{english}" 的键 (需本地模组 JAR 或 KubeJS 英文源)')
        return 1
    zh = resources.zh(namespace)
    for key, value in sorted(matches):
        current = zh.get(key, ('(无中文)', ''))
        print(f'{key}\t{value}\t{current[0]}\t{current[1]}')
    return 0


def export(fmt, output):
    columns = ['id', 'en', 'zh', 'status', 'category', 'namespaces', 'quest_chapters', 'keys', 'avoid', 'allow', 'note', 'source']
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter='\t' if fmt == 'tsv' else ',', lineterminator='\n')
    writer.writerow(columns)
    for entry in load_glossary()['entries']:
        writer.writerow([' | '.join(v) if isinstance(v, list) else ('' if v is None else v)
                         for v in (entry.get(column) for column in columns)])
    if output:
        Path(output).write_text(buffer.getvalue(), encoding='utf-8')
        print(f'wrote {output}')
    else:
        sys.stdout.write(buffer.getvalue())
    return 0


def stats():
    entries = load_glossary()['entries']
    by_namespace = collections.Counter(n for e in entries for n in e['namespaces'])
    print(f'{len(entries)} entries, {sum(e["status"] == "approved" for e in entries)} approved, '
          f'{sum(bool(e.get("keys")) for e in entries)} key-bound, {sum(bool(e.get("avoid")) for e in entries)} with avoid lists')
    for namespace, count in by_namespace.most_common():
        print(f'  {namespace}\t{count}')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('lookup')
    p.add_argument('query')
    p.add_argument('--legacy', action='store_true', help='also search historical term lists')
    p = sub.add_parser('check')
    p.add_argument('--strict', action='store_true', help='treat warnings as failures')
    p = sub.add_parser('suggest-keys')
    p.add_argument('namespace')
    p.add_argument('english')
    p = sub.add_parser('export')
    p.add_argument('--format', choices=['tsv', 'csv'], default='tsv')
    p.add_argument('--output')
    sub.add_parser('stats')
    args = parser.parse_args(argv)
    if args.command == 'lookup':
        return lookup(args.query, args.legacy)
    if args.command == 'check':
        return check(args.strict)
    if args.command == 'suggest-keys':
        return suggest_keys(args.namespace, args.english)
    if args.command == 'export':
        return export(args.format, args.output)
    return stats()


if __name__ == '__main__':
    sys.exit(main())
