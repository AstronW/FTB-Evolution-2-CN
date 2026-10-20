import pathlib,json,zipfile,re,collections,hashlib
from reviewed_cfpa_overlay import load_verified_review
R=pathlib.Path(__file__).resolve().parent.parent; MC=pathlib.Path(json.loads((R/'project.json').read_text())['target_instance'])
resources={}; errors=[]; langs=set(); jar_count=0
for jar in sorted((MC/'mods').glob('*.jar')):
 jar_count+=1
 try:
  with zipfile.ZipFile(jar) as z:
   for n in z.namelist():
    if n.startswith(('assets/','data/')) and n.endswith(('.md','.mdx','.txt','.json')):
     if n.endswith('/lang/en_us.json'):
      try:langs.update(json.loads(z.read(n)))
      except Exception:pass
     if n.endswith(('.md','.mdx')) or '/patchouli_books/' in n or '/lang/bestiary/' in n:
      resources[n]=(z.read(n).decode('utf-8-sig',errors='replace'),str(jar))
 except Exception as e:errors.append(str(e))
for kind in ('assets','data'):
 for p in (MC/'kubejs'/kind).rglob('*'):
  if p.is_file() and p.suffix in ('.md','.mdx','.txt','.json'):
   n=kind+'/'+p.relative_to(MC/'kubejs'/kind).as_posix()
   if p.suffix in ('.md','.mdx') or '/patchouli_books/' in n or '/lang/bestiary/' in n: resources[n]=(p.read_text(),str(p))
# Only book-player prose paths. Skip developer/readme/license docs, code help.
def isenglish(n):return not re.search(r'/(?:_?[a-z]{2}_[a-z]{2})(?:/|_)',n) and '/translated/' not in n
def english_path(n):
 n=re.sub(r'/translated/zh_cn/','/',n)
 n=n.replace('/_zh_cn/','/').replace('/zh_cn/','/en_us/').replace('/zh_cn_0/','/en_us_0/')
 return n

def zhpaths(n):
 if '/en_us/' in n:return [n.replace('/en_us/','/zh_cn/')]
 if '/en_us_0/' in n:return [n.replace('/en_us_0/','/zh_cn_0/')]
 if '/oracle_index/books/' in n:
  parts=n.split('/');return ['/'.join(parts[:4])+'/translated/zh_cn/'+'/'.join(parts[4:])]
 return [n[:m.start()]+'/_zh_cn'+n[m.start():] for m in re.finditer('/',n) if m.start()>len(n.split('/')[0]+'/'+n.split('/')[1])]
CJK=re.compile('[\u3400-\u9fff]')
def words(s):
 s=re.sub(r'```.*?```',' ',s,flags=re.S);s=re.sub(r'<[^>]*>|\$\([^)]*\)|\]\([^)]*\)|[a-z_]+:[a-z0-9_./-]+',' ',s)
 return len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*",s))
language_references=[]
visible={'name','description','text','title','subtitle','landing_text','caption'}
def fields(a,loc=()):
 out={}
 if isinstance(a,dict):
  for k,v in a.items():
   if k in visible and isinstance(v,str) and v in langs:language_references.append({'field':'.'.join(map(str,loc+(k,))),'language_key':v})
   elif k in visible and isinstance(v,str) and re.search('[A-Za-z]',v):out[loc+(k,)]=v
   elif isinstance(v,(dict,list)):out.update(fields(v,loc+(k,)))
 elif isinstance(a,list):
  for i,v in enumerate(a):out.update(fields(v,loc+(i,)))
 return out

def get(a,path):
 try:
  for k in path:a=a[k]
  return a
 except (KeyError,IndexError,TypeError):return ''
cache={}
def parse(text,path):
 try:return json.loads(text)
 except Exception as e:
  if path not in cache:errors.append({'path':path,'error':str(e)});cache[path]=1
  return {}
