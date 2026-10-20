"""Read-only 1.4.0 language-key inventory with cross-version CFPA/PR candidates.

Reports candidate coverage, not linguistic approval or installation. Run after
cfpa-pr-audit/download-index.json is available to include cached PR sources.
"""
from pathlib import Path
import collections, hashlib, io, json, re, zipfile, tomllib
from reviewed_cfpa_overlay import load_verified_review

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / 'localization/reports'
GAME = Path(json.loads((ROOT / 'project.json').read_text())['target_instance'])
CJK = re.compile(r'[\u3400-\u9fff]')
LATIN = re.compile(r'[A-Za-z]')
MANUAL_PREFIXES = ('book.', 'info_book.', 'infobook.', 'gui.guide.', 'guide.betterfishtanks.', 'guide.animusnv.')
ERRORS = []
MOD_IDS = set()


def parse(data, source):
    if isinstance(data, bytes):
        data = data.decode('utf-8-sig', errors='replace')
    try:
        return json.loads(data)
    except ValueError as exc:
        try:
            value = json.loads(data, strict=False)
            ERRORS.append({'source': source, 'recovered_nonstandard_json': str(exc)})
            return value
        except ValueError:
            ERRORS.append({'source': source, 'error': str(exc)})
            return {}


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def scan_instance(mc, collect_documents=False):
    langs = collections.defaultdict(dict)
    origins = {}
    documents = {}
    jars = []

    def ingest(name, data, source):
        m = re.fullmatch(r'assets/([^/]+)/lang/(en_us|zh_cn)\.json', name)
        if m:
            d = parse(data, source + ':' + name)
            if m[2] == 'zh_cn' and not d:
                raw = data.decode('utf-8-sig', errors='replace') if isinstance(data, bytes) else data
                salvaged = {}
                for pair in re.finditer(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"', raw):
                    try:
                        key, value = (json.loads('"' + x + '"', strict=False) for x in pair.groups())
                        salvaged[key] = value
                    except ValueError:
                        pass
                langs['repair_zh'].update(salvaged)
            if isinstance(d, dict):
                langs[m[2]].update({k: v for k, v in d.items() if isinstance(v, str)})
                for k in d:
                    origins[m[2], k] = {'namespace': m[1], 'source': source, 'path': name}
        elif collect_documents and name.startswith(('assets/', 'data/')) and name.endswith(('.json', '.md', '.mdx', '.txt')):
            documents[name] = (data, source)

    def archive(z, source, nested=True):
        names = z.namelist()
        if mc == GAME:
            for metadata in ['META-INF/neoforge.mods.toml', 'META-INF/mods.toml', 'fabric.mod.json']:
                if metadata in names:
                    raw = z.read(metadata).decode('utf-8-sig')
                    meta = json.loads(raw) if metadata.endswith('.json') else tomllib.loads(raw)
                    for mod in meta.get('mods', [meta]):
                        identifier = mod.get('modId', mod.get('id'))
                        if identifier:
                            MOD_IDS.add(identifier)
                    break
        if nested:
            for name in names:
                if name.startswith('META-INF/jars/') and name.endswith('.jar'):
                    try:
                        with zipfile.ZipFile(io.BytesIO(z.read(name))) as child:
                            archive(child, source + '!' + name, False)
                    except (ValueError, zipfile.BadZipFile) as exc:
                        ERRORS.append({'source': source + '!' + name, 'error': str(exc)})
        for name in names:
            if re.fullmatch(r'assets/[^/]+/lang/(en_us|zh_cn)\.json', name) or collect_documents and name.startswith(('assets/', 'data/')) and name.endswith(('.json', '.md', '.mdx', '.txt')):
                ingest(name, z.read(name), source)

    for jar in sorted((mc / 'mods').glob('*.jar')):
        jars.append(jar.name)
        with zipfile.ZipFile(jar) as z:
            archive(z, str(jar))
    for folder in ['kubejs/assets', 'kubejs/data']:
        for p in sorted((mc / folder).rglob('*')):
            if p.is_file() and p.suffix in {'.json', '.md', '.mdx', '.txt'}:
                ingest(folder.split('/')[-1] + '/' + p.relative_to(mc / folder).as_posix(), p.read_bytes(), str(p))
    options = mc / 'options.txt'
    selected = []
    if options.exists():
        line = next((x for x in options.read_text().splitlines() if x.startswith('resourcePacks:')), None)
        if line:
            selected = json.loads(line.split(':', 1)[1])
    for entry in selected:
        if not entry.startswith('file/'):
            continue
        pack = mc / 'resourcepacks' / entry[5:]
        if pack.is_file() and zipfile.is_zipfile(pack):
            with zipfile.ZipFile(pack) as z:
                archive(z, str(pack), False)
        elif pack.is_dir():
            for p in sorted(pack.rglob('*')):
                if p.is_file():
                    ingest(p.relative_to(pack).as_posix(), p.read_bytes(), str(p))
    return langs, origins, documents, jars


def legacy_or_json(path, format_hint=None):
    if path.suffix.lower() == '.lang' or format_hint == 'lang':
        out = {}
        for line in path.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            if '=' in line and not line.lstrip().startswith(('#', '!')):
                k, v = line.split('=', 1)
                out[k.strip()] = v
        return out
    return parse(path.read_bytes(), str(path))


def candidate_files():
    base = ROOT / 'CFPA/projects/assets'
    for p in base.rglob('*'):
        if not p.is_file() or p.parent.name != 'lang' or not re.match(r'zh_cn(?:[-.]|$)', p.name, re.I) or p.suffix not in {'.json', '.lang'}:
            continue
        rel = p.relative_to(base)
        if len(rel.parts) < 5:
            continue
        en = next((x for x in p.parent.iterdir() if x.name.lower() == ('en_us' + p.suffix).lower()), None)
        yield {'zh_path': str(p), 'en_path': str(en) if en else None, 'namespace': rel.parts[2], 'version': rel.parts[1], 'slug': rel.parts[0], 'kind': 'cfpa'}
    index = REPORT / 'cfpa-pr-audit/download-index.json'
    if index.exists():
        data = json.loads(index.read_text())
        for item in data:
            # The PR worker writes the same zh_path/en_path resource schema.
            yield item


def main():
    langs, origins, documents, jars = scan_instance(GAME, True)
    en, official = langs['en_us'], langs['zh_cn']
    oldlangs, _, _, _ = scan_instance(ROOT / '.minecraft')
    olden = oldlangs['en_us']
    project = {}
    for p in sorted((ROOT / '.minecraft/kubejs/assets').glob('*/lang/zh_cn.json')):
        project.update(parse(p.read_bytes(), str(p)))
    for pack in sorted((ROOT / '.minecraft/resourcepacks').iterdir()):
        if pack.is_dir():
            for p in sorted(pack.glob('assets/*/lang/zh_cn.json')):
                project.update(parse(p.read_bytes(), str(p)))
    # Updated quest dependencies have their own immutable 1.4.0 source snapshot.
    for group in json.loads((ROOT / 'localization/quest_extra_labels.json').read_text()):
        for key, value in group['entries'].items():
            olden[key] = value['en']
    reviewed,_=load_verified_review()
    adopted={d['key']:d for d in reviewed if d['status']=='accepted' and d.get('resource_domain','lang')=='lang'}
    rejected={d['key']:d for d in reviewed if d['status']=='rejected' and d.get('resource_domain','lang')=='lang'}
    for key,d in adopted.items():
        project[key]=d['chinese'];olden[key]=d['english']
    reviewed_english = set()
    for folder in (ROOT / 'localization/ordinary').glob('batch-*'):
        manifest = folder / 'manifest.json'
        source = folder / 'source-en_us.json'
        if not (folder / 'verification.json').exists() or not source.exists():
            continue
        meta = json.loads(manifest.read_text())
        unchanged = set(meta.get('unchanged_values', []))
        for key, value in json.loads(source.read_text()).items():
            if value in unchanged and en.get(key) == value:
                reviewed_english.add(key)
    referenced = set()
    for name, (data, source) in documents.items():
        if not name.endswith('.json') or not any(t in name for t in ['/patchouli_books/', '/books/', '/modonomicon/']):
            continue
        if re.search(r'/(?:_?[a-z]{2}_[a-z]{2})/', name) and '/en_us/' not in name:
            continue
        def walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k in {'name', 'description', 'text', 'title', 'subtitle', 'landing_text', 'caption'} and isinstance(v, str) and v in en:
                        referenced.add(v)
                    elif isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
        walk(parse(data, source + ':' + name))
    # Candidate indexes retain source-specific evidence. English matches across keys
    # require the same namespace, so generic words from unrelated mods cannot count.
    by_key = collections.defaultdict(list)
    by_text = collections.defaultdict(list)
    target_texts = {(origins['en_us', k]['namespace'], v) for k, v in en.items() if isinstance(v, str)}
    file_count = collections.Counter()
    for item in candidate_files():
        if not item.get('zh_path'):
            continue
        path = Path(item['zh_path'])
        if not path.exists():
            ERRORS.append({'source': str(path), 'error': 'candidate cache missing'})
            continue
        zh = legacy_or_json(path, item.get('format'))
        ep = Path(item['en_path']) if item.get('en_path') else None
        eng = legacy_or_json(ep, item.get('format')) if ep and ep.exists() else {}
        if not isinstance(zh, dict) or not isinstance(eng, dict):
            continue
        file_count[item['kind']] += 1
        for key, text in zh.items():
            if not isinstance(text, str) or not CJK.search(text):
                continue
            english = eng.get(key)
            record = {**{k:v for k,v in item.items() if k not in {'zh_path','en_path'}}, 'path': str(path.relative_to(ROOT)), 'source_key': key, 'english': english, 'chinese': text}
            if key in en:
                by_key[key].append(record)
            if isinstance(english, str) and (item['namespace'], english) in target_texts:
                by_text[item['namespace'], english].append(record)
    scope = json.loads((ROOT / 'localization/language_scope.json').read_text())
    def excluded(ns):
        return scope['excluded_namespaces'].get(ns) or next((reason for p, reason in scope['excluded_namespace_prefixes'].items() if ns.startswith(p)), '')
    rows = []
    omitted = []
    for key, value in en.items():
        if not isinstance(value, str) or not LATIN.search(value):
            continue
        owner = origins['en_us', key]
        ns = owner['namespace']
        omit_reason = ''
        if key.startswith(('_comment', '__comment')):
            omit_reason = 'language-file metadata/comment key'
        elif ns == 'modonomicon' and re.match(r'(?:book|research_node|research_stage)\.modonomicon\.demo', key):
            omit_reason = 'framework developer demonstration book'
        elif ns == 'collective':
            referenced_mod = key.split('.')[1] if key.startswith('collective.') else None
            if referenced_mod and referenced_mod not in MOD_IDS and referenced_mod != 'shared':
                omit_reason = 'shared library text for a mod not installed in this instance'
            elif key.startswith(('item.', 'block.', 'entity.')) and key.split('.')[1] not in MOD_IDS:
                omit_reason = 'shared library item/entity text for a mod not installed in this instance'
        if key in rejected and rejected[key].get('rejection_kind')=='out_of_scope':
            omit_reason='reviewed out-of-scope: '+rejected[key]['reason']
        if omit_reason:
            omitted.append({'namespace':ns,'key':key,'reason':omit_reason})
            continue
        candidates = by_key.get(key, [])
        exact = [x for x in candidates if x['english'] == value]
        renamed = [x for x in by_text.get((ns, value), []) if x['source_key'] != key]
        if key in adopted and adopted[key]['english']==value:
            state = 'reviewed_cfpa_adopted'
        elif key in rejected and rejected[key]['english']==value:
            state = 'reviewed_candidate_rejected'
        elif CJK.search(official.get(key, '')):
            state = 'official_cjk'
        elif CJK.search(project.get(key, '')) and olden.get(key) == value:
            state = 'project_source_match'
        elif key in reviewed_english:
            state = 'reviewed_english'
        elif CJK.search(langs['repair_zh'].get(key, '')):
            state = 'official_needs_json_repair'
        elif any(x['kind'] == 'cfpa' for x in exact):
            state = 'cfpa_source_match'
        elif any(x['kind'] == 'pr' for x in exact):
            state = 'pr_source_match'
        elif renamed:
            state = 'renamed_key_same_english'
        elif candidates:
            state = 'same_key_needs_review'
        else:
            state = 'no_chinese_candidate'
        covered = state in {'official_cjk', 'project_source_match', 'reviewed_english','reviewed_cfpa_adopted'}
        rows.append({'namespace': ns, 'key': key, 'english': value, 'category': 'manual_keys' if key.startswith(MANUAL_PREFIXES) or key in referenced else 'ordinary', 'excluded': bool(excluded(ns)), 'exclusion_reason': excluded(ns), 'state': state, 'source': owner['source'], 'official_zh': official.get(key), 'repair_candidate':langs['repair_zh'].get(key), 'project_zh': project.get(key), 'project_source_changed': bool(CJK.search(project.get(key, '')) and olden.get(key) != value), 'exact_candidates': exact[:3] if not covered else [], 'renamed_candidates': renamed[:3] if not covered else [], 'review_candidates': [x for x in candidates if x['english'] != value][:3] if not covered else []})
    counts = collections.defaultdict(collections.Counter)
    namespaces = collections.defaultdict(collections.Counter)
    for row in rows:
        group = 'excluded' if row['excluded'] else row['category']
        counts[group][row['state']] += 1
        if not row['excluded']:
            namespaces[row['namespace'] + ' [' + row['category'] + ']'][row['state']] += 1
    summary = {'target_pack': '1.4.0', 'minecraft': '26.1.2', 'game': str(GAME), 'top_level_jars_scanned': len(jars), 'english_keys_global': len(en), 'english_keys_with_latin_text': len(rows), 'cfpa_commit': json.loads((ROOT / 'project.json').read_text())['cfpa']['commit'], 'candidate_files': dict(file_count), 'counts': {k:dict(v) for k,v in counts.items()}, 'scope':scope, 'project_source_changed_keys':sum(x['project_source_changed'] for x in rows if not x['excluded']), 'namespace_counts': {k:dict(v) for k,v in sorted(namespaces.items(), key=lambda p:-p[1]['no_chinese_candidate'])}, 'omitted_non_player_text':omitted, 'parse_errors': ERRORS, 'method': 'Global keys from current target JARs (including embedded META-INF/jars), KubeJS and selected packs. Official CJK is candidate coverage, project overlays count only with matching English source; all CFPA versions and cached PRs compared by exact key+English, then namespace+English for renamed-key candidates. Same-key changed/missing English is review-only. No linguistic approval or runtime visibility claim. Unknown language-key collisions follow scan order, not verified resource-manager order. Manual keys use known prefixes and book JSON references; document-based manuals counted separately. Framework demo books, language metadata and Collective strings for uninstalled mods omitted.'}
    dump(REPORT / 'remaining-1.4.0-language-summary.json', summary)
    dump(REPORT / 'remaining-1.4.0-language-detail.json', rows)
    print(json.dumps({k:summary[k] for k in ['top_level_jars_scanned','english_keys_global','candidate_files','counts','project_source_changed_keys']},ensure_ascii=False,indent=2))
    print('Largest no-candidate namespaces:',list(summary['namespace_counts'].items())[:18])


if __name__ == '__main__':
    main()
