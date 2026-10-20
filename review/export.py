"""Export English/Chinese text pairs for the review web app.

Read-only: scans mod JARs (including jar-in-jar), the target instance's KubeJS
assets, quest language files and the built release bundle, then writes
per-mod JSON under review/app/static/data/. Never writes to the game instance.

Layer order (lowest priority first) mirrors the game:
  mod JARs  <  instance kubejs/assets  <  release resource pack / datapack
"""
from pathlib import Path, PurePosixPath
import collections, difflib, hashlib, io, json, re, sys, zipfile

ROOT = Path(__file__).resolve().parent.parent
PROJECT = json.loads((ROOT / 'project.json').read_text())
INSTANCE = Path(PROJECT['target_instance'])
MODS = ROOT / '.minecraft/mods'
BUNDLE = ROOT / 'dist/FTB-Evolution-2-1.4.0-zh_CN-install.zip'
CUSTOM = ROOT / 'localization/custom/batches'
OUT = ROOT / 'review/app/static/data'

EXCLUDED = set(json.loads((ROOT / 'localization/language_scope.json').read_text())['excluded_namespaces'])
MOD_NAMES = json.loads((ROOT / 'localization/client_fixes/mod-names.json').read_text())

LANG_RE = re.compile(r'^assets/([^/]+)/([^/]+)/(en_us|zh_cn)\.json$')
PATCHOULI_RE = re.compile(r'^(assets/[^/]+/patchouli_books/[^/]+)/(en_us|zh_cn)/(.+\.json)$')
GUIDE_ZH_RE = re.compile(r'^(.*)/_zh_cn/(.+\.mdx?)$')
ORACLE_ZH_RE = re.compile(r'^(assets/[^/]+/books/[^/]+)/translated/zh_cn/(.+)$')
SKIP_DOC = re.compile(r'(^|/)(readme|license|licence|changelog|credits)[^/]*\.mdx?$', re.I)
OTHER_LANG_DIR = re.compile(r'/(_[a-z]{2}_[a-z]{2}|translated|[a-z]{2}_[a-z]{2})/')
LANG_KEY_RE = re.compile(r'^[a-z0-9_]+(\.[a-z0-9_:/-]+)+$')
PATCHOULI_VISIBLE = {'name', 'text', 'title', 'description', 'subtitle', 'landing_text',
                     'link_text', 'header', 'book_desc', 'entry_name', 'category_name'}


def interesting(path):
    if LANG_RE.match(path) or PATCHOULI_RE.match(path):
        return True
    if path.startswith('assets/') and path.endswith(('.md', '.mdx')):
        return not SKIP_DOC.search(path)
    if ORACLE_ZH_RE.match(path) or (path.startswith('assets/') and '/books/' in path and path.endswith('_meta.json')):
        return True
    return path.startswith('data/') and '/wiki/' in path and path.endswith('.md')


def mods_toml(text):
    mods = []
    for block in re.split(r'^\s*\[\[mods\]\].*$', text, flags=re.M)[1:]:
        mid = re.search(r'^\s*modId\s*=\s*"([^"]+)"', block, re.M)
        name = re.search(r'^\s*displayName\s*=\s*"([^"]+)"', block, re.M)
        if mid:
            mods.append((mid.group(1), name.group(1) if name else mid.group(1)))
    return mods


class Layer:
    def __init__(self, name):
        self.name = name
        self.files = {}   # path -> text
        self.owner = {}   # path -> jar label

    def add(self, path, data, owner=None):
        try:
            self.files[path] = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            return
        if owner:
            self.owner[path] = owner


JAR_MODS = {}        # jar label -> [(modId, displayName)]
MODID_JAR = {}       # modId -> jar label
NS_OWNER = {}        # namespace -> jar label (first JAR shipping that namespace)


def scan_jar(layer, label, zf):
    names = zf.namelist()
    if 'META-INF/neoforge.mods.toml' in names:
        JAR_MODS[label] = mods_toml(zf.read('META-INF/neoforge.mods.toml').decode('utf-8', 'replace'))
        for mid, _ in JAR_MODS[label]:
            MODID_JAR.setdefault(mid, label)
    for n in names:
        if n.startswith('assets/') and n.count('/') >= 2:
            NS_OWNER.setdefault(n.split('/')[1], label)
        if interesting(n):
            layer.add(n, zf.read(n), label)
        elif n.startswith('META-INF/jarjar/') and n.endswith('.jar'):
            try:
                scan_jar(layer, PurePosixPath(n).name, zipfile.ZipFile(io.BytesIO(zf.read(n))))
            except zipfile.BadZipFile:
                pass


