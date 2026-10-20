"""Carry reviewed key translations forward only after exact source comparison."""
from pathlib import Path
import collections,hashlib,json,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent;sys.path.insert(0,str(ROOT/'localization'))
import ordinary_translation as o
GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
def read(p):return json.loads(p.read_text())
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def backup(p):
 b=BASE/'before'/p.relative_to(ROOT)
 if p.exists() and not b.exists():b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,b)
 return b
index=collections.defaultdict(list)
for jar in sorted((GAME/'mods').glob('*.jar')):
 with zipfile.ZipFile(jar) as z:
  for name in z.namelist():
   if name.endswith('/lang/en_us.json'):index[name].append(jar)
rows=[];revisions=read(o.WORK/'overlay-revisions.json');backup(o.WORK/'overlay-revisions.json')
for folder in sorted(o.WORK.glob('batch-*')):
 if not (folder/'verification.json').exists():continue
 originals={name:backup(folder/name) for name in ['manifest.json','source-en_us.json','source-values.json','zh-values.tsv']}
 manifest=read(originals['manifest.json']);old=read(originals['source-en_us.json']);values=read(originals['source-values.json']);zvalues={}
 for line in originals['zh-values.tsv'].read_text().splitlines():
  i,v=line.split('\t',1);zvalues[values[int(i)]]=v.replace('\\n','\n')
 oldzh={k:manifest['context_overrides'].get(k,zvalues[v]) for k,v in old.items()}
 jar=ROOT/manifest['jar']
 if not jar.exists():
  candidates=index[manifest['language_path']]
  if not candidates and manifest['namespace']=='wakes':
   archive=ROOT/'localization/archive/ordinary-1.4.0'/folder.name
   archive.parent.mkdir(parents=True,exist_ok=True);shutil.move(folder,archive)
   rows.append({'batch':folder.name,'state':'retired_mod','reason':'Wakes removed from actual 1.4.1 instance','old_jar':manifest['jar'],'archive':str(archive.relative_to(ROOT))});continue
  assert len(candidates)==1,(folder,candidates);jar=candidates[0]
 if jar.parent.resolve()==(GAME/'mods').resolve():manifest['jar']=str(Path('.minecraft/mods')/jar.name)
 if 'jar_sha256' in manifest:manifest['jar_sha256']=hashlib.sha256(jar.read_bytes()).hexdigest()
 raw=o.language_source(manifest);current=json.loads(raw)
 selected={k:v for k,v in current.items() if k in old};changed={k:{'old':old[k],'new':v} for k,v in selected.items() if old[k]!=v}
 for k,r in changed.items():
  assert k=='config.crystalix.show_wand_tooltips.tooltip',(folder,k,r)
  assert r['old'].replace('Default: false','Default: true')==r['new']
  assert 'false' in oldzh[k];newzh=oldzh[k].replace('false','true');oldzh[k]=newzh
  prev=read(ROOT/manifest['target'])[k]
  rev={'batch':folder.name,'namespace':manifest['namespace'],'key':k,'source':r['new'],'previous':prev,'translation':newzh,'reason':'1.4.1 source changes default from false to true; preserve formatting and line breaks.'}
  if not any(x['key']==k and x['source']==r['new'] for x in revisions):revisions.append(rev)
 manifest['include_keys']=list(selected);original_overrides=set(manifest['context_overrides']);newvals=list(dict.fromkeys(selected.values()));seen={}
 for k,en in selected.items():seen.setdefault(en,oldzh[k])
 if 'include_keys' not in read(originals['manifest.json']) and selected==current:manifest.pop('include_keys',None)
 manifest['context_overrides']={k:oldzh[k] for k,en in selected.items() if k in original_overrides or oldzh[k]!=seen[en]}
 dump(folder/'manifest.json',manifest);dump(folder/'source-en_us.json',selected);dump(folder/'source-values.json',newvals)
 (folder/'zh-values.tsv').write_text('\n'.join(str(i)+'\t'+seen[v].replace('\n','\\n') for i,v in enumerate(newvals))+'\n')
 rows.append({'batch':folder.name,'state':'active','namespace':manifest['namespace'],'old_jar':read(originals['manifest.json'])['jar'],'jar':manifest['jar'],'jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'language_path':manifest['language_path'],'language_sha256':hashlib.sha256(raw).hexdigest(),'previous_keys':len(old),'retained_keys':len(selected),'source_changes':changed,'removed_compatibility_keys':{k:{'source':v,'translation':oldzh[k]} for k,v in old.items() if k not in current},'before':str(originals['manifest.json'].parent.relative_to(ROOT))})
dump(o.WORK/'overlay-revisions.json',revisions);dump(BASE/'ordinary-rebind.json',{'target_pack_version':'1.4.1','batches':rows,'in_game_tested':False})
for folder in sorted(o.WORK.glob('batch-*')):
 if (folder/'verification.json').exists():o.process(folder,True)
print('Reconciled',len(rows),'existing batches')
