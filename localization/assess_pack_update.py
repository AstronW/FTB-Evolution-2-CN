"""Read-only instance update audit against preserved 1.4.0 translation inputs.

Writes only versioned assessment reports. Does not migrate bindings or install.
Global language observations use historical inventory scope; newly seen keys are
candidates, not a count of added player-facing text.
"""
import pathlib,json,hashlib,gzip,zipfile,io,re,sys
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'localization'));from quest_translation import load_source
G=pathlib.Path(json.load(open(R/'project.json'))['target_instance']);W=R/'.minecraft'
h=lambda b:hashlib.sha256(b).hexdigest()
def diff(a,b):return {'unchanged':sum(a[k]==b[k] for k in a.keys()&b.keys()),'changed':[{'key':k,'old':a[k],'new':b[k]} for k in sorted(a.keys()&b.keys()) if a[k]!=b[k]],'added':[{'key':k,'new':b[k]} for k in sorted(b.keys()-a.keys())],'removed':[{'key':k,'old':a[k]} for k in sorted(a.keys()-b.keys())]}
q={}
for p in (W/'config/ftbquests/quests/lang/en_us').rglob('*.json5'):
 rel=p.relative_to(W);n=G/rel;q[str(rel)]=diff(load_source(p),load_source(n) if n.exists() else {})
langs={};docs={};jars=[];nested=[];errors=[];nativezh={}
def ingest(z,origin):
 for n in z.namelist():
  if n.endswith('.jar') and n.startswith(('META-INF/jarjar/','META-INF/jars/')):
   b=z.read(n);nested.append({'source':origin+'!'+n,'sha256':h(b)});ingest(zipfile.ZipFile(io.BytesIO(b)),origin+'!'+n)
  elif re.fullmatch('assets/[^/]+/lang/(en_us|zh_cn).json',n):
   try:
    d=json.loads(z.read(n),strict=False)
    (langs if n.endswith('/en_us.json') else nativezh).update({k:{'english':v,'namespace':n.split('/')[1],'source':origin,'path':n} for k,v in d.items() if isinstance(v,str)})
   except Exception as e:errors.append([origin,n,str(e)])
  elif n.startswith(('assets/','data/')) and n.endswith(('.md','.mdx','.txt','.json')):docs[n]={'sha256':h(z.read(n)),'sha256_lf':h(z.read(n).decode('utf-8-sig',errors='replace').replace('\r\n','\n').replace('\r','\n').encode()),'source':origin}
for p in sorted((G/'mods').glob('*.jar')):
 jars.append({'file':p.name,'sha256':h(p.read_bytes())});ingest(zipfile.ZipFile(p),str(p))
for p in sorted((G/'kubejs').rglob('*')):
 if not p.is_file():continue
 n=p.relative_to(G/'kubejs').as_posix()
 if re.fullmatch('assets/[^/]+/lang/en_us.json',n):
  d=json.loads(p.read_bytes());langs.update({k:{'english':v,'namespace':n.split('/')[1],'source':str(p),'path':n} for k,v in d.items() if isinstance(v,str)})
 elif n.startswith(('assets/','data/')) and p.suffix in {'.md','.mdx','.txt','.json'}:docs[n]={'sha256':h(p.read_bytes()),'sha256_lf':h(p.read_text(encoding='utf-8-sig').encode()),'source':str(p)}
oldrows=json.load(gzip.open(R/'localization/reports/remaining-1.4.0-language-detail.json.gz'));old={r['key']:r['english'] for r in oldrows};new={k:v['english'] for k,v in langs.items() if re.search('[A-Za-z]',v['english'])};ld=diff(old,new)
def read(p):return json.loads(p.read_text())
def filehash(p):return h(p.read_bytes()) if p.is_file() else None
instance=read(G/'instance.json');version=instance['version']
assert version != '1.4.0', 'This audit expects an instance newer than the preserved baseline'
# Include added quest language files as well as the old file set.
for p in (G/'config/ftbquests/quests/lang/en_us').rglob('*.json5'):
 rel=p.relative_to(G)
 if str(rel) not in q:q[str(rel)]=diff({},load_source(p))