def load_layers():
    jars = Layer('jar')
    for jar in sorted(MODS.glob('*.jar')):
        try:
            scan_jar(jars, jar.name, zipfile.ZipFile(jar))
        except zipfile.BadZipFile:
            print('skip bad jar', jar.name, file=sys.stderr)
    kube = Layer('kubejs')
    base = INSTANCE / 'kubejs/assets'
    for p in base.rglob('*'):
        rel = 'assets/' + p.relative_to(base).as_posix()
        if p.is_file() and interesting(rel):
            kube.add(rel, p.read_bytes())
    pack = Layer('pack')
    bundle = zipfile.ZipFile(BUNDLE)
    for n in bundle.namelist():
        if n.startswith('datapacks/ftb_evolution_cn/data/'):
            rel = n[len('datapacks/ftb_evolution_cn/'):]
        else:
            rel = n
        if interesting(rel):
            pack.add(rel, bundle.read(n))
    return [jars, kube, pack], bundle


def h(en, zh):
    return hashlib.sha1(f'{en}\0{zh}'.encode()).hexdigest()[:12]


def entry(eid, label, en, zh, origin, en_origin=None, upstream=None, kind='lang', excluded=False, path=None):
    e = {'id': eid, 'k': label, 'en': en, 'zh': zh, 'o': origin, 'h': h(en, zh or '')}
    if en_origin and en_origin != 'jar':
        e['eo'] = en_origin
    if upstream is not None and upstream != zh:
        e['up'] = upstream
    if excluded:
        e['ex'] = 1
    if path:
        e['p'] = path
    e['t'] = kind
    return e


def parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # tolerate trailing commas / comments occasionally found in mod assets
        text = re.sub(r'^\s*//.*$', '', text, flags=re.M)
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None


def flatten(value, prefix=''):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from flatten(v, f'{prefix}.{k}' if prefix else k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from flatten(v, f'{prefix}[{i}]')
    elif isinstance(value, str):
        yield prefix, value


def text_value(v):
    return '\n'.join(v) if isinstance(v, list) else (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))


# ---------------------------------------------------------------------------

class Groups:
    def __init__(self):
        self.mods = {}    # gid -> {meta, sections: {sid: {title, kind, entries}}}

    def section(self, gid, sid, title, kind):
        g = self.mods.setdefault(gid, {'sections': {}})
        return g['sections'].setdefault(sid, {'id': sid, 'title': title, 'kind': kind, 'entries': []})['entries']


def group_for_namespace(ns):
    if ns in MODID_JAR:
        return 'mod:' + ns
    jar = NS_OWNER.get(ns)
    if jar:
        for mid, _ in JAR_MODS.get(jar, []):
            if mid == ns:
                return 'mod:' + ns
        mods = JAR_MODS.get(jar)
        if mods:
            return 'mod:' + mods[0][0]
        return 'jar:' + jar
    return 'mod:' + ns


def collect_lang(layers, groups):
    en, zh = collections.defaultdict(dict), collections.defaultdict(dict)
    upstream = collections.defaultdict(dict)
    for layer in layers:
        for path, text in sorted(layer.files.items()):
            m = LANG_RE.match(path)
            if not m:
                continue
            ns, folder, code = m.groups()
            data = parse_json(text)
            if not isinstance(data, dict):
                continue
            target = en if code == 'en_us' else zh
            for k, v in data.items():
                if not isinstance(v, str):
                    v = text_value(v)
                target[(ns, folder)][k] = (v, layer.name)
                if code == 'zh_cn' and layer.name != 'pack':
                    upstream[(ns, folder)][k] = v
    for (ns, folder), keys in sorted(en.items()):
        gid = group_for_namespace(ns)
        title = f'{ns} 语言文件' if folder == 'lang' else f'{ns}/{folder}'
        sec = groups.section(gid, f'lang:{ns}:{folder}', title, 'lang')
        zmap, umap = zh.get((ns, folder), {}), upstream.get((ns, folder), {})
        for k, (ev, eo) in keys.items():
            if not re.search('[A-Za-z]', ev):
                continue
            zv, zo = zmap.get(k, (None, None))
            origin = {'pack': 'project', 'kubejs': 'pack', 'jar': 'mod'}.get(zo, 'missing')
            sec.append(entry(f'lang:{ns}:{folder}:{k}', k, ev, zv, origin, eo,
                             umap.get(k) if zo == 'pack' else None, 'lang', ns in EXCLUDED))


