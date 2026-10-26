"""Audit quest/manual/description text against the in-game item names.

Item, block, entity, fluid and effect names that the game actually shows are
the reference.  Wherever an English source segment mentions such a name, the
paired Chinese segment must contain the current Chinese name.  Project quest
and manual prose rank below those names unless a reviewed decision says
otherwise (see `glossary/glossary.json` and `TERMINOLOGY.md`).

  python localization/audit_item_names.py [--json PATH] [--kind quest|patchouli|manual|lang]

Read-only.  Findings covered by `glossary/name-audit-exceptions.json` are
reviewed false positives or deliberate keeps; any other finding fails.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import glossary as g  # noqa: E402

ROOT = g.ROOT
MC = g.MC
NAME_KEY = re.compile(r'^(item|block|entity|fluid_type|fluid|effect)\.([a-z0-9_]+)\.[a-z0-9_/]+$')
FULLWIDTH = str.maketrans('：（），。；！？【】“”', ':(),.;!?[]""')
# Generic labels (Altar, Spirit, Blocks...) would match ordinary prose, so only
# multi-word names are required verbatim; a name with many variants is a family.
MAX_VARIANTS = 2
FORMAT = re.compile(r'§[0-9a-fk-or]|&[0-9a-fk-or]|\$\([^)]*\)|</?[A-Za-z][^>]*>|\[(?:ref|item)=[^\]]*\]|\[ref\]|\\n|\s+')
QUEST_EN = MC / 'config/ftbquests/quests/lang/en_us'
QUEST_ZH = MC / 'config/ftbquests/quests/lang/zh_cn'
QUEST_DATA = MC / 'config/ftbquests/quests/chapters'
EXCEPTIONS = ROOT / 'localization/glossary/name-audit-exceptions.json'
MANUAL_PAIRS = [
    (ROOT / 'localization/manuals/sources', ROOT / 'localization/manuals/translations'),
    (ROOT / 'localization/manuals_extra/sources', ROOT / 'localization/manuals_extra/translations'),
]
PATTERNS = {}


def plain(text):
    return FORMAT.sub('', text).translate(FULLWIDTH)


def pattern(name):
    if name not in PATTERNS:
        PATTERNS[name] = re.compile(r'(?<![A-Za-z])' + re.escape(name) + r'(?:s|es)?(?![A-Za-z])')
    return PATTERNS[name]


class Names:
    def __init__(self):
        self.resources = g.Resources()
        self.cache = {}

    def namespaces(self):
        found = {path.parent.parent.name for root in g.LANG_OUTPUTS for path in root.glob('*/lang/en_us.json')}
        found |= {path.parent.parent.name for path in (MC / 'kubejs/assets').glob('*/lang/en_us.json')}
        found |= {namespace for namespace, language in self.resources._jar_index() if language == 'en_us'}
        return found

    def table(self, namespace):
        """{English name: {Chinese names}} for one namespace's name keys."""
        if namespace not in self.cache:
            english = self.resources.en(namespace)
            chinese = self.resources.zh(namespace)
            table = collections.defaultdict(set)
            for key, (value, _) in english.items():
                match = NAME_KEY.match(key)
                if not match or match[2] != namespace or key not in chinese:
                    continue
                zh = chinese[key][0]
                if not isinstance(value, str) or '%' in value or not re.search('[㐀-鿿]', zh):
                    continue
                if ' ' not in value.strip():
                    continue
                table[value].add(plain(zh))
            self.cache[namespace] = {k: v for k, v in table.items() if len(v) <= MAX_VARIANTS}
        return self.cache[namespace]

    def merged(self, namespaces):
        key = frozenset(namespaces)
        if key not in self.cache:
            table = collections.defaultdict(set)
            for namespace in namespaces:
                for english, chinese in self.table(namespace).items():
                    table[english] |= chinese
            self.cache[key] = (dict(table), sorted(table, key=len, reverse=True))
        return self.cache[key]


def missing_names(merged, english, chinese):
    """English names present in `english` whose current Chinese name is absent from `chinese`."""
    table, order = merged
    text = re.sub(r'§[0-9a-fk-or]|&[0-9a-fk-or]|\$\([^)]*\)', '', english)
    target = plain(chinese)
    found = []
    for name in order:
        if name not in text or not pattern(name).search(text):
            continue
        text = pattern(name).sub('\0', text)
        expected = table[name]
        if not any(zh in target for zh in expected):
            found.append((name, sorted(expected)))
    return found


