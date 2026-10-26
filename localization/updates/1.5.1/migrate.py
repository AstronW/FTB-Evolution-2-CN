"""Reviewed 1.4.1 -> 1.5.1 localization migration; writes the worktree only."""
from pathlib import Path
import collections, difflib, hashlib, json, shutil, sys, zipfile
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'localization'))
CONFIG=json.loads((ROOT/'project.json').read_text());GAME=Path(CONFIG['target_instance']);W=ROOT/CONFIG['worktree']
def read(p):return json.loads(p.read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def backup(p):
 p=Path(p).absolute();out=BASE/'before'/p.relative_to(ROOT)
 if p.is_file() and not out.exists():out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
 return out
def write(p,data):
 p=Path(p).absolute();backup(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data.encode() if isinstance(data,str) else data)
def dump(p,data):write(p,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def quests():
 import quest_translation as q
 oldfiles={p.relative_to(q.SOURCE):p for p in q.SOURCE.rglob('*.json5')}
 overrides=read(BASE/'quest-translations.json');records=[];old_to_new={}
 for rel,p in oldfiles.items():
  oldpath=backup(p);old=q.segments(q.load_source(oldpath));newpath=GAME/p.relative_to(W);new=q.segments(q.load_source(newpath))
  target=q.WORK/'translations'/rel.with_suffix('.json');oldzh=read(backup(target));out={};indices={}
  for block in difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_matching_blocks():
   for off in range(block.size):
    a,b=block.a+off,block.b+off
    if str(a) in oldzh:out[str(b)]=oldzh[str(a)];indices[str(a)]=str(b)
  for i,text in enumerate(new):
   if text in overrides:out[str(i)]=overrides[text]
   elif str(i) not in out:
    prior=[oldzh[str(j)] for j,s in enumerate(old) if s==text and str(j) in oldzh]
    if len(set(prior))==1:out[str(i)]=prior[0]
    else:raise ValueError((str(rel),i,text))
  q.translate(q.load_source(newpath),out,read(q.WORK/'terms.json'))
  for i,text in enumerate(new):
   if text in overrides:records.append({'file':str(rel),'segment':i,'source':text,'translation':out[str(i)]})
  dump(target,out);write(p,newpath.read_bytes());old_to_new[str(target.relative_to(ROOT))]=indices
 for p in (GAME/'config/ftbquests/quests').rglob('*'):
  if p.is_file() and 'lang' not in p.relative_to(GAME/'config/ftbquests/quests').parts:write(W/p.relative_to(GAME),p.read_bytes())
 dump(q.WORK/'source_manifest.json',{str(p.relative_to(q.SOURCE)):sha(p.read_bytes()) for p in sorted(q.SOURCE.rglob('*.json5'))})
 names=read(q.WORK/'quest_item_names.json');jar=next((GAME/'mods').glob('ftb-evolution-companion-*.jar'));names['source_jar']=str(Path('.minecraft/mods')/jar.name);dump(q.WORK/'quest_item_names.json',names)
 extra=read(q.WORK/'quest_extra_labels.json')
 for group in extra:
  if group['source'].endswith('ftb-en_us.json'):
   source=GAME/'kubejs/assets/ftb/lang/en_us.json';write(ROOT/group['source'],source.read_bytes());group['source_sha256']=sha(source.read_bytes())
 dump(q.WORK/'quest_extra_labels.json',extra)
 path=q.WORK/'feedback_20261019/quest-name-changes.json';changes=read(backup(path))
 for row in changes:
  if row['key'] in old_to_new.get(row['file'],{}):row['key']=old_to_new[row['file']][row['key']]
  else:
   values=read(ROOT/row['file']);matches=[k for k,v in values.items() if v==row['zh']];assert len(matches)==1,row;row['key']=matches[0]
 dump(path,changes);dump(BASE/'quest-deltas.json',records)

def custom():
 bindings=read(ROOT/CONFIG['custom_adaptation']['source_bindings']);bindings['target_pack_version']='1.5.1'
 for ns,row in bindings['sources'].items():
  data=(GAME/row['path']).read_bytes();write(W/row['path'],data);row['sha256']=sha(data)
 dump(ROOT/'localization/custom/source-bindings-1.5.1.json',bindings)
 # Preserve old immutable batch-003 sources; the new correction is its own batch.
 key='skill.ftb.melee.unarmed_hub.description';en=read(GAME/'kubejs/assets/ftb/lang/en_us.json')[key]
 manifest={'target_pack_version':'1.5.1','scope':'Pack 1.5.1 unarmed skill source correction','files':[], 'language_entries':[{'key':key,'en':en,'zh':'+3 徒手伤害. 解锁格斗家与重装战士路线.','source_path':'kubejs/assets/ftb/lang/en_us.json','output_path':'.minecraft/kubejs/assets/ftb/lang/zh_cn.json'}]}
 dump(ROOT/'localization/custom/batches/batch-006/manifest.json',manifest)
 # Batch version labels describe provenance, not current resource identity.
 for p in (ROOT/'localization/custom/batches').glob('batch-*/manifest.json'):backup(p)

def ordinary():
 import ordinary_translation as o
 from source_archive import read_resource
 records=[];revisions=read(o.WORK/'overlay-revisions.json');reviewed=read(BASE/'language-translations.json')
 for folder in sorted(o.WORK.glob('batch-*')):
  if not (folder/'verification.json').exists():continue
  oldmanifest=read(backup(folder/'manifest.json'));old=read(backup(folder/'source-en_us.json'));values=read(backup(folder/'source-values.json'));zh={}
  for line in backup(folder/'zh-values.tsv').read_text().splitlines():
   i,v=line.split('\t',1);zh[values[int(i)]]=v.replace('\\n','\n')
  oldzh={k:oldmanifest['context_overrides'].get(k,zh[v]) for k,v in old.items()};manifest=dict(oldmanifest)
  container=manifest.pop('source_container',None)
  preferred=ROOT/(container['jar'] if container else manifest['jar'])
  nested=[container['member']] if container else [x['path'] for x in manifest.get('nested_jars',[])] if 'nested_jars' in manifest else [manifest['nested_jar']] if 'nested_jar' in manifest else []
  raw,evidence=read_resource(manifest['language_path'],preferred,nested_paths=nested)
  jar=Path(evidence['jar']);manifest['jar']=str(Path('.minecraft/mods')/jar.name);manifest['jar_sha256']=evidence['jar_sha256'];manifest['resource_binding']=evidence
  for k in ['nested_jar','nested_jar_sha256','nested_jars']:manifest.pop(k,None)
  if evidence['nested_jars']:manifest['nested_jars']=evidence['nested_jars']
  current=json.loads(raw);selected={k:v for k,v in current.items() if k in old};changes={k:{'old':old[k],'new':v} for k,v in selected.items() if old[k]!=v}
  for k,r in changes.items():
   assert k in reviewed,(folder.name,k,r);newzh=reviewed[k]['translation'];assert reviewed[k]['source']==r['new']
   revision={'batch':folder.name,'namespace':manifest['namespace'],'key':k,'source':r['new'],'previous':oldzh[k],'translation':newzh,'reason':reviewed[k]['reason']}
   if revision not in revisions:revisions.append(revision)
   oldzh[k]=newzh
  manifest['include_keys']=list(selected);newvals=list(dict.fromkeys(selected.values()));seen={}
  for k,en in selected.items():seen.setdefault(en,oldzh[k])
  manifest['context_overrides']={k:oldzh[k] for k,en in selected.items() if k in oldmanifest['context_overrides'] or oldzh[k]!=seen[en]}
  dump(folder/'manifest.json',manifest);dump(folder/'source-en_us.json',selected);dump(folder/'source-values.json',newvals)
  write(folder/'zh-values.tsv','\n'.join(str(i)+'\t'+seen[v].replace('\n','\\n') for i,v in enumerate(newvals))+'\n')
  records.append({'batch':folder.name,'state':'active','namespace':manifest['namespace'],'old_jar':oldmanifest['jar'],'jar':manifest['jar'],'jar_sha256':manifest.get('jar_sha256',sha((ROOT/manifest['jar']).read_bytes())),'language_path':manifest['language_path'],'language_sha256':sha(raw),'source_changes':changes,'removed_compatibility_keys':{k:{'source':v,'translation':oldzh[k]} for k,v in old.items() if k not in current},'before':str((BASE/'before'/folder.relative_to(ROOT)).relative_to(ROOT))})
 dump(o.WORK/'overlay-revisions.json',revisions);dump(BASE/'ordinary-rebind.json',{'target_pack_version':'1.5.1','batches':records,'in_game_tested':False})
 for folder in sorted(o.WORK.glob('batch-*')):
  if (folder/'verification.json').exists():o.process(folder,True)

def core_manuals(prepare=False):
 import manual_translation as m
 mf=m.BASE/'source_manifest.json';prior=read(backup(mf));pending={};records=[]
 # The new pack English override takes precedence over the unchanged FTBIC JAR.
 path='kubejs/assets/ftbic/ftbic/materials/alloys.md';write(W/path,(GAME/path).read_bytes())
 current=m.sources();reviewed=read(BASE/'core-manual-translations.json') if (BASE/'core-manual-translations.json').exists() else {}
 for key,text in current.items():
  if sha(text.encode())==prior.get(key):continue
  trans=m.BASE/'translations'/Path(key).with_suffix('.json');oldzh=read(backup(trans)) if trans.exists() else {};oldkey=key
  if key=='nodeworks/nodeworks-mechanics/moving-items.md':oldkey='nodeworks/example-setups/moving-items.md';oldzh=read(backup(m.BASE/'translations'/Path(oldkey).with_suffix('.json')))
  ns,rel=oldkey.split('/',1)
  if ns=='nodeworks':oldpath=BASE/'old-sources/assets/nodeworks/nodeworksguide'/rel;old=oldpath.read_text() if oldpath.exists() else ''
  else:
   with zipfile.ZipFile(next((GAME/'mods').glob('ftb-industrial-contraptions-*.jar'))) as z:old=z.read('assets/ftbic/ftbic/'+rel).decode()
  if old:assert sha(old.encode())==prior[oldkey],(oldkey,'historical source mismatch')
  a,b=old.splitlines(),text.splitlines();out={}
  for block in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_matching_blocks():
   for off in range(block.size):
    i,j=block.a+off,block.b+off
    if str(i) in oldzh:out[str(j)]=oldzh[str(i)]
  # New line translations are tied to exact current English text, not just indexes.
  for i,line in m.segments(text):
   if str(i) in out:continue
   match=reviewed.get(key,{}).get(str(i))
   if match:
    assert match['source']==line,(key,i);out[str(i)]=match['translation']
   else:pending.setdefault(key,{})[str(i)]={'source':line}
  if not prepare and key not in pending:dump(trans,out)
  records.append({'page':key,'old_page':oldkey,'old_sha256':prior.get(oldkey),'source_sha256':sha(text.encode()),'reviewed_segments':len(reviewed.get(key,{})),'pending_segments':len([i for i,_ in m.segments(text) if str(i) not in out]),'translated_lines':len(out)})
 dump(BASE/'core-manual-pending.json',pending)
 if prepare:return
 assert not pending, 'Review core-manual-pending.json'
 # Retire the removed path, keeping its full source/translation in before/.
 old=m.BASE/'translations/nodeworks/example-setups/moving-items.json';backup(old)
 if old.exists():old.unlink()
 out=m.target('nodeworks/example-setups/moving-items.md');backup(out)
 if out.exists():out.unlink()
 dump(mf,{k:sha(v.encode()) for k,v in current.items()});dump(BASE/'core-manual-deltas.json',records)

def extra_manuals(prepare=False):
 import manual_extra_translation as m
 from source_archive import read_resource
 prior=read(backup(m.MANIFEST));manifest=json.loads(json.dumps(prior));records=[];pending={}
 reviewed=read(BASE/'extra-manual-translations.json') if (BASE/'extra-manual-translations.json').exists() else {}
 for path,entry in manifest['documents'].items():
  source=m.SOURCES/path;oldsource=backup(source).read_text();oldzh=backup(m.TRANSLATIONS/path).read_text();assert m.digest(oldsource)==entry['source_sha256']
  live=GAME/'kubejs'/path
  if live.exists():text=m.normalize(live.read_text());origin=str(live);evidence=None
  elif Path(entry['source']).suffix=='.jar':
   raw,evidence=read_resource(path,entry['source']);text=m.normalize(raw.decode('utf-8-sig'));origin=evidence['jar']
  else:
   text=m.normalize(Path(entry['source']).read_text());origin=entry['source'];evidence=None
  if m.digest(text)!=entry['source_sha256']:
   a,b=oldsource.splitlines(),text.splitlines();zh=oldzh.splitlines();assert len(a)==len(zh);out={}
   for block in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_matching_blocks():
    for off in range(block.size):out[block.b+off]=zh[block.a+off]
   for i,line in enumerate(b):
    if i in out:continue
    match=reviewed.get(path,{}).get(str(i))
    if match:assert match['source']==line;out[i]=match['translation']
    elif not line.strip() or not __import__('re').search('[A-Za-z]',line):out[i]=line
    else:pending.setdefault(path,{})[str(i)]={'source':line}
   if not prepare and path not in pending:write(m.TRANSLATIONS/path,'\n'.join(out[i] for i in range(len(b)))+'\n')
   records.append({'page':path,'old_sha256':entry['source_sha256'],'new_sha256':m.digest(text)})
  if not prepare:
   entry['source']=origin;entry['source_sha256']=m.digest(text);entry['english_words_approx']=m.word_count(text)
   if evidence:entry['resource_binding']=evidence
   write(source,text)
 dump(BASE/'extra-manual-pending.json',pending)
 if prepare:return
 assert not pending,'Review extra-manual-pending.json'
 manifest['target_pack_version']='1.5.1';manifest['known_pages']=sorted(m.known_pages());dump(m.MANIFEST,manifest);dump(BASE/'extra-manual-deltas.json',records)