# CFPA full-version path index, retaining exact provenance.
cfindex=collections.defaultdict(list); cf_files=0
for p in (R/'CFPA/projects/assets').rglob('*'):
 if not p.is_file() or not (p.suffix in ('.md','.mdx','.txt') or '/patchouli_books/' in str(p) and p.suffix=='.json'):continue
 rel=p.relative_to(R/'CFPA/projects/assets').parts
 if len(rel)<4:continue
 cp='assets/'+'/'.join(rel[2:])
 if not ('zh_cn' in cp):continue
 en=english_path(cp);text=p.read_text(errors='replace')
 if not CJK.search(text):continue
 # Derive counterpart in same CFPA source-version directory.
 ep=p
 for token,replacement in (('/translated/zh_cn/','/'),('/_zh_cn/','/'),('/zh_cn/','/en_us/'),('/zh_cn_0/','/en_us_0/')):
  ep=pathlib.Path(str(ep).replace(token,replacement))
 et=ep.read_text(errors='replace') if ep.is_file() else None
 cfindex[en].append({'path':str(p.relative_to(R)),'version':rel[1],'text':text,'english':et,'english_path':str(ep.relative_to(R)) if ep.is_file() else None});cf_files+=1
# Audited open PR head snapshots. Fallback to base English only when unchanged-file evidence and matching base commit exist.
prdir=R/'localization/reports/cfpa-pr-audit'
prmeta=json.loads((prdir/'file-cache-index.json').read_text()) if (prdir/'file-cache-index.json').exists() else []
prlookup={(x['number'],x['path']):x for x in prmeta}
prchanged={x['number']:set(x['files']) for x in json.loads((prdir/'relevant-pr-index.json').read_text())} if (prdir/'relevant-pr-index.json').exists() else {}
prdocs=0
for item in prmeta:
 pp=item['path']
 if item['status']!='ok' or '/zh_cn' not in pp and '/_zh_cn/' not in pp:continue
 if not (pp.endswith(('.md','.mdx','.txt')) or '/patchouli_books/' in pp):continue
 if pp.startswith('projects/assets/'):
  rel=pp.removeprefix('projects/assets/').split('/')
 else:
  legacy=re.match(r'projects/([^/]+)/assets/([^/]+)/(.*)',pp)
  if not legacy:continue
  rel=[legacy[2],legacy[1],*legacy[3].split('/')]
 if len(rel)<4:continue
 cp='assets/'+'/'.join(rel[2:]);en=english_path(cp)
 text=(prdir/item['cache_file']).read_text(errors='replace')
 if not CJK.search(text):continue
 ep=english_path(pp);ei=prlookup.get((item['number'],ep));et=None;es=None
 if ei and ei['status']=='ok':et=(prdir/ei['cache_file']).read_text(errors='replace');es=str(prdir.relative_to(R)/ei['cache_file'])
 elif ep not in prchanged.get(item['number'],set()) and item['base_sha']==json.loads((R/'project.json').read_text())['cfpa']['commit'] and (R/'CFPA'/ep).is_file():
  et=(R/'CFPA'/ep).read_text(errors='replace');es='CFPA/'+ep
 cfindex[en].append({'path':str(prdir.relative_to(R)/item['cache_file']),'version':rel[1],'text':text,'english':et,'english_path':es,'pr':item['number'],'author':item['author'],'head_sha':item['head_sha'],'repo_path':pp,'review_status':'not_reviewed_for_adoption'})
 prdocs+=1

manifest=json.loads((R/'localization/manuals/source_manifest.json').read_text())
project={}
for key,sha in manifest.items():
 ns,rel=key.split('/',1);root={'ftb':'guides/ftb','ftbic':'ftbic','nodeworks':'nodeworksguide'}[ns]
 n='assets/'+ns+'/'+root+'/'+rel
 project[n]=(key,sha)
reviewed_language,reviewed_manual=load_verified_review()
reviewed_fields={(d['path'],d.get('field')):d for d in reviewed_manual if d['status']=='accepted' and d['format']=='Patchouli'}
reviewed_excluded={d['path'] for d in reviewed_manual if d['status']=='rejected' and d.get('rejection_kind')=='out_of_scope'}
for d in reviewed_manual:
 if d['status']=='accepted' and d['format']!='Patchouli':project[d['path']]=('cfpa_review/'+d['path'],d['english_sha256'])
