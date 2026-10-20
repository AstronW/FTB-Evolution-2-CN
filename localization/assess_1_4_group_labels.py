"""Audit Collapsible Groups' separate group_lang labels against fixed PR sources."""
from pathlib import Path
import collections,json,zipfile,tomllib
from reviewed_cfpa_overlay import load_verified_review
ROOT=Path(__file__).resolve().parent.parent
GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
REPORT=ROOT/'localization/reports'
mods=set()
for p in (GAME/'mods').glob('*.jar'):
 with zipfile.ZipFile(p) as z:
  n=next((n for n in ['META-INF/neoforge.mods.toml','META-INF/mods.toml','fabric.mod.json'] if n in z.namelist()),None)
  if n:
   d=json.loads(z.read(n)) if n.endswith('.json') else tomllib.loads(z.read(n).decode())
   mods.update(m.get('modId',m.get('id')) for m in d.get('mods',[d]))
scope=json.loads((ROOT/'localization/language_scope.json').read_text())
def excluded(mod):
 return mod in scope['excluded_namespaces'] or any(mod.startswith(p) for p in scope['excluded_namespace_prefixes'])
def required(req):
 if 'mod' in req:return req['mod'] in mods
 if 'any' in req:return any(required(r) for r in req['any'])
 if 'all' in req:return all(required(r) for r in req['all'])
 if 'not' in req:return not required(req['not'])
 return True
def referenced_mods(req):
 if 'mod' in req:return {req['mod']}
 return set().union(*(referenced_mods(x) for value in req.values() if isinstance(value,list) for x in value))
cache=REPORT/'cfpa-pr-audit'
index=json.loads((cache/'file-cache-index.json').read_text())
matched={i['path']:i for i in index if i['number']==6101 and i['status']=='ok'}
prefix='projects/assets/collapsible-groups/1.21/collapsible_groups/group_lang/'
en_index=matched[prefix+'en_us.json'];zh_index=matched[prefix+'zh_cn.json']
prior=json.loads((cache/en_index['cache_file']).read_text());zh=json.loads((cache/zh_index['cache_file']).read_text())
rows=[];skipped=[]
reviewed,_=load_verified_review()
adopted={d['key']:d for d in reviewed if d['status']=='accepted' and d.get('resource_domain')=='group_lang'}
with zipfile.ZipFile(next((GAME/'mods').glob('*collapsible*'))) as z:
 source=json.loads(z.read('assets/collapsible_groups/group_lang/en_us.json'))
 active=set()
 for n in z.namelist():
  if '/groups/' not in n or not n.endswith('/metadata.json'):continue
  metadata=json.loads(z.read(n));folder=n.rsplit('/',1)[0]
  if 'neoforge' not in metadata.get('loaders',['neoforge']):continue
  if not required(metadata.get('requirement',{})):continue
  category=folder.rsplit('/',1)[1]
  if excluded(category) or any(excluded(mod) for mod in referenced_mods(metadata.get('requirement',{})) if mod in mods):skipped.append(category);continue
  def refs(value):
   if isinstance(value,dict):
    if 'translate' in value:active.add(value['translate'])
    for v in value.values():refs(v)
   elif isinstance(value,list):
    for v in value:refs(v)
  refs(metadata.get('category',{}))
  for p in z.namelist():
   if p.startswith(folder+'/') and p.endswith('.json') and p!=n:
    value=json.loads(z.read(p))
    if value.get('enabled',True):refs(value.get('name',{}))
 project=json.loads((ROOT/'localization/manuals/group_lang-zh.json').read_text())
 for key,value in source.items():
  if key not in active:continue
  candidate=zh.get(key)
  installed=project.get(key)
  state='reviewed_cfpa_adopted' if key in adopted and adopted[key]['english']==value else 'project_translated' if installed and installed!=value else 'pr_source_match' if candidate and prior.get(key)==value else 'same_key_needs_review' if candidate else 'no_chinese_candidate'
  rows.append({'key':key,'english':value,'chinese':candidate,'project_chinese':installed,'source_english':prior.get(key),'state':state})
report={'method':'Separate non-global group_lang labels. Include groups whose category metadata mod requirement is met in this instance, honoring enabled flag and building/decoration exclusions by category. Does not evaluate runtime item filters or user config. project_translated marks labels translated in localization/manuals/group_lang-zh.json and built into the group_lang overlay; only matching PR #6101 candidates are listed as upstream reuse.','total_pack_labels':len(source),'active_in_scope_candidate_labels':len(rows),'counts':dict(collections.Counter(r['state'] for r in rows)),'excluded_categories':skipped,'pr_number':6101,'pr_head_sha':en_index['head_sha'],'source_version':'1.21','target_version':'26.1.2','rows':rows}
(REPORT/'remaining-1.4.0-group-labels.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in report.items() if k not in ['rows','method']})