def doc_pairs(layers):
    """Map English doc path -> zh path and layered contents."""
    merged = {}
    for layer in layers:
        for path, text in layer.files.items():
            if LANG_RE.match(path):
                continue
            merged.setdefault(path, {})[layer.name] = text
    en_docs, zh_of = {}, {}
    for path in merged:
        m = PATCHOULI_RE.match(path)
        if m:
            if m.group(2) == 'en_us':
                en_docs[path] = 'patchouli'
            else:
                zh_of[f'{m.group(1)}/en_us/{m.group(3)}'] = path
            continue
        m = ORACLE_ZH_RE.match(path)
        if m:
            zh_of[f'{m.group(1)}/{m.group(2)}'] = path
            continue
        m = GUIDE_ZH_RE.match(path)
        if m:
            zh_of[f'{m.group(1)}/{m.group(2)}'] = path
            continue
        if path.startswith('data/'):
            en_docs[path] = 'datawiki'
            if 'pack' in merged[path]:
                zh_of[path] = path
            continue
        if OTHER_LANG_DIR.search(path):
            continue
        en_docs[path] = 'json' if path.endswith('.json') else 'md'
    return merged, en_docs, zh_of


def book_of(path, kind):
    parts = path.split('/')
    if kind == 'patchouli':
        return '/'.join(parts[2:4]), 'Patchouli: ' + parts[3]
    if kind == 'datawiki':
        return '/'.join(parts[:3]), f'{parts[1]} wiki'
    if '/books/' in path:
        return '/'.join(parts[2:4]), 'Oracle Index: ' + parts[3]
    if len(parts) > 3 and parts[2] == 'guides':
        return '/'.join(parts[2:4]), 'GuideME: ' + parts[3]
    return parts[2], 'GuideME: ' + parts[2]


def pick(layered, prefer_pack=True):
    for name in (('pack', 'kubejs', 'jar') if prefer_pack else ('kubejs', 'jar')):
        if name in layered:
            return layered[name], name
    return None, None


def collect_docs(layers, groups):
    merged, en_docs, zh_of = doc_pairs(layers)
    for path, kind in sorted(en_docs.items()):
        ns = path.split('/')[1]
        gid = group_for_namespace(ns)
        bid, btitle = book_of(path, kind)
        if kind == 'datawiki':
            en_text, eo = pick(merged[path], prefer_pack=False)
            zh_text, zo = (merged[path].get('pack'), 'pack') if 'pack' in merged[path] else (None, None)
        else:
            en_text, eo = pick(merged[path])
            zpath = zh_of.get(path)
            zh_text, zo = pick(merged[zpath]) if zpath else (None, None)
        if en_text is None:
            continue
        origin = {'pack': 'project', 'kubejs': 'pack', 'jar': 'mod'}.get(zo, 'missing')
        rel = path.split('/', 3)[-1] if kind != 'datawiki' else path
        sec = groups.section(gid, f'doc:{bid}', btitle, 'manual')
        if kind in ('patchouli', 'json'):
            en_json, zh_json = parse_json(en_text), parse_json(zh_text) if zh_text else None
            if en_json is None:
                continue
            zflat = dict(flatten(zh_json)) if zh_json is not None else {}
            for jp, ev in flatten(en_json):
                leaf = re.sub(r'\[\d+\]', '', jp.rsplit('.', 1)[-1])
                zv = zflat.get(jp)
                if kind == 'patchouli' and leaf not in PATCHOULI_VISIBLE and (zv is None or zv == ev):
                    continue
                if not re.search('[A-Za-z]', ev) or LANG_KEY_RE.match(ev):
                    continue
                sec.append(entry(f'doc:{path}#{jp}', f'{rel} › {jp}', ev, zv,
                                 origin if zv is not None else 'missing', eo, None, 'manual', ns in EXCLUDED))
        else:
            sec.append(entry(f'doc:{path}', rel, en_text, zh_text, origin, eo, None, 'page', ns in EXCLUDED))


def load_json5(text):
    out, quoted, escaped = [], False, False
    for i, c in enumerate(text):
        if quoted:
            out.append(c)
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
        else:
            if c == '"':
                quoted = True
            if c == ',' and text[i + 1:].lstrip().startswith(('}', ']')):
                continue
            out.append(c)
    return json.loads(''.join(out))


def collect_quests(bundle, groups):
    en_dir = INSTANCE / 'config/ftbquests/quests/lang/en_us'
    prefix = 'config/ftbquests/quests/lang/zh_cn/'
    zh_members = {n[len(prefix):]: n for n in bundle.namelist() if n.startswith(prefix)}
    for p in sorted(en_dir.rglob('*.json5')):
        rel = p.relative_to(en_dir).as_posix()
        en = load_json5(p.read_text(encoding='utf-8-sig'))
        zh_path = INSTANCE / 'config/ftbquests/quests/lang/zh_cn' / rel
        if rel in zh_members:
            zh, origin = load_json5(bundle.read(zh_members[rel]).decode('utf-8-sig')), 'project'
        elif zh_path.exists():
            zh, origin = load_json5(zh_path.read_text(encoding='utf-8-sig')), 'pack'
        else:
            zh, origin = {}, 'missing'
        title = rel.removeprefix('chapters/').removesuffix('.json5')
        sec = groups.section('quests', f'quest:{rel}', title, 'quest')
        for k, v in en.items():
            ev = text_value(v)
            if not re.search('[A-Za-z]', ev):
                continue
            zv = text_value(zh[k]) if k in zh else None
            sec.append(entry(f'quest:{rel}:{k}', k, ev, zv, origin if zv is not None else 'missing',
                             None, None, 'quest'))


