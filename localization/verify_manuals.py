"""Independent checks for the 164 scoped manual pages and supporting resources."""
import collections,hashlib,json,pathlib,re,sys,zipfile
import manual_translation as build
ROOT=pathlib.Path(__file__).resolve().parent.parent
BASE=ROOT/'localization/manuals'
PACK=ROOT/'.minecraft/resourcepacks/FTB-Evolution-2-Manuals-zh_CN'
src=build.sources()
assert len(src)==164 and sum(k.startswith('nodeworks/') for k in src)==75 and sum(k.startswith('ftb/') for k in src)==23 and sum(k.startswith('ftbic/') for k in src)==66
expected={build.target(k) for k in src}
extra_base=ROOT/'localization/manuals_extra'
extra_manifest=json.loads((extra_base/'source_manifest.json').read_text()) if (extra_base/'source_manifest.json').exists() else {'documents':{}}
extra_outputs={PACK/entry['target'] for path,entry in extra_manifest['documents'].items()
               if (extra_base/'translations'/path).exists() and not entry['target'].startswith('datapacks/') and entry['target'].endswith('.md')}
assert set(PACK.rglob('*.md'))==expected|extra_outputs,'Unexpected/missing manual output'
manifest=json.loads((BASE/'source_manifest.json').read_text())
corrections=json.loads((BASE/'source_corrections.json').read_text())
unchanged=[];latin=[];tables=0
allow=['FTB','Xy','Starcatcher','I','V','X','FTB Evolution 2','FTB Materials','Colossal Reactors','Energized Power','Just Dire Things','Just Dyna Things','Mob Flow Utilities','Compressium','Stellaris','Powah','Nautec','LTX','Neo Vitae','Anima',"Iron's Arms 'n Artifice",'Dimensional Resources','Horse Powered','AgriTech Evolved','Applied Flux','The One Probe','Jade','Curios','Shift','Enter','Space','Tab','JEI','TNT','JSON','Zap','FE','RF','mB','LV','MV','HV','EV','IV','III','VII','VI','II','I/O','ID','IO','Y','y','L','F','N','K','M','s','t','x']
node_api='ObserverCard RedstoneCard shulkerBox chest furnace step clock print require card items network z n Nodeworks Lua API CPU NBT nil true false number string bool CardHandle VariableHandle ItemsHandle BreakerHandle PlacerHandle UserHandle BreakBuilder CraftBuilder HandleList Channel Network Job InputItems Importer ImporterBuilder Stocker StockerBuilder Scheduler BoolVariableHandle NumberVariableHandle StringVariableHandle Breaker Placer BlockItem BlockState Minecraft BlockPos DyeColor onChange IO io Alt Ctrl Left-Alt TPS A B T get getAll getFirst cards channel channels find findEach insert tryInsert count craft shapeless handle route debug face slots powered strength set block state mine cancel isMining progress connect list from to filter roundrobin pull place isBlocked every start stop isRunning tick second delay ensure keep batch use isUsing mode setMode setFilter facing cas type toggle tryLock unlock increment decrement min max append length clear id name kind stackable maxStackSize hasData hasTag matches pcall'.split()
allow+=node_api
anchors_checked=0;code_lines=0
for key,en in src.items():
 assert hashlib.sha256(en.encode()).hexdigest()==manifest[key]
 zh=build.target(key).read_text();a=en.splitlines();b=zh.splitlines()
 plan=build.anchor_plan(key,en)
 for i,names in plan.items():
  import html
  for name in names:
   tag='<a name="'+html.escape(name,quote=True)+'" />'
   assert b[i].count(tag)==1,(key,i,'missing/duplicate heading anchor',name)
   b[i]=b[i].replace(tag+' ','',1)
   anchors_checked+=1
 in_code=False;lua_lines={}
 for i,line in enumerate(a):
  if line.lstrip().startswith('```'):in_code=not in_code;continue
  if in_code:
   pos=build.lua_comment(line)
   if pos is not None:lua_lines[i]=pos
   assert (line if pos is None else line[:pos+2])==(b[i] if pos is None else b[i][:pos+2]),(key,i,'executable code changed')
   code_lines+=1
 assert len(a)==len(b),(key,'line count')
 for i,(e,z) in enumerate(zip(a,b)):
  assert re.findall(r'<[^>]+>',e)==re.findall(r'<[^>]+>',z),(key,i,'component markup')
  assert re.findall(r'\]\(([^)]*)\)',e)==re.findall(r'\]\(([^)]*)\)',z),(key,i,'links')
  assert collections.Counter(re.findall(r'`[^`]+`',e))==collections.Counter(re.findall(r'`[^`]+`',z)),(key,i,'inline code')
  if e.startswith('|'):
   tables+=1;assert e.count('|')==z.count('|'),(key,i,'table cells')
  correction=corrections.get(f'{key}#{i}')
  if correction:assert correction['source']==e and correction['translation']==z and correction['reason']
  else:
   nums=lambda t:collections.Counter(re.findall(r'(?<![A-Za-z_])\d+(?:[,.]\d+)*(?:%)?',t))
   assert nums(e)==nums(z),(key,i,'numeric values')
  # Links resolve as logical page IDs; translated paths retain the same targets.
  for link in re.findall(r'\]\(([^)]*\.md)(?:#[^)]*)?\)',e):
   if ':' not in link and not link.startswith('/'):
    target=(pathlib.PurePosixPath(key).parent/link).as_posix()
    import posixpath
    assert posixpath.normpath(target) in src,(key,link,'missing logical page')
 for i,e in build.segments(en):
  z=b[i]
  if e==z:unchanged.append({'page':key,'line':i,'text':z})
  visible=z
  if i in lua_lines:
   visible=z[lua_lines[i]+2:]
   visible=re.sub(r'"[^"\n]*"|[a-z_]+:[a-z0-9_./*-]+','',visible)
   # Exact debug/output notation, not explanatory prose.
   if key=='nodeworks/lua-api/network.md' and i in [390,392]:visible=''
  v=re.sub(r'<[^>]+>|`[^`]+`|\]\([^)]*\)','',visible)
  v=re.sub(r'^\s*title:\s*','',v)
  v=re.sub(r'(?<![A-Za-z0-9_])[a-z][a-z0-9_]*:[a-z0-9_./-]+','',v)
  for phrase in sorted(allow,key=len,reverse=True):v=re.sub(r'(?<![A-Za-z])'+re.escape(phrase)+r'(?![A-Za-z])','',v)
  words=re.findall(r'[A-Za-z]+',v)
  if words:latin.append({'page':key,'line':i,'words':words,'text':z})
