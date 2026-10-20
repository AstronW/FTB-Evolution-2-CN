"""Extract, build and validate the remaining 1.4.0 GuideME/MDX manual pages.

Scope comes from ``localization/reports/remaining-1.4.0-manuals.json`` and is
limited to player-facing Markdown/MDX pages that were still uncovered after the
first manual batch.  Translations are maintained as whole pages under
``localization/manuals_extra/translations``; the builder never edits the mod
JARs and only writes the two explicit output roots below.
"""
from __future__ import annotations
from protected_text import signature

import collections
import hashlib
import posixpath
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / 'localization/manuals_extra'
PACK = ROOT / '.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN'
DATAPACK = ROOT / '.minecraft/datapacks/ftb_evolution_cn'
REPORT = ROOT / 'localization/reports/remaining-1.4.0-manuals.json'
MANIFEST = BASE / 'source_manifest.json'
SOURCES = BASE / 'sources'
TRANSLATIONS = BASE / 'translations'
PROGRESS = BASE / 'progress.json'

CJK = re.compile(r'[\u3400-\u9fff]')
PUNCT = re.compile(r'[\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\u2026\u2014\u2013]')
TAG = re.compile(r'<[^>]+>')
LINK = re.compile(r'\]\(([^)]*)\)')
IMAGE = re.compile(r'!\[[^\]]*\]\(([^)]*)\)')
CODE = re.compile(r'`[^`\n]+`')
NUMBER = re.compile(r'(?<![A-Za-z_])\d+(?:[,.]\d+)*(?:%)?')
MACRO = re.compile(r'\$\([^)]*\)')
STELLAR = re.compile(r'\[/?(?:ref|item|block|entity|recipe|tag)=?[^\]]*\]')
PLACEHOLDER = re.compile(r'%(?:\d+\$)?[sdf]|\{\d+\}')
HEADING = re.compile(r'^(#{1,6})\s+(.*)$')
LIST = re.compile(r'^(\s*)([-*+]|\d+\.)\s+')
TABLE = re.compile(r'^\s*\|')
QUOTE = re.compile(r'^\s*(>+)\s?')
FENCE = re.compile(r'^\s*(```+|~~~+)')


def digest(text: str) -> str:
    return hashlib.sha256(text.replace('\r\n', '\n').replace('\r', '\n').encode()).hexdigest()


def normalize(text: str) -> str:
    return text.replace('\r\n', '\n').replace('\r', '\n')


def guide_roots(paths: dict[str, dict]) -> dict[str, str]:
    """Map a GuideME page prefix to its content root.

    GuideME inserts the language directory directly below the guide's content
    root.  The root is the shortest ancestor that owns an ``index.md``; this
    distinguishes ``.../power`` from ``.../colossal_reactors/guide``.
    """
    index_dirs = {str(pathlib.PurePosixPath(path).parent) for path in paths if path.endswith('/index.md')}
    roots = {}
    for path in paths:
        if not (path.startswith('assets/') and '/guides/' in path):
            continue
        parts = path.split('/')
        ns = parts[1]
        # Some guides have their index page already translated by an earlier
        # batch, so the remaining subset cannot always see index.md.  The
        # conventional layouts are still unambiguous:
        #   assets/<ns>/guides/<ns>/guide/...  -> root .../<ns>/guide
        #   assets/<ns>/guides/<ns>/<book>/... -> root .../<ns>/<book>
        if parts[3] == ns:
            root = '/'.join(parts[:5]) if len(parts) > 5 and parts[4] == 'guide' else '/'.join(parts[:4])
        else:
            root = '/'.join(parts[:4])
        roots[path] = root
    return roots


def target_for(path: str, roots: dict[str, str] | None = None) -> str:
    if path.startswith('assets/') and '/guides/' in path:
        root = (roots or {}).get(path)
        if root is None:
            # Fallback for a direct call: the guide root is the directory
            # containing index.md, which is not knowable from this path alone.
            raise ValueError(f'No GuideME content root for: {path}')
        rel = pathlib.PurePosixPath(path).relative_to(root).as_posix()
        return f'{root}/_zh_cn/{rel}'
    if path.startswith('assets/') and '/ae2guide/' in path:
        prefix, rel = path.split('/ae2guide/', 1)
        return f'{prefix}/ae2guide/_zh_cn/{rel}'
    if path.startswith('assets/oracle_index/books/'):
        parts = path.split('/')
        book = parts[3]
        rel = '/'.join(parts[4:])
        return f'assets/oracle_index/books/{book}/translated/zh_cn/{rel}'
    if path.startswith('assets/auroral/auroral/'):
        return path.replace('assets/auroral/auroral/', 'assets/auroral/auroral/_zh_cn/', 1)
    if path.startswith('data/stellaris/wiki/infos/'):
        return 'datapacks/ftb_evolution_cn/' + path
    raise ValueError(f'Unmapped manual path: {path}')