custom=[]
for p in sorted((W/'kubejs/assets').glob('*/lang/en_us.json')):
 n=G/p.relative_to(W)
 if p.parent.parent.name!='ftb_custom':custom.append({'path':str(p.relative_to(W)),**diff(read(p),read(n) if n.exists() else {})})
for p in sorted((G/'kubejs/assets').glob('*/lang/en_us.json')):
 if not (W/p.relative_to(G)).exists():custom.append({'path':str(p.relative_to(G)),**diff({},read(p))})
installed_path=R/'dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json'
installed=read(installed_path)['files'] if installed_path.exists() else {}
installed_changes=[{'path':k,'expected':v,'actual':filehash(G/k)} for k,v in installed.items() if filehash(G/k)!=v]
# Compare source and translated-output hashes separately: an installed translation
# must not be mistaken for an upstream English edit.
custom_files=[]
for folder in sorted((R/'localization/custom/batches').glob('batch-*')):
 m=read(folder/'manifest.json')
 for row in m.get('files',[])+m.get('scripts',[]):
  k=row['source_path'];actual=filehash(G/k);src=row.get('source_sha256',row.get('sha256'));output=row.get('output_sha256')
  snap=folder/row['snapshot']
  if not output and (W/k).is_file():output=filehash(W/k)
  custom_files.append({'batch':folder.name,'path':k,'source_sha256':src,'output_sha256':output,'current_sha256':actual,'state':'original_source' if actual==src else 'installed_translation' if actual==output else 'changed_or_missing'})
manuals=[]
for k,v in read(R/'localization/manuals/source_manifest.json').items():
 ns,rel=k.split('/',1);base={'ftb':'guides/ftb','ftbic':'ftbic','nodeworks':'nodeworksguide'}[ns];path=f'assets/{ns}/{base}/{rel}'
 manuals.append({'group':'core','path':path,'old_sha256':v,'new_sha256':docs.get(path,{}).get('sha256_lf')})
for k,v in read(R/'localization/manuals_extra/source_manifest.json')['documents'].items():
 manuals.append({'group':'extra','path':k,'old_sha256':v['source_sha256'],'new_sha256':docs.get(k,{}).get('sha256_lf')})
for k,v in read(R/'localization/cfpa_review/build-manifest.json')['manual_sources'].items():
 manuals.append({'group':'cfpa','path':k,'old_sha256':v['sha256_lf'],'new_sha256':docs.get(k,{}).get('sha256_lf')})
for k,v in read(R/'localization/patchouli/source_manifest.json').items():
 ns,book,rel=k.split('/',2);path=f'assets/{ns}/patchouli_books/{book}/en_us/{rel}'
 manuals.append({'group':'patchouli','path':path,'old_sha256':v,'new_sha256':docs.get(path,{}).get('sha256')})
manual_changes=[r for r in manuals if r['old_sha256']!=r['new_sha256']]
preexisting_overrides=[]
for row in manual_changes[:]:
 local=W/'kubejs'/row['path'];current=G/'kubejs'/row['path']
 if local.is_file() and current.is_file() and local.read_bytes()==current.read_bytes():
  row['reason']='Unchanged pack override differs from original JAR manifest; preexisting effective-source discrepancy'
  preexisting_overrides.append(row);manual_changes.remove(row)
known=set(read(R/'localization/manuals_extra/source_manifest.json')['known_pages'])
new_pages=[{'path':k,'source':v['source']} for k,v in sorted(docs.items()) if k.endswith(('.md','.mdx')) and k not in known and not re.search(r'/(?:_?[a-z]{2}_[a-z]{2})(?:/|_)',k) and '/translated/' not in k and '/node_modules/' not in k and (k.startswith('assets/') or '/wiki/' in k)]
# Existing complete batches can supply source entries missed by the old inventory
# (notably Sodium nested resources); these are not newly added text.
known_keys=set(old)
for folder in (R/'localization/ordinary').glob('batch-*'):
 p=folder/'source-en_us.json'
 if p.exists():known_keys.update(read(p))
