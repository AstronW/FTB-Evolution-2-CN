"""Read-only manual inventory; emits assessment data, never modifies game resources."""
import collections, json, pathlib, re, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
MC = ROOT / '.minecraft'
resources = {}
lang_layers = collections.defaultdict(dict)
lang_sources = {}
jar_baseline = {}
errors = []
def ingest(path, data, source):
    resources[path] = (data, source)
    m = re.fullmatch(r'assets/([^/]+)/lang/(en_us|zh_cn)\.json', path)
    if m:
        try:
            parsed = json.loads(data)
            lang_layers[(m[1], m[2])].update(parsed)
            for key in parsed: lang_sources[(m[1], m[2], key)] = source
        except ValueError as e:
            errors.append({'path':path,'source':source,'error':str(e)})
for jar in sorted((MC / 'mods').glob('*.jar')):
    with zipfile.ZipFile(jar) as z:
        for n in z.namelist():
            if n.startswith(('assets/', 'data/')) and n.endswith(('.json', '.md', '.mdx', '.txt')):
                content = z.read(n).decode('utf-8-sig', errors='replace')
                jar_baseline[n] = content
                ingest(n, content, jar.name)
# Inventory candidate layers. Exact active layer priority is a runtime check.
pack = MC / 'resourcepacks/Minecraft-Mod-Language-Modpack-Converted-26.1.2.zip'
with zipfile.ZipFile(pack) as z:
    for n in z.namelist():
        if n.endswith(('.json', '.md', '.mdx', '.txt')):
            ingest(n, z.read(n).decode('utf-8-sig', errors='replace'), 'CFPA:' + pack.name)
for folder in ['kubejs/assets', 'kubejs/data']:
    for p in sorted((MC / folder).rglob('*')):
        if p.is_file() and p.suffix in {'.json', '.md', '.mdx', '.txt'}:
            ingest(folder.split('/')[-1] + '/' + p.relative_to(MC / folder).as_posix(), p.read_text(errors='replace'), p.relative_to(ROOT).as_posix())
# Include selected supplemental resource packs, including our completed manuals.
options = (MC / 'options.txt').read_text()
selected = json.loads(next(line.split(':', 1)[1] for line in options.splitlines() if line.startswith('resourcePacks:')))
for entry in selected:
    if not entry.startswith('file/'): continue
    supplemental = MC / 'resourcepacks' / entry[5:]
    if supplemental == pack: continue
    if supplemental.is_dir():
        for p in sorted(supplemental.rglob('*')):
            n = p.relative_to(supplemental).as_posix()
            if p.is_file() and n.startswith(('assets/', 'data/')) and p.suffix in {'.json', '.md', '.mdx', '.txt'}:
                ingest(n, p.read_text(errors='replace'), 'Resourcepack:' + supplemental.name)
    elif supplemental.is_file() and zipfile.is_zipfile(supplemental):
        with zipfile.ZipFile(supplemental) as z:
            for n in z.namelist():
                if n.startswith(('assets/', 'data/')) and n.endswith(('.json', '.md', '.mdx', '.txt')):
                    ingest(n, z.read(n).decode('utf-8-sig', errors='replace'), 'Resourcepack:' + supplemental.name)
def parse(n):
    try: return json.loads(resources[n][0])
    except (ValueError, TypeError) as e:
        errors.append({'path': n, 'source': resources[n][1], 'error': str(e)})
        return {}
cjk = re.compile(r'[\u3400-\u9fff]')
def words(s):
    # Approximate English volume, stripping common resource references/markup.
    s = re.sub(r'```.*?```', '', s, flags=re.S)
    s = re.sub(r'<[^>]*>|\$\([^)]*\)|\]\([^)]*\)|[a-z_]+:[a-z0-9_./-]+', ' ', s)
    return len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", s))
langs = dict(lang_layers)
referenced = set()
key_owners = {k:ns for (ns,locale),data in langs.items() if locale=='en_us' for k in data}
rows = collections.defaultdict(list)
def add(group, unit, en, zh='', source='', target=''):
    if not isinstance(en, str) or not re.search('[A-Za-z]', en): return
    ok = isinstance(zh, str) and bool(cjk.search(zh))
    rows[group].append({'unit': unit, 'covered_candidate': ok, 'english_words_approx': words(en), 'missing_words_approx': 0 if ok else words(en), 'source': source, 'zh_source': target})