scope=json.loads((R/'localization/language_scope.json').read_text())
def excluded(ns):return ns in scope['excluded_namespaces'] or any(ns.startswith(x) for x in scope['excluded_namespace_prefixes'])
units=[]; ignored=[];projectverification=[]; pending=[]
for n,(text,source) in sorted(resources.items()):
 ns=n.split('/')[1];group=n.split('/')[3] if '/oracle_index/books/' in n else ns
 if n in reviewed_excluded:ignored.append(n);continue
 if n.startswith('assets/oracle_index/books/oracle-index/docs/developer/') or n in {'assets/enderio/patchouli_books/guide/en_us/categories/test_category.json','assets/enderio/patchouli_books/guide/en_us/entries/test_entry.json'}:
  ignored.append(n);continue
 if n.endswith(('.md','.mdx')):
  if not isenglish(n):continue
  if n.endswith(('credits_and_copyright.md','00_readme.md','readme.md','README.md')) or '/lua/' in n or n.startswith('data/replication/recipe/'):
   ignored.append(n);continue
  fmt='Markdown/MDX';items={():text}
 elif '/patchouli_books/' in n and '/en_us/' in n and n.endswith('.json'):
  fmt='Patchouli';before_refs=len(language_references);items=fields(parse(text,n))
  for ref in language_references[before_refs:]:ref.update({'path':n,'namespace':ns,'source':source,'excluded_scope':excluded(ns)})
 elif re.search(r'/lang/bestiary/en_us_0/.*\.txt$',n):fmt='Bestiary TXT';items={():text}
 else:continue
 if excluded(ns) or ns in {'modonomicon','cyclopscore'}:ignored.append(n);continue
 # Building Gadgets is explicitly an architectural construction utility; report separately for parent decision.
 if ns=='buildinggadgets2':
  pending.append({'path':n,'reason':'Building Gadgets construction/copy/paste utility; pending scope decision, not included in main totals','fields':len(items),'words':sum(words(x) for x in items.values())});continue
 zpaths=[p for p in zhpaths(n) if p in resources]
 zhtext=resources[zpaths[-1]][0] if zpaths else ''
 zhobj=parse(zhtext,zpaths[-1]) if fmt=='Patchouli' and zhtext else {}
 proj_state='none'
 if n in project:
  key,sha=project[n];canonical=text.replace('\r\n','\n').replace('\r','\n') if key.startswith('cfpa_review/') else text;current=hashlib.sha256(canonical.encode()).hexdigest();proj_state='unchanged' if current==sha else 'changed'
  projectverification.append({'key':key,'current_path':n,'source':source,'expected_sha256':sha,'current_sha256':current,'status':proj_state})
 document_project_state=proj_state
 for loc,en in items.items():
  proj_state=document_project_state
  if not re.search('[A-Za-z]',en):continue
  official=get(zhobj,loc) if fmt=='Patchouli' else zhtext
  official_ok=isinstance(official,str) and bool(CJK.search(official))
  candidates=[]
  lookup_paths=[n]
  if '/guides/'+ns+'/guide/' in n: lookup_paths.append(n.replace('/guides/'+ns+'/guide/','/guide/'))
  for cand in [c for cp in lookup_paths for c in cfindex.get(cp,[])]:
   zh=get(parse(cand['text'],cand['path']),loc) if fmt=='Patchouli' else cand['text']
   if not isinstance(zh,str) or not CJK.search(zh):continue
   if cand['english'] is None:state='no_english_source'
   else:
    old=get(parse(cand['english'],cand['english_path']),loc) if fmt=='Patchouli' else cand['english']
    state='exact_english' if old==en else 'changed_english'
   candidates.append({'path':cand['path'],'version':cand['version'],'english_path':cand['english_path'],'status':state,**{k:cand[k] for k in ('pr','author','head_sha','repo_path','review_status') if k in cand}})
  states={x['status'] for x in candidates}
  candidate_state='exact_english' if 'exact_english' in states else 'no_english_source' if 'no_english_source' in states else 'changed_english' if 'changed_english' in states else 'none'
  field_review=reviewed_fields.get((n,'.'.join(map(str,loc))))
  if field_review and field_review['english']==en and hashlib.sha256(en.encode()).hexdigest()==field_review['english_sha256']:proj_state='unchanged'
  covered=proj_state=='unchanged' or official_ok
  units.append({'group':group,'namespace':ns,'format':fmt,'path':n,'field':'.'.join(map(str,loc)) if loc else None,'source':source,'english_words_approx':words(en),'official_cjk_candidate':official_ok,'official_path':zpaths[-1] if official_ok else None,'project_status':proj_state,'covered_candidate':covered,'cfpa_best_status':candidate_state,'cfpa_candidates':candidates})