def collect_custom(bundle, groups):
    members = set(bundle.namelist())
    for manifest in sorted(CUSTOM.glob('batch-*/manifest.json')):
        data = json.loads(manifest.read_text())
        batch = manifest.parent
        items = [(f, f['source_path']) for f in data.get('files', [])] + \
                [(s, s['source_path']) for s in data.get('scripts', [])]
        for item, src in items:
            if src.startswith('kubejs/assets/'):
                continue  # language sources: covered by the language layers
            en_text = (batch / item['snapshot']).read_text(encoding='utf-8-sig')
            if src in members:
                zh_text = bundle.read(src).decode('utf-8-sig')
            elif (ROOT / '.minecraft' / src).exists():
                zh_text = (ROOT / '.minecraft' / src).read_text(encoding='utf-8-sig')
            else:
                continue
            sec = groups.section('custom', f'custom:{src}', src, 'custom')
            if src.endswith('.json'):
                zflat = dict(flatten(parse_json(zh_text)))
                for jp, ev in flatten(parse_json(en_text)):
                    zv = zflat.get(jp)
                    if zv is not None and zv != ev:
                        sec.append(entry(f'custom:{src}#{jp}', jp, ev, zv, 'project', None, None, 'custom'))
            else:
                a, b = en_text.splitlines(), zh_text.splitlines()
                for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                    if tag == 'equal':
                        continue
                    sec.append(entry(f'custom:{src}@{i1}', f'L{i1 + 1}-{i2}', '\n'.join(a[i1:i2]),
                                     '\n'.join(b[j1:j2]), 'project', None, None, 'code'))
    sec = groups.section('custom', 'custom:mod_names', '模组名称 (客户端脚本)', 'custom')
    for mid, v in sorted(MOD_NAMES.items()):
        sec.append(entry(f'custom:mod_names:{mid}', mid, v['english'], v['translation'], 'project', None, None, 'custom'))


def mod_meta(gid):
    if gid == 'quests':
        return 'FTB 任务书', '整合包任务书', 'quests'
    if gid == 'custom':
        return '整合包特色内容', '商店 / 对话 / 运行时脚本', 'custom'
    kind, ident = gid.split(':', 1)
    if kind == 'mod':
        for mods in JAR_MODS.values():
            for mid, name in mods:
                if mid == ident:
                    return name, MOD_NAMES.get(ident, {}).get('translation', ''), 'mod'
        return ident, MOD_NAMES.get(ident, {}).get('translation', ''), 'mod'
    return ident, '', 'mod'


def main():
    layers, bundle = load_layers()
    groups = Groups()
    collect_quests(bundle, groups)
    collect_custom(bundle, groups)
    collect_lang(layers, groups)
    collect_docs(layers, groups)

    (OUT / 'mods').mkdir(parents=True, exist_ok=True)
    for old in (OUT / 'mods').glob('*.json'):
        old.unlink()
    index = []
    for gid, g in groups.mods.items():
        sections = [s for s in g['sections'].values() if s['entries']]
        if not sections:
            continue
        name, zh_name, kind = mod_meta(gid)
        fname = re.sub(r'[^A-Za-z0-9_.-]', '_', gid) + '.json'
        counts = collections.Counter()
        for s in sections:
            for e in s['entries']:
                counts[e['o']] += 1
                counts['total'] += 1
        index.append({'id': gid, 'name': name, 'zh': zh_name, 'kind': kind, 'file': fname,
                      'excluded': all(e.get('ex') for s in sections for e in s['entries']),
                      'counts': dict(counts),
                      'sections': [{'id': s['id'], 'title': s['title'], 'kind': s['kind'],
                                    'n': len(s['entries'])} for s in sections]})
        (OUT / 'mods' / fname).write_text(json.dumps({'id': gid, 'sections': sections},
                                                     ensure_ascii=False, separators=(',', ':')))
    order = {'quests': 0, 'custom': 1, 'mod': 2}
    index.sort(key=lambda m: (order[m['kind']], m['excluded'], m['name'].lower()))
    (OUT / 'index.json').write_text(json.dumps({'pack': PROJECT['target_pack_version'], 'mods': index},
                                               ensure_ascii=False, indent=1))
    total = collections.Counter()
    for m in index:
        total.update(m['counts'])
    print(json.dumps({'groups': len(index), **total}, ensure_ascii=False))


if __name__ == '__main__':
    main()