anchor_links=0
for key,en in src.items():
 if not key.startswith('nodeworks/'):continue
 for link in re.findall(r'\]\(([^)]*)\)',en):
  if '://' in link or '#' not in link:continue
  page,fragment=link.split('#',1)
  dest=posixpath.normpath(posixpath.join(posixpath.dirname(key),page)) if page else key
  assert dest in src,(key,link,'anchor page missing')
  names={html.unescape(x) for x in re.findall(r'<a name="([^"]+)" />',build.target(dest).read_text())}
  assert fragment in names or fragment.lower() in names,(key,link,'anchor not resolved')
  anchor_links+=1
assert not latin,latin
# Only names and voltage/unit tables may remain exactly equal to English.
for u in unchanged:
 if u['page'].startswith('nodeworks/'):continue # Reviewed by per-line Latin and Lua-code checks above.
 plain=re.sub(r'<[^>]+>|^\s*title:\s*','',u['text'])
 for phrase in sorted(allow,key=len,reverse=True):plain=re.sub(r'(?<![A-Za-z])'+re.escape(phrase)+r'(?![A-Za-z])','',plain)
 assert not re.search('[A-Za-z]',plain),(u,'unreviewed unchanged text',plain)
extras=json.loads((PACK/'assets/ftbic/lang/zh_cn.json').read_text());orig=json.loads((BASE/'extra_language_sources.json').read_text())
assert extras.keys()==orig.keys()
with zipfile.ZipFile(next((ROOT/'.minecraft/mods').glob('ftb-industrial-contraptions-*.jar'))) as jar:
 current_english=json.loads(jar.read('assets/ftbic/lang/en_us.json'))
for key,value in orig.items():assert current_english[key]==value,(key,'item/control English changed')
node_zh=json.loads((PACK/'assets/nodeworks/lang/zh_cn.json').read_text())
node_en=json.loads((BASE/'nodeworks_language_source.json').read_text())
with zipfile.ZipFile(next((ROOT/'.minecraft/mods').glob('nodeworks-*.jar'))) as jar:
 assert json.loads(jar.read('assets/nodeworks/lang/en_us.json'))==node_en
assert node_zh.keys()==node_en.keys() and len(node_zh)==111
for k,v in node_zh.items():assert re.findall(r'%(?:\d+\$)?[sdf]',v)==re.findall(r'%(?:\d+\$)?[sdf]',node_en[k]),(k,'Nodeworks placeholders')
selected=next(line for line in (ROOT/'.minecraft/options.txt').read_text().splitlines() if line.startswith('resourcePacks:'))
assert json.loads(selected.split(':',1)[1])[-1]=='file/FTB-Evolution-2-Manuals-zh_CN','Pack not selected last'

for k,v in extras.items():
 tokens=lambda s:re.findall(r'%%|%(?:\d+\$)?[sdif]',s)
 assert tokens(orig[k])==tokens(v),(k,'format placeholders')
 assert orig[k].count('\n')==v.count('\n'),(k,'line breaks')
for p in PACK.rglob('*'):
 if p.is_file() and p.suffix in {'.json','.md','.mcmeta'}:
  assert not re.search(r'[，。：；！？（）【】“”‘’、》《「」『』]',p.read_text()),(str(p),'Chinese punctuation')
 if p.is_file() and p.suffix=='.json':json.loads(p.read_text())
json.loads((PACK/'pack.mcmeta').read_text())
for book in ['power','crop_mutation','skills','hostile_networks']:
 p=f'.minecraft/kubejs/assets/ftb/guideme_guides/{book}.json'
 assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==json.loads((BASE/'entry_source_manifest.json').read_text())[p]
 before=json.loads((ROOT/p).read_text());after=json.loads((PACK/f'assets/ftb/guideme_guides/{book}.json').read_text())
 for parent,field in [(before['item_settings'],'display_name'),(before['item_settings']['tooltip_lines'],0)]:parent[field].pop('text');parent[field]['translate']=f"guide.ftb.{book}.{'name' if field=='display_name' else 'tooltip'}"
 assert before==after,(book,'entry semantics')
report={'status':'passed','manual_pages':164,'nodeworks_pages':75,'nodeworks_anchors_checked':anchors_checked,'nodeworks_anchor_links':anchor_links,'code_lines_preserved':code_lines,'pack_guides':23,'ftbic_pages':66,'segments':sum(len(list(build.segments(v))) for v in src.values()),'table_rows_checked':tables,'additional_ftbic_language_keys':len(extras),'additional_nodeworks_language_keys':111,'guide_title_tooltip_keys':8,'documented_correction_lines':len(corrections),'intentional_unchanged':unchanged,'unreviewed_latin':latin,'in_game_tested':False}
(BASE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['intentional_unchanged','unreviewed_latin']},ensure_ascii=False,indent=2))