omitted=read(R/'localization/reports/remaining-1.4.0-language-summary.json')['omitted_non_player_text']
known_keys.update(r['key'] for r in omitted)
observed=[]
for r in ld['added']:
 if r['key'] in known_keys or r['key'].startswith(('_comment','__comment')):continue
 origin=langs[r['key']];observed.append({**r,**origin,'native_zh':nativezh.get(r['key'],{}).get('english')})
oldfiles={pathlib.Path(r['source'].split('!')[0]).name for r in oldrows if '/mods/' in r['source']}
currentfiles={r['file'] for r in jars}
# All hashes bound by ordinary batches are checked, without replacing vanished paths.
bindings=[]
for p in sorted((R/'localization/ordinary').glob('batch-*/manifest.json')):
 m=read(p);jar=R/m['jar'];expected=m.get('jar_sha256');actual=filehash(jar)
 if actual is None or expected and actual!=expected:bindings.append({'batch':p.parent.name,'jar':m['jar'],'expected':expected,'actual':actual})
feedback=read(R/'localization/feedback_20261019/manifest.json')['source_inputs']
feedback_changes=[{'path':k,'expected':v,'actual':filehash(G/k)} for k,v in feedback.items() if filehash(G/k)!=v]
quest_structure=[]
base=W/'config/ftbquests/quests'
for p in sorted(base.rglob('*')):
 if p.is_file() and 'lang' not in p.relative_to(base).parts:
  target=G/p.relative_to(W)
  if filehash(p)!=filehash(target):quest_structure.append({'path':str(p.relative_to(W)),'old':filehash(p),'new':filehash(target)})
pack_asset_changes=[]
for p in sorted((W/'kubejs/assets').rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(W)
 if re.search(r'/(?:_?zh_[a-z]+)(?:/|\.)',str(rel)) or '/ftb_custom/' in str(rel):continue
 current=G/rel
 if filehash(p)!=filehash(current):pack_asset_changes.append({'path':str(rel),'old':filehash(p),'new':filehash(current)})
report={'date':'2026-10-20','baseline':'1.4.0','actual_pack':version,'instance':str(G),'minecraft':instance['mcVersion'],'modloader':instance['modLoader'],'in_game_tested':False,
'method':['Read-only local inputs; no source manifest rebinding, rebuild, or installation.','Current top-level and recursively nested JAR assets/data; KubeJS same-path overrides. Deterministic filename order is not runtime collision evidence. Selected external resource packs are not treated as upstream.','Historical global language inventory omitted some nested/developer/project-generated keys. Newly observed keys are review candidates, not proven version additions or missing translations.','Markdown text hashes normalize CRLF/CR to LF; Patchouli uses raw UTF-8 hashes, matching historical extraction.','Full old mod inventory unavailable; missing historical language-source filenames show rebinding needs, not a total updated-mod count. Official historical API returned HTTP 403.'],
'instance_metadata_sha256':filehash(G/'instance.json'),'current_mods':jars,'nested_jars':nested,'quests':q,'quest_structure_changes':quest_structure,'pack_asset_changes':pack_asset_changes,'custom_languages':custom,'custom_files':custom_files,'manuals_checked':len(manuals),'manual_changes':manual_changes,'preexisting_effective_source_discrepancies':preexisting_overrides,'manual_new_page_candidates':new_pages,'global_language_delta':{k:v for k,v in ld.items() if k!='added'},'new_language_candidates':observed,'ordinary_broken_bindings':bindings,'feedback_broken_bindings':feedback_changes,'historical_language_source_jars_missing':sorted(oldfiles-currentfiles),'installation_record_available':bool(installed),'installed_files_checked':len(installed),'installed_file_changes':installed_changes,'resource_pack_selection':next((l for l in (G/'options.txt').read_text().splitlines() if l.startswith('resourcePacks:')),None),'parse_errors':errors}
out=R/f'localization/reports/update-{version}-assessment.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Report:',out)
print('Quests:',{a:sum(len(v[a]) if isinstance(v[a],list) else v[a] for v in q.values()) for a in ['unchanged','changed','added','removed']})
print('Manual changes:',len(manual_changes));print('New page candidates:',len(new_pages));print('Broken ordinary bindings:',len(bindings));print('Installed changes:',len(installed_changes))