# Standalone Markdown/MDX, Patchouli JSON and legacy Bestiary TXT.
for n, (text, source) in resources.items():
    if n.endswith(('.md', '.mdx')) and n.startswith(('assets/', 'data/')):
        if n.endswith(('credits_and_copyright.md', '00_readme.md')) or '/lua/' in n: continue
        if re.search(r'/(?:_?[a-z]{2}_[a-z]{2})(?:/|_)', n): continue
        if '/translated/' in n: continue
        parts = n.split('/')
        group = parts[3] if '/oracle_index/books/' in n else parts[1]
        if '/oracle_index/books/' in n:
            root = '/'.join(parts[:4])
            candidate = root + '/translated/zh_cn/' + '/'.join(parts[4:])
            matches = [candidate] if candidate in resources else []
        else:
            matches = [n[:m.start()] + '/_zh_cn' + n[m.start():] for m in re.finditer('/', n) if m.start() > len('assets/' + parts[1])]
            matches = [x for x in matches if x in resources]
        target = matches[-1] if matches else ''
        add(group + ' [Markdown]', n, text, resources.get(target, ('', ''))[0], source, resources.get(target, ('', ''))[1])
    elif '/patchouli_books/' in n and '/en_us/' in n and n.endswith('.json'):
        zhpath = n.replace('/en_us/', '/zh_cn/')
        en, zh = parse(n), parse(zhpath) if zhpath in resources else {}
        ns = n.split('/')[1]
        def walk(a, b, loc=''):
            if isinstance(a, dict):
                for k,v in a.items():
                    if k in {'name','description','text','title','subtitle','landing_text','caption'}:
                        if isinstance(v,str):
                            if v in key_owners:
                                referenced.add((key_owners[v],v))
                                continue # Counted once in lang keys.
                            add(ns + ' [Patchouli]', n + '#' + loc + k, v, b.get(k,'') if isinstance(b,dict) else '', source, resources.get(zhpath, ('',''))[1])
                    if isinstance(v,(dict,list)): walk(v,b.get(k,{}) if isinstance(b,dict) else {},loc+k+'.')
            elif isinstance(a,list):
                for i,v in enumerate(a):walk(v,b[i] if isinstance(b,list) and i<len(b) else {},loc+str(i)+'.')
        walk(en,zh)
    elif re.search(r'/lang/bestiary/en_us_0/.*\.txt$', n):
        zn = n.replace('/en_us_0/', '/zh_cn_0/')
        add('iceandfire [Bestiary]',n,text,resources.get(zn,('',''))[0],source,resources.get(zn,('',''))[1])
# Handbooks backed by localization keys; includes relevant adjuncts, excludes framework demo books.
prefixes = ('book.', 'info_book.', 'infobook.', 'gui.guide.', 'guide.betterfishtanks.', 'guide.animusnv.')
for (ns, locale), en in langs.items():
    if locale != 'en_us' or ns in {'modonomicon','cyclopscore'}: continue
    zh = langs.get((ns,'zh_cn'),{})
    for k,v in en.items():
        if k.startswith(prefixes) or (ns,k) in referenced:
            add(ns + ' [language keys]',k,v,zh.get(k,''),lang_sources.get((ns,'en_us',k),''),lang_sources.get((ns,'zh_cn',k),''))
summaries = []
for group, units in sorted(rows.items()):
    summaries.append({'group':group,'units':len(units),'covered_candidates':sum(x['covered_candidate'] for x in units),'missing_candidates':sum(not x['covered_candidate'] for x in units),'english_words_approx':sum(x['english_words_approx'] for x in units),'missing_words_approx':sum(x['missing_words_approx'] for x in units)})
local_overrides = [{'path':n,'changed_from_jar': n not in jar_baseline or t != jar_baseline[n], 'new_in_pack':n not in jar_baseline} for n,(t,src) in resources.items() if src.startswith('.minecraft/kubejs/') and (n.endswith(('.md','.mdx')) or '/patchouli_books/' in n or '/guideme_guides/' in n)]
out = {'local_overrides':local_overrides,'method':'Static candidate coverage: a same-path zh_cn document or same language key containing CJK. Not proof of complete/current translation or runtime activation. Units are documents, visible JSON fields, or language keys; do not add as page counts. English words approximate markup-stripped.', 'summaries':summaries,'units':dict(rows),'parse_errors':errors}
report = ROOT / 'localization/reports/manual-inventory.json'
report.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
for s in summaries: print(s['group'], s['units'], s['covered_candidates'], s['missing_candidates'], s['missing_words_approx'])
print('TOTAL missing words approximation:',sum(s['missing_words_approx'] for s in summaries))
print('PARSE ERRORS',len(errors))