def output_path(target: str) -> pathlib.Path:
    return (DATAPACK if target.startswith('datapacks/') else PACK) / target.removeprefix('datapacks/ftb_evolution_cn/')


def source_text(entry: dict) -> str:
    source = pathlib.Path(entry['source'])
    if source.is_file() and source.suffix == '.jar':
        with zipfile.ZipFile(source) as archive:
            return normalize(archive.read(entry['path']).decode('utf-8-sig'))
    candidates = [
        ROOT / '.minecraft/kubejs' / entry['path'].removeprefix('assets/'),
        ROOT / '.minecraft/kubejs' / entry['path'].removeprefix('data/'),
    ]
    for path in candidates:
        if path.is_file():
            return normalize(path.read_text())
    if source.is_file():
        return normalize(source.read_text())
    raise FileNotFoundError(entry['source'])


def word_count(text: str) -> int:
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    text = re.sub(r'<[^>]*>|\$\([^)]*\)|\]\([^)]*\)|[a-z_]+:[a-z0-9_./-]+', ' ', text)
    return len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", text))


def known_pages() -> set[str]:
    """All Markdown/MDX pages shipped by the current top-level mods.

    Used only to resolve local links; it does not extend the translation scope.
    """
    pages = set()
    for jar in sorted((ROOT / '.minecraft/mods').glob('*.jar')):
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    if name.endswith(('.md', '.mdx')) and name.startswith(('assets/', 'data/')):
                        pages.add(name)
        except Exception:
            continue
    for kind in ('assets', 'data'):
        for path in (ROOT / '.minecraft/kubejs' / kind).rglob('*'):
            if path.is_file() and path.suffix in {'.md', '.mdx'}:
                pages.add(f'{kind}/{path.relative_to(ROOT / ".minecraft/kubejs" / kind).as_posix()}')
    return pages


def extract() -> None:
    report = json.loads(REPORT.read_text())
    units = [
        unit for unit in report['units']
        if unit['format'] == 'Markdown/MDX' and not unit['covered_candidate']
    ]
    documents = {}
    roots = guide_roots({unit['path']: unit for unit in units})
    for unit in units:
        path = unit['path']
        entry = {
            'path': path,
            'source': unit['source'],
            'format': path.rsplit('.', 1)[-1],
            'group': unit['group'],
            'target': target_for(path, roots),
            'english_words_approx': unit['english_words_approx'],
        }
        text = source_text(entry)
        entry['source_sha256'] = digest(text)
        documents[path] = entry
        snapshot = SOURCES / path
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_text(text)
    manifest = {
        'target_pack_version': '1.4.0',
        'generated_from': str(REPORT.relative_to(ROOT)),
        'known_pages': sorted(known_pages()),
        'documents': dict(sorted(documents.items())),
    }
    BASE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(documents)} source pages extracted from the 1.4.0 remaining report')


def load_manifest() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    for path, entry in manifest['documents'].items():
        current = digest(source_text(entry))
        assert current == entry['source_sha256'], f'Source changed: {path}'
    return manifest


def frontmatter(text: str) -> tuple[list[str], list[str]]:
    lines = normalize(text).splitlines()
    if not lines or lines[0].strip() != '---':
        return [], lines
    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            return lines[1:index], lines[index + 1:]
    raise ValueError('unclosed frontmatter')


def frontmatter_key(line: str) -> tuple[int, str] | None:
    match = re.match(r'^(\s*)([A-Za-z0-9_-]+)\s*:(.*)$', line)
    if not match:
        return None
    return len(match[1]), match[2]