def quest_pairs():
    from quest_translation import load_source
    for zh_path in sorted((QUEST_ZH / 'chapters').glob('*.json5')):
        en_path = QUEST_EN / 'chapters' / zh_path.name
        data = QUEST_DATA / zh_path.name
        namespaces = set(re.findall(r'"([a-z0-9_]+):[a-z0-9_/]+"', data.read_text(encoding='utf-8'))) if data.exists() else set()
        english, chinese = (load_source(path) for path in (en_path, zh_path))
        for key, value in chinese.items():
            source = english.get(key)
            if source is None:
                continue
            join = lambda v: '\n'.join(v) if isinstance(v, list) else v
            yield 'quest', f'{zh_path.relative_to(ROOT)}:{key}', namespaces, join(source), join(value)


def patchouli_pairs():
    import patchouli_translation as p
    for namespace, books in p.BOOKS.items():
        for book, source, _ in books:
            lang_keys = p.book_lang(namespace, source)
            for rel, text, _ in p.book_files(namespace, book, source):
                tsv = p.BASE / 'translations' / namespace / book / (rel + '.tsv')
                if not tsv.exists():
                    continue
                zh = dict(line.split('\t', 1) for line in tsv.read_text(encoding='utf-8').splitlines() if '\t' in line)
                for path, value in p.segments(text, lang_keys):
                    if path in zh:
                        yield 'patchouli', f'{tsv.relative_to(ROOT)}:{path}', {namespace}, value, zh[path].replace('\\n', '\n')


def manual_pairs():
    for sources, translations in MANUAL_PAIRS:
        for target in sorted(translations.rglob('*')):
            if not target.is_file() or target.suffix not in {'.md', '.mdx', '.json'}:
                continue
            source = sources / target.relative_to(translations)
            if not source.exists():
                continue
            parts = target.relative_to(translations).parts
            namespace = parts[1] if parts[0] in {'assets', 'data'} else parts[0]
            yield 'manual', str(target.relative_to(ROOT)), {namespace}, source.read_text(encoding='utf-8'), target.read_text(encoding='utf-8')


def lang_pairs(names):
    """Descriptions, tooltips and language-key manuals maintained by the project."""
    for root in g.LANG_OUTPUTS:
        for path in sorted(root.glob('*/lang/zh_cn.json')):
            namespace = path.parent.parent.name
            english = names.resources.en(namespace)
            for key, value in json.loads(path.read_text(encoding='utf-8')).items():
                if NAME_KEY.match(key) or key.endswith('.latin') or key not in english or not isinstance(value, str):
                    continue
                yield 'lang', f'{path.relative_to(ROOT)}:{key}', {namespace}, english[key][0], value


def audit(kinds):
    names = Names()
    known = names.namespaces()
    findings = []
    sources = {'quest': quest_pairs, 'patchouli': patchouli_pairs, 'manual': manual_pairs,
               'lang': lambda: lang_pairs(names)}
    for kind in kinds:
        for kind_, location, namespaces, english, chinese in sources[kind]():
            namespaces = {n for n in namespaces if n in known}
            # Quest chapters span many mods; they use the names of the mods they reference.
            table = names.merged(namespaces)
            for name, expected in missing_names(table, english, chinese):
                findings.append({'kind': kind_, 'location': location, 'english_name': name,
                                 'expected_zh': expected, 'zh': plain(chinese)[:200]})
    return findings


def excepted(finding, exceptions):
    for index, rule in enumerate(exceptions):
        if rule['english_name'] == finding['english_name'] and rule.get('location', '') in finding['location']:
            return index
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--json')
    parser.add_argument('--kind', action='append', choices=['quest', 'patchouli', 'manual', 'lang'])
    args = parser.parse_args(argv)
    findings = audit(args.kind or ['quest', 'patchouli', 'manual', 'lang'])
    exceptions = json.loads(EXCEPTIONS.read_text(encoding='utf-8'))['exceptions']
    assert all(rule.get('reason') for rule in exceptions), 'Every exception needs a reason'
    used = set()
    open_findings = []
    for finding in findings:
        index = excepted(finding, exceptions)
        if index is None:
            open_findings.append(finding)
        else:
            used.add(index)
    counts = collections.Counter((f['kind'], f['english_name'], tuple(f['expected_zh'])) for f in open_findings)
    for (kind, name, expected), count in counts.most_common():
        sample = next(f['location'] for f in open_findings if f['english_name'] == name and f['kind'] == kind)
        print(f'FAIL {kind}\t{count}\t{name}\t{" / ".join(expected)}\t{sample}')
    if not args.kind:
        for index, rule in enumerate(exceptions):
            if index not in used:
                print(f'WARN exception no longer reproduces: {rule["english_name"]} {rule.get("location", "")}')
    print(f'{"FAILED" if open_findings else "PASSED"}: {len(open_findings)} open findings, '
          f'{len(findings) - len(open_findings)} reviewed exceptions')
    if args.json:
        Path(args.json).write_text(json.dumps(open_findings, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return 1 if open_findings else 0


if __name__ == '__main__':
    sys.exit(main())