summary=[]
for group,fmt in sorted({(u['group'],u['format']) for u in units}):
 us=[u for u in units if u['group']==group and u['format']==fmt];missing=[u for u in us if not u['covered_candidate']]
 row={'group':group,'format':fmt,'documents':len({u['path'] for u in us}),'visible_fields':len(us) if fmt=='Patchouli' else None,'units':len(us),'unit_type':'visible_JSON_fields' if fmt=='Patchouli' else 'documents','total_words_approx':sum(u['english_words_approx'] for u in us),'official_candidate_units':sum(u['official_cjk_candidate'] for u in us),'project_unchanged_units':sum(u['project_status']=='unchanged' for u in us),'uncovered_before_CFPA':len(missing),'uncovered_before_CFPA_words':sum(u['english_words_approx'] for u in missing)}
 for status in ('exact_english','no_english_source','changed_english','none'):
  subset=[u for u in missing if u['cfpa_best_status']==status];row['cfpa_'+status+'_units']=len(subset);row['cfpa_'+status+'_words']=sum(u['english_words_approx'] for u in subset)
 summary.append(row)
out={'target_instance':str(MC),'target_version':'1.4.0','jar_count':jar_count,'pr_document_candidates':prdocs,'cfpa_commit':json.loads((R/'project.json').read_text())['cfpa']['commit'],'method':'Read-only scan of enabled top-level JAR assets/data plus KubeJS same-path overlays. JAR path collision priority is deterministic filename order, not runtime evidence. No external or selected resource pack counted. CFPA all local versions, same namespace/document relative path; additionally GuideME /guides/{namespace}/guide/ to legacy /guide/ relocation candidate map. Exact comparison is full source document for Markdown/TXT, individual visible field for Patchouli; renamed paths not automatically inferred. Chinese presence is a candidate, not completeness proof. Documents and JSON fields are separate units. Language-backed manual keys are handled separately. Approximate words strip markup and code blocks. All candidates require term/context/format/license review.','language_key_references':language_references,'project_source_validation':projectverification,'project_pages_manifest':len(project),'project_pages_found':len(projectverification),'summaries':summary,'units':units,'pending_building_gadgets_exclusion':pending,'ignored_paths':ignored,'errors':errors}
p=R/'localization/reports/remaining-1.4.0-manuals.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
md=['# 1.4.0 手册文档剩余量静态盘点','','重跑: 在项目根目录运行 `python localization/assess_1_4_manuals.py`.','','此报告不含 lang/*.json 中承载的手册正文; 这些语言键由总盘点另计. Markdown/MDX 与 TXT 按文档计, Patchouli 按可见 JSON 字段计, 不得相加称为页面数.','','输入见 [project.json](../../project.json)、[手册源清单](../manuals/source_manifest.json)、[范围名单](../language_scope.json). 使用当前实例 '+str(MC)+' 的 '+str(jar_count)+' 个启用顶层 JAR 及 KubeJS 同路径覆盖; 未将旧实例或旧 CFPA 压缩包视作新版已覆盖. CFPA 扫描本地全部版本目录, 锁定提交 '+out['cfpa_commit']+'.','','## 项目已译页源文复核','',f'{len(project)} 页已有/审校复用清单中找到 {len(projectverification)} 页, 原文完全相同 {sum(x["status"]=="unchanged" for x in projectverification)} 页. 这证明既有译文可复用, 不代表已安装或游戏内验收.','','## 各组候选与缺口','','“已有”指项目源哈希不变或模组自带对应中文含汉字. “精确”指 CFPA 配套英文与当前原文逐字一致. “无英文”无法核验, “已变”必须适配. 所有 CFPA 项仅为待审候选.','','| 分组 | 单位 | 总量 | 已有候选 | 剩余 | CFPA 精确 | 无英文 | 已变 | 无候选 | 剩余英文词约数 |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for s in summary:md.append('| '+s['group']+' | '+s['unit_type']+' | '+' | '.join(str(x) for x in [s['units'],s['units']-s['uncovered_before_CFPA'],s['uncovered_before_CFPA'],s['cfpa_exact_english_units'],s['cfpa_no_english_source_units'],s['cfpa_changed_english_units'],s['cfpa_none_units'],s['uncovered_before_CFPA_words']])+' |')
md+=['','## 方法边界','','- 对照路径保留完整 CFPA 来源版本及文件, 详见同名 JSON. 不因版本不同跳过检索, 但仅额外尝试 GuideME /guides/{namespace}/guide/ 到旧 /guide/ 的目录迁移对应, 未做任意改名页面的语义映射. 精确候选也仍需术语与格式验收.','- 自带中文仅以对应字段/文档含汉字识别, 混合中文与未译英文可能仍有遗漏, 因此这是乐观候选覆盖而非完成声明.','- Building Gadgets 2 已由主线程依据当前模组元信息列入建筑工具排除名单, 不在主表中. 排除路径保留于 JSON 的 ignored_paths.','- 已通过 build-manifest 与 verification 双重校验的 CFPA 审校包按逐页/字段决定计入项目覆盖; 未启用不代表已安装到真实游戏. 其他额外资源包及运行时资源优先级未验收; 同名 JAR 路径冲突按文件名排序取值, 与实际加载顺序可能不同.','- 英文词数去掉代码块和常用标记, 只用于工作量近似; 不等于需逐词重新翻译.','- 手册重要性尚需结合任务引用与使用门槛划分, 本报告不擅自将所有手册列作关键手册.','- Patchouli 可见字段的值若精确命中当前启用 JAR 的英文语言键集合, 则作为语言键引用单列于 JSON 的 language_key_references, 不计入本表正文; 因此不会与语言键盘点重复. 当前引用集合不对未解析引用作猜测. JSON 的引用记录带当前文档路径、字段路径、语言键、来源和排除范围标记.','- 已排除 credits、readme、Computercraft 开发/终端帮助及 modonomicon/cyclopscore 框架示例资源; EnderIO 明确标注 Test Entry/Test Category 的占位示例及 Oracle Index 的 developer 开发文档也排除. Oracle Index 的 search/user_guide 两页为玩家使用指南, 保留.','- 未翻译任何正文, 未改动游戏、CFPA 或现有译文.','','解析错误数: '+str(len(errors))+'. 已纳入 file-cache-index.json 中固定 head SHA 的未合并 PR 文档候选; PR 编号、作者、提交及来源见 JSON. 未审查批准采用. 若 PR 未修改配套英文且基线 SHA 与本地 CFPA 一致, 允许以该基线英文核验; 否则无法核验即单列.']
totals=[]
for fmt in ('Markdown/MDX','Patchouli','Bestiary TXT'):
 ss=[r for r in summary if r['format']==fmt]
 vals={k:sum(r[k] for r in ss) for k in ('documents','units','uncovered_before_CFPA','uncovered_before_CFPA_words','cfpa_exact_english_units','cfpa_exact_english_words','cfpa_changed_english_units','cfpa_changed_english_words','cfpa_no_english_source_units','cfpa_no_english_source_words','cfpa_none_units','cfpa_none_words')}
 totals.append({'format':fmt,**vals})
out['totals_by_format']=totals
p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
md+=['','## 分格式汇总','','| 格式 | 文档总数 | 计量单位总数 | 原始剩余单位 | 原始剩余词数 | 精确 CFPA/PR 候选单位 | 精确候选词数 | 扣除精确候选后词数 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for t in totals:md.append('| '+t['format']+' | '+' | '.join(str(t[k]) for k in ('documents','units','uncovered_before_CFPA','uncovered_before_CFPA_words','cfpa_exact_english_units','cfpa_exact_english_words'))+' | '+str(t['uncovered_before_CFPA_words']-t['cfpa_exact_english_words'])+' |')
md+=['','以上扣除只用于估算新增翻译量, 精确候选仍需裁决、格式复核和合入. PR 不会因未合并而跳过, 本次发现对原始缺口直接相关的 PR 文档为 #6142 AE2 import/export card、#5196 AE2 storage cells 和 #5997 Little Big Redstone battery; 候选均在 JSON 标明英文核验结果.']

(R/'localization/reports/remaining-1.4.0-manuals.md').write_text('\n'.join(md)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2));print('project',len(projectverification),collections.Counter(x['status'] for x in projectverification));print('errors',errors[:4])