def check_frontmatter(source: str, translated: str, errors: list[str], key: str) -> None:
    source_lines, _ = frontmatter(source)
    target_lines, _ = frontmatter(translated)
    if bool(source_lines) != bool(target_lines):
        errors.append(f'{key}: frontmatter presence differs')
        return
    if len(source_lines) != len(target_lines):
        errors.append(f'{key}: frontmatter line count differs')
        return
    for index, (left, right) in enumerate(zip(source_lines, target_lines)):
        left_key = frontmatter_key(left)
        right_key = frontmatter_key(right)
        if left_key != right_key:
            errors.append(f'{key}: frontmatter key/indent differs at line {index + 1}')
            continue
        if left_key is None:
            if left != right:
                errors.append(f'{key}: frontmatter raw line differs at line {index + 1}')
            continue
        name = left_key[1]
        display = name in {'title', 'description', 'subtitle', 'tooltip', 'landing_text'}
        if not display and left != right:
            errors.append(f'{key}: non-display frontmatter changed ({name})')
        if display and not CJK.search(right):
            # A page title may intentionally keep a mod name, but an empty value
            # or unchanged English display field needs review.
            if right.strip() == left.strip():
                errors.append(f'{key}: display frontmatter left unchanged ({name})')


def code_blocks(text: str) -> list[str]:
    blocks = []
    current = []
    active = False
    for line in normalize(text).splitlines():
        if FENCE.match(line):
            if active:
                current.append(line)
                blocks.append('\n'.join(current))
                current = []
                active = False
            else:
                active = True
                current = [line]
        elif active:
            current.append(line)
    if active:
        blocks.append('\n'.join(current))
    return blocks


def table_blocks(text: str) -> list[list[str]]:
    blocks = []
    current: list[str] = []
    for line in normalize(text).splitlines():
        if TABLE.match(line):
            current.append(line)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def structure(text: str) -> dict:
    lines = normalize(text).splitlines()
    front, body = frontmatter(text)
    body_text = '\n'.join(body)
    return {
        'syntax': signature(body_text),
        'headings': [(len(level), text_value) for level, text_value in
                     (match.groups() for match in (HEADING.match(line) for line in body) if match)],
        'lists': [(len(indent), marker) for indent, marker in
                  (match.groups() for match in (LIST.match(line) for line in body) if match)],
        'tables': [[line.count('|') for line in block] for block in table_blocks(body_text)],
        'quotes': [len(match.group(1)) for match in (QUOTE.match(line) for line in body) if match],
        'tags': TAG.findall(body_text),
        'links': LINK.findall(body_text),
        'images': IMAGE.findall(body_text),
        'code': dict(collections.Counter(CODE.findall(body_text))),
        'numbers': dict(collections.Counter(NUMBER.findall(body_text))),
        'macros': dict(collections.Counter(MACRO.findall(body_text))),
        'stellar': dict(collections.Counter(STELLAR.findall(body_text))),
        'placeholders': dict(collections.Counter(PLACEHOLDER.findall(body_text))),
        'code_blocks': code_blocks(body_text),
    }


def check_page(path: str, entry: dict, source: str, translated: str, manifest: dict) -> list[str]:
    errors: list[str] = []
    if not translated.strip():
        return [f'{path}: empty translation']
    prose = re.sub(r'```.*?```', '', translated, flags=re.S)
    prose = re.sub(r'`[^`\n]*`', '', prose)
    if PUNCT.search(prose):
        errors.append(f'{path}: Chinese punctuation present')
    check_frontmatter(source, translated, errors, path)
    left = structure(source)
    right = structure(translated)
    # Headings keep their level sequence; text is translated.
    if [level for level, _ in left['headings']] != [level for level, _ in right['headings']]:
        errors.append(f'{path}: heading level sequence differs')
    if len(left['headings']) != len(right['headings']):
        errors.append(f'{path}: heading count differs')
    if left['lists'] != right['lists']:
        errors.append(f'{path}: list marker sequence differs')
    if left['tables'] != right['tables']:
        errors.append(f'{path}: table shape differs')
    if left['quotes'] != right['quotes']:
        errors.append(f'{path}: blockquote marker sequence differs')
    def tag_shape(tag: str) -> str:
        return re.sub(r'(fallbackText=")[^"]*(")', r'\1\2', tag)

    if [tag_shape(tag) for tag in left['tags']] != [tag_shape(tag) for tag in right['tags']]:
        errors.append(f'{path}: protected tags differs')
    for tag in right['tags']:
        if 'fallbackText="' in tag and not CJK.search(re.search(r'fallbackText="([^"]*)"', tag).group(1)):
            errors.append(f'{path}: fallbackText not translated')
    for field in ('syntax', 'links', 'images', 'code', 'numbers', 'macros', 'stellar', 'placeholders', 'code_blocks'):
        if left[field] != right[field]:
            errors.append(f'{path}: protected {field} differs')
    # Local manual links must keep resolving to a known source page.
    for link in left['links']:
        target = link.split('#', 1)[0]
        if not target or '://' in target or target.startswith(('/', '#')) or ':' in target:
            # Namespace-qualified links point into another guide/book and are
            # not relative files in this page's directory.
            continue
        if target.endswith(('.md', '.mdx')):
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            known = set(manifest.get('known_pages', [])) | set(manifest['documents'])
            if resolved not in known and not (SOURCES / resolved).exists():
                errors.append(f'{path}: local link target missing from current sources: {target}')
    return errors


