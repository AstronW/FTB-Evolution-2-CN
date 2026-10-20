"""Build explicitly reviewed 1.4.1 language deltas and newly audited nested UI."""
from pathlib import Path
import collections,hashlib,io,json,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'localization'))
from punctuation import normalize
import ordinary_translation as o
GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
rows=json.loads((BASE/'new-language-candidates.json').read_text());mapping=json.loads((BASE/'new-language-translations.json').read_text())
extra=[('death.attack.ltxi.lightfrag','%1$s was shot by %2$s'),('death.attack.ltxi.railgun_turret',"%1$s was obliterated by %2$s's turret")]
jar=next((GAME/'mods').glob('ltxi-*.jar'))
for key,en in extra:rows.append({'namespace':'ltxi','key':key,'english':en,'source':str(jar),'path':'assets/ltxi/lang/en_us.json','candidates':[],'reason':'Official Chinese has stale argument or turret name; current source adaptation'})
# Review native JECharacters messages as well: remove a much stronger colloquial
# exclamation than the English source, preserving the actual file path.
all_observed=json.loads((ROOT/'localization/reports/update-1.4.1-assessment.json').read_text())['new_language_candidates']
for row in all_observed:
 if row['namespace']=='jecharacters' and row['key']!='jecharacters.chat.help':
  row['candidates']=[];row['reason']='Review native tone and retain source paths; ASCII punctuation in project override'
  rows.append(row)
# Legitimate names, key labels, format-only patterns and command grammar are
# explicit entries, never a catch-all escape for an untranslated sentence.
preserved={
 'sathlib':{'{%s}','(%s)','[%s]'},'ae2addonlib':{'%s / %s B'},
 'nautec':{'%s / %s','%s AP','%s mB/s'},
 'codedefinedgui':{'Code Defined GUI'},'trender':{'Trender'},
 'tinymultiblocklib':{'Tiny Multiblock Lib'},'kuma_api':{'Alt','Control','Shift','%s + %s'},
 'productivelib':{' - %s','   %s'},
 'jecharacters':{'/jech [profile] / [verbose true/false]'},
}
selected=collections.defaultdict(list);excluded=[];decisions=[]
for row in rows:
 ns=row['namespace'];en=row['english'];key=row['key']
 if ns in {'ftb','crystalix'}:
  excluded.append({'key':key,'namespace':ns,'reason':'Custom batch-005 owns this key' if ns=='ftb' else 'Decoration mod; preserve earlier translation only'});continue
 if key.startswith('enchantment.level.') and ns=='nautec':
  assert re.fullmatch('[IVXLCDM]+',en);zh=en;kind='Roman numeral enchantment level'
 elif en in mapping.get(ns,{}):zh=mapping[ns][en];kind='Current source reviewed manual translation'
 elif row['candidates']:
  assert ns=='productivelib',(ns,key)
  zh=normalize(row['candidates'][0]['chinese']);kind='Reviewed exact-English cross-version CFPA reuse'
  if key=='item.productivelib.upgrade_block':zh='升级: 方块';kind+='; adapt shared-library block scope'
 elif en in preserved.get(ns,set()):zh=en;kind='Reviewed name, format, key label or command syntax'
 else:raise AssertionError(('Unreviewed language entry',ns,key,en))
 row['translation']=zh;row['review_reason']=kind;selected[ns].append(row);decisions.append(row)
number=317
groups=collections.defaultdict(list)
for ns,entries in selected.items():
 for row in entries:groups[ns,row['source']].append(row)
for (ns,origin),entries in sorted(groups.items()):
 folder=o.WORK/f'batch-{number:03d}';number+=1;folder.mkdir(parents=True,exist_ok=True)
 origins={r['source'] for r in entries};assert len(origins)==1,(ns,origins)
 origin=next(iter(origins));parts=origin.split('!');jar=Path(parts[0]);manifest={'batch':folder.name.split('-')[1],'namespace':ns,'jar':str(Path('.minecraft/mods')/jar.name),'jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'language_path':entries[0]['path'],'target':f'.minecraft/kubejs/assets/{ns}/lang/zh_cn.json','include_keys':[r['key'] for r in entries],'context_overrides':{},'unchanged_values':list(dict.fromkeys(r['english'] for r in entries if not re.search('[\u3400-\u9fff]',r['translation']))),'target_pack_version':'1.4.1'}
 if len(parts)>1:
  raw=jar.read_bytes();layers=[]
  for part in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(part)
   layers.append({'path':part,'sha256':hashlib.sha256(raw).hexdigest()})
  manifest['nested_jars']=layers
 source=json.loads(o.language_source(manifest));wanted={r['key']:r for r in entries};source={k:v for k,v in source.items() if k in wanted}
 assert len(source)==len(entries)
 for k,v in source.items():assert wanted[k]['english']==v,(ns,k,'current source drift')
 vals=list(dict.fromkeys(source.values()));translations={}
 for r in entries:
  assert r['english'] not in translations or translations[r['english']]==r['translation'],(ns,r['key'])
  translations[r['english']]=r['translation']
 for name,data in [('manifest.json',manifest),('source-en_us.json',source),('source-values.json',vals),('source-review.json',entries)]:
  (folder/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (folder/'zh-values.tsv').write_text('\n'.join(str(i)+'\t'+translations[v].replace('\n','\\n') for i,v in enumerate(vals))+'\n')
 (folder/'README.md').write_text(f'# 第 {manifest["batch"]} 批: {ns} / 1.4.1\n\n当前选定 {len(entries)} 个键, 含新增源键与本轮首次纳入的嵌套依赖界面. 不将首次观察到的键都计为版本新增. 原文及逐项来源/审校理由见 source-review.json, 英文源与原始命令/格式保持. CFPA 来源固定为项目本地检出, 采用条目保留原版本与路径, 许可延用 THIRD_PARTY_NOTICES.md 的 CC BY-NC-SA 4.0. 未采用未核验 PR, 不声称已穷尽远端 PR.\n\n构建与检查: `python localization/ordinary_translation.py {folder.name} --build`, `python localization/ordinary_translation.py {folder.name}`. 未进行游戏内验收.\n')
 o.process(folder,True)
(BASE/'language-update-review.json').write_text(json.dumps({'translated_or_preserved':len(decisions),'namespaces':{ns:len(es) for ns,es in selected.items()},'excluded':excluded,'method':'Current native English plus reviewed exact-match CFPA/PR cache candidates; nested library entries are separately attributed, not all claimed as pack additions.','in_game_tested':False},ensure_ascii=False,indent=2)+'\n')
print('Built',len(groups),'batches,',len(decisions),'reviewed keys')