def translations() -> dict[str, pathlib.Path]:
    result = {}
    if not TRANSLATIONS.exists():
        return result
    for path in TRANSLATIONS.rglob('*'):
        if path.is_file() and path.suffix in {'.md', '.mdx'}:
            result[path.relative_to(TRANSLATIONS).as_posix()] = path
    return dict(sorted(result.items()))


def main() -> None:
    if len(sys.argv) not in {2, 3} or sys.argv[1] not in {'extract', 'status', 'build', 'check', 'check-page'}:
        raise SystemExit('Usage: python localization/manual_extra_translation.py extract|status|build|check|check-page <page>')
    command = sys.argv[1]
    if command == 'extract':
        extract()
        return
    manifest = load_manifest()
    if command == 'check-page':
        if len(sys.argv) != 3:
            raise SystemExit('check-page requires a source page path')
        path = sys.argv[2]
        if path not in manifest['documents']:
            raise SystemExit(f'Unknown page: {path}')
        entry = manifest['documents'][path]
        zh_path = TRANSLATIONS / path
        if not zh_path.is_file():
            raise SystemExit(f'Missing translation: {path}')
        errors = check_page(path, entry, source_text(entry), normalize(zh_path.read_text()), manifest)
        if errors:
            print('\n'.join(errors))
            raise SystemExit(1)
        print(f'PASS {path}')
        return
    translated = translations()
    rows = []
    errors: list[str] = []
    for path, entry in manifest['documents'].items():
        source = source_text(entry)
        zh_path = translated.get(path)
        complete = zh_path is not None
        if complete:
            zh = normalize(zh_path.read_text())
            errors.extend(check_page(path, entry, source, zh, manifest))
        rows.append({
            'page': path,
            'group': entry['group'],
            'target': entry['target'],
            'words': entry['english_words_approx'],
            'translated': complete,
        })
    progress = {
        'target_pack_version': '1.4.0',
        'pages': len(rows),
        'translated_pages': sum(row['translated'] for row in rows),
        'translated_words': sum(row['words'] for row in rows if row['translated']),
        'total_words': sum(row['words'] for row in rows),
        'errors': errors,
        'rows': rows,
    }
    if errors:
        PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
        print('\n'.join(errors[:40]))
        raise SystemExit(f'{len(errors)} manual validation error(s)')
    if command in {'build', 'check'}:
        for path, zh_path in translated.items():
            if path not in manifest['documents']:
                raise SystemExit(f'Translation without current source: {path}')
            output = output_path(manifest['documents'][path]['target'])
            data = normalize(zh_path.read_text())
            if command == 'build':
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(data)
                if output.is_relative_to(DATAPACK):
                    DATAPACK.mkdir(parents=True, exist_ok=True)
                    meta = DATAPACK / 'pack.mcmeta'
                    if not meta.exists():
                        meta.write_text(json.dumps({
                            'pack': {
                                'description': 'FTB Evolution 2 简体中文数据包',
                                'min_format': [101, 0],
                                'max_format': [101, 2147483647],
                            }
                        }, ensure_ascii=False, indent=2) + '\n')
            else:
                assert output.is_file() and normalize(output.read_text()) == data, f'Output drift: {path}'
    PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    print(f"{progress['translated_pages']}/{progress['pages']} pages translated "
          f"({progress['translated_words']}/{progress['total_words']} words)")


if __name__ == '__main__':
    main()
