import json,zipfile,re,pathlib,collections,hashlib,difflib
ROOT=pathlib.Path(__file__).resolve().parents[3]; BASE=ROOT/'localization/cfpa_review/manuals'
p=json.loads((ROOT/'localization/reports/remaining-1.4.0-manuals.json').read_text()); units=[v for v in p['units'] if not v['covered_candidate'] and v['cfpa_best_status']!='none']
def read(path):return (ROOT/path).read_text().replace('\r\n','\n')
def current(v):return zipfile.ZipFile(v['source']).read(v['path']).decode().replace('\r\n','\n') if v['source'].endswith('.jar') else pathlib.Path(v['source']).read_text()
def get(d,s):
 for x in s.split('.'):d=d[int(x)] if isinstance(d,list) else d[x]
 return d
def fields(d,prefix=''):
 out=[]
 if isinstance(d,dict):
  for k,v in d.items():out+=fields(v, prefix+'.'+k if prefix else k)
 elif isinstance(d,list):
  for i,v in enumerate(d):out+=fields(v,prefix+'.'+str(i))
 elif isinstance(d,str):out.append((prefix,d))
 return out
PUNCT=str.maketrans({'，':', ', '。':'.', '：':': ', '；':'; ', '！':'!', '？':'?', '（':'(', '）':')', '“':'"','”':'"','‘':"'",'’':"'",'、':', ', '…':'...', '—':'-', '⸺':' - ', '《':'"','》':'"','【':'[','】':']'})
def punctuation(s):
 # Avoid components, code fences, inline code, URLs and Patchouli syntax.
 chunks=re.split(r'(```[\s\S]*?```|`[^`\n]+`|<[^>]+>|\$\([^)]*\)|https?://[^\s)]+)',s)
 return ''.join(x if i%2 else x.translate(PUNCT) for i,x in enumerate(chunks))
def tags(s):return re.findall(r'</?[A-Za-z][^>]*>',s)
def links(s):return re.findall(r'\]\(([^)]+)\)',s)
def front(s):
 m=re.match(r'^---\n(.*?)\n---',s,re.S);return m.group(0) if m else ''
def macros(s):return re.findall(r'\$\(([^)]*)\)',s)
def nums(s):return collections.Counter(re.findall(r'(?<![A-Za-z_])\d+(?:[.,]\d+)*',s))
def target(v):
 path=v['path']
 if v['format']=='Patchouli':return path.replace('/en_us/','/zh_cn/')
 if '/guides/' in path:return path.replace('/guide/','/guide/_zh_cn/')
 return path.replace('/ae2guide/','/ae2guide/_zh_cn/')
D=[]; problems=[]
for v in units:
 cs=sorted(v['cfpa_candidates'], key=lambda c:(c['status']!='exact_english',bool(c.get('pr')),c['version']!='1.21'))
 c=cs[0];src=current(v); old=read(c['english_path']);zh=read(c['path']); changes=[];reason=None
 if v['format']=='Patchouli':
  sd=json.loads(src);od=json.loads(old);zd=json.loads(zh);en=get(sd,v['field']);prev=get(od,v['field']);val=get(zd,v['field'])
  if en!=prev:
   matches=[(f,t) for f,t in fields(od) if t==en and f.split('.')[-1]==v['field'].split('.')[-1]]
   if matches:
    f,_=matches[0];val=get(zd,f);changes.append({'type':'field_mapping','from':f,'to':v['field'],'basis':'当前英文与旧字段英文完全一致'})
   elif v['namespace']=='modularrouters' and 'A Modular Router GUI' in en:changes.append({'type':'source_grammar','detail':'An→A 冠词修正, 含义未变'})
   elif v['namespace']=='productivebees' and v['path'].endswith('quarry.json'):
    val='会啃咬附近的石头, 圆石, 沙子, 沙砾, 泥土及类似方块, 并把所造访方块的副本带回蜂巢.$(br2)它只会生产造访过的方块, 因此请在蜂巢周围摆上希望生产的方块. 泥土地上的蜂巢只会生产泥土, 不会生产石头.';changes.append({'type':'mechanics_adaptation','detail':'当前采石蜂直接复制造访方块, 删除旧版碎片合成说明, 补充当前授粉源限制'})
   else:reason='原文正文不同, 无可确认的同义字段映射'
  if 'filter_nbt.json' in v['path']:val=val.replace('更多信息课参见','更多信息可参见')
  if v['namespace']=='modularrouters':val=val.replace('模块每游戏能够','模块每游戏刻能够')
  if v['namespace']=='productivebees':
   val=val.replace('喂食板','饲养板').replace('基因索引器','基因检索器').replace('敲打（右键点击）蜂箱或蜂箱','敲打（右键点击）蜂箱或蜂巢')
  if v['path'].endswith('filter_nbt.json'):val=val.replace('更多信息课参见','更多信息可参见')
  val=val.replace('对附近的一个一个','对附近的一个').replace('总是填充总是填充','总是填充').replace('既可以放置的方块数量','即可以放置的方块数量').replace('会时路由器刻来的更快','会使路由器运行得更快').replace('方向。/$(p)','方向。$(p)').replace('将会将沿地面将一个物品','会沿地面将一个物品')
  if v['namespace']=='laserio' and '$(l)' not in en and '$(l)' in val:
   val=val.replace('$(l)','').replace('$()','')
   changes.append({'type':'format_repair','detail':'移除 CFPA 额外引入的强调/重置宏, 与当前源控制码一致'})
  if v['namespace']=='modularrouters':
   before_macro_repair=val
   if '$(modr)' in en:
    val=val.replace('$(#228)模块化路由器$()','$(modr)')
   else:val=val.replace('$(#228)模块化路由器$()','模块化路由器')
   if v['path'].endswith('/intro/modules.json') and v['field']=='pages.5.text':
    val=val.replace('https://zh.minecraft.wiki/w/%E6%A0%87%E7%AD%BE','https://minecraft.gamepedia.com/Tag')
   if val!=before_macro_repair:changes.append({'type':'macro_repair','detail':'保留当前 modr 宏与原始外链; 不用硬编码颜色替代宏'})
  z=punctuation(val).replace('/$(', '/$ (')
  z=re.sub(r'\$\(t:([^)]*)\)',lambda m:'$(t:'+m[1].translate(PUNCT)+')',z)
  if z!=val:changes.append({'type':'punctuation','detail':'正文半角标点, 保留 Patchouli 控制码'})
  val=z
  if v['namespace']=='productivebees' and v['path'].endswith('/hive/coal.json') and v['field']=='pages.0.text':
   changes.append({'type':'source_correction','detail':'当前煤炭蜜蜂配方 bee_breeding/coal_bee.json 亲本为 magmatic 与 leafcutter_bee, CFPA 链接/名称与配方一致, 当前英文 Blazing/redstone 为旧错误. 保留 CFPA 正确亲本, 不改原文/配方.'})
  if v['namespace']=='modularrouters' and v['path'].endswith('/modules/breaker.json') and v['field']=='pages.0.text':
   changes.append({'type':'source_link_correction','detail':'当前 JAR 中不存在 router/item_router, 实际页面是 router/modular_router; 保留 CFPA 有效链接'})
  if v['namespace']=='modularrouters' and v['path'].endswith('/intro/modules.json') and v['field']=='pages.5.text':
   changes.append({'type':'external_link_restored','detail':'NBT Tag 链接恢复当前英文原始 URL, 避免改变链接目的地'})
  # Functional tokens must retain all destination/action IDs; style counts may differ legitimately.
  em=collections.Counter(x for x in macros(en) if ':' in x);zm=collections.Counter(x for x in macros(val) if ':' in x)
  if em!=zm:problems.append({'path':v['path'],'field':v['field'],'type':'patchouli_macros','en':dict(em),'zh':dict(zm)})
  row={**{k:v[k] for k in ('namespace','format','path','field')},'status':'rejected' if reason else 'accepted','reason':reason or ('当前有效英文与 CFPA 原文一致; 复核字段含义和控制码后复用' if en==prev else '核对当前英文, 按记录映射/适配已有 CFPA 译文'),'source':c,'chinese':val,'output_resource_path':target(v),'changes':changes,'english':en,'english_sha256':hashlib.sha256(en.encode()).hexdigest()}
 else:
  # Current English frontmatter is authoritative. Only visible navigation title is inherited.
  sf,of,zf=front(src),front(old),front(zh)
  if sf:
   title=re.search(r'(?m)^(\s*title:\s*)(.+)$',zf)
   nf=re.sub(r'(?m)^(\s*title:\s*)(.+)$',lambda m:m[1]+title[2] if title else m[0],sf)
   if zf:zh=nf+zh[len(zf):]
   if nf!=zf:changes.append({'type':'frontmatter','detail':'当前源导航/分类/item_ids, 只保留中文 title'})
  name=pathlib.PurePosixPath(v['path']).name
  if name=='quantum_crafter_terminal.md':reason='当前 JAR 整页已注释禁用, 不恢复旧版可见终端说明/组件'
  if v['namespace']=='ae2':
   if name=='ae2importexportcard-index.md':
    zh=zh.replace('<ItemImage id="ae2importexportcard:export_card" scale="2" />','<ItemImage id="ae2importexportcard:export_card" scale="2" />\n   <ItemImage id="ae2importexportcard:block_picker_card" scale="2" />',1)
    zh=zh.replace('输入卡和输出卡可通过玩家物品栏输入/输出物品。','输入卡, 输出卡和方块选取卡可通过玩家物品栏输入/输出物品。')
    zh+='\n## 方块选取卡\n\n<ItemImage id="ae2importexportcard:block_picker_card" scale="2" />\n\n方块选取卡可直接从网络中取出你正看着的方块. 对准方块并按下选取方块按键即可. 如果网络中存有对应的方块, 就会将其取出至你的物品栏.\n\n![方块选取卡](diagrams/block_picker_card.png)\n\n### 配方\n\n<RecipeFor id="ae2importexportcard:block_picker_card" />\n'
    changes.append({'type':'source_addition','detail':'补齐当前新增方块选取卡说明/图片/RecipeFor, 沿用当前源物品ID与按键行为'})
   zh=zh.replace('id="chest"','id="me_chest"').replace('id="ae2:chest"','id="ae2:me_chest"')
   if name=='export_bus.md':zh=zh.replace('，并给予设置输出顺序的功能','')
   if name in ['network_tool.md','facades.md']:
    zh=re.sub(r'<a href="facades.md">.*?</a>','<ItemLink id="facade" />',zh)
    zh=re.sub(r'<a href="network_tool.md">.*?</a>','<ItemLink id="network_tool" />',zh)
   if name=='sky_stone.md':
    zh=zh.replace('向上放置一个破坏面板','向上放置一个<ItemLink id="annihilation_plane" />')
  if v['namespace']=='advanced_ae' and name=='advanced_pattern_provider.md':zh=zh.replace('<ItemLink id="extendedae:ex_pattern_provider" />','扩展样板供应器(来自AE2扩展)')
  if v['namespace']=='extendedae':
   zh=zh.replace('处理样本','处理样板').replace('空白样本','空白样板')
   if name=='entro_budding.md':zh=zh.replace('破坏长成的恩特罗芽','破坏未长成的恩特罗芽');changes.append({'type':'meaning_correction','detail':'未长成芽才掉碎片, 修复 CFPA 漏译否定'})
   if name=='caner.md':
    zh=zh.replace('第一个槽位是需要装填的事物，第二个槽位则是需被装填的事物。','第一个槽位放入填充资源, 第二个槽位放入需要填充的容器.').replace('### 支持的附属：','## 支持的附属')
   if name=='tag_storage_bus.md':zh=zh.replace('\nc:raw_materials\n','\n`c:raw_materials/*`\n').replace('\nc:raw_materials/*\n','\n`c:raw_materials/*`\n').replace('\nc:ingots/* | c:gems/*\n','\n`c:ingots/* | c:gems/*`\n')
  if v['namespace']=='little_big_redstone':
   zh=zh.replace('<RecipeFor id="battery" />','<Recipe id="little_big_redstone:logic/battery" />').replace('计数器会取各输入的计算结果作为输出。信号值不会超出0到15的范围。','信号源始终输出设定的信号强度. 信号值不会超出0到15的范围.');changes.append({'type':'component_and_copy_error','detail':'RecipeFor→当前 Recipe ID; 修复原 PR 从计数器页复制的说明'})
  # Repair confirmed upstream translation issues before syntactic validation.
  if v['namespace']=='ae2':
   zh=zh.replace('模板供应器','样板供应器')
   if name=='energy.md':
    zh=zh.replace('8000AE。','每个方块8k AE。').replace('可存储200kAE，','可存储200k AE(相当于25个控制器方块)，').replace('可存储1.6MAE，','可存储1.6M AE(相当于8个能源元件)，')
   if name=='terminals.md':
    zh=zh.replace('搜索框接受正则表达式','搜索框接受正则表达式(*regex*)')
    zh=zh.replace('手持桶或其他流体容器右击可存入流体，以空流体容器左击终端内流体可将其取出','手持桶或其他流体容器右击可存入流体\n*   空手左击流体时, 若网络中有空桶, 即可取出一桶流体; 手持流体容器左击则将流体取出至容器中')
   if name=='sky_stone.md':zh=zh.replace('在世界高度上限向上放置破坏面板以获取陨石粉。','在世界高度上限向上放置<ItemLink id="annihilation_plane" />以获取<ItemLink id="sky_dust" />。')
   if name=='bucket-filler.md':zh=zh.replace('流体则使用成型面板放置','流体则使用<ItemLink id="formation_plane" />放置')
   if name=='quantum_bridge.md':
    zh=zh.replace('在周围放下8个此方块','在<ItemLink id="quantum_link" />周围放下8个此方块').replace('只有与<ItemLink id="quantum_ring" />相邻的4个量子桥','只有与<ItemLink id="quantum_link" />相邻的4个<ItemLink id="quantum_ring" />')
   if name=='facades.md':zh=re.sub(r'\[网络工具\]\(network_tool.md\)','<ItemLink id="network_tool" />',zh)
   if name=='network_tool.md':zh=re.sub(r'\[伪装板\]\(facades.md\)','<ItemLink id="facade" />',zh)
  if v['namespace']=='ae2':
   zh=re.sub(r'<a title="[^"]*">(.*?)</a>',r'\1',zh)
   if name=='channels.md':zh=zh.replace('/ae2 channelmode <模式>','/ae2 channelmode <mode>')
   if name=='subnetworks.md':zh=zh.replace('通过各种方块型设备与主网络保持连接','通过各种方块型设备与主网络保持[连接](../ae2-mechanics/me-network-connections.md)')
   if name=='pattern_provider.md':
    zh=zh.replace('样板供应器是自动合成系统','样板供应器是[自动合成](../ae2-mechanics/autocrafting.md)系统').replace('面板型样板供应器是[线缆子部件]','面板型样板供应器是[线缆子部件]').replace('面板型样板供应器是[线缆子部件](../ae2-mechanics/cable-subparts.md)','面板型样板供应器是[线缆子部件](../ae2-mechanics/cable-subparts.md)')
   if name=='vibration_chamber.md':
    for cfg in ['baseEnergyPerFuelTick','minEnergyPerGameTick','maxEnergyPerGameTick']:zh=zh.replace(cfg,'`'+cfg+'`')
    zh=zh.replace('.minecraft/config/ae2/common.json','`.minecraft\\`/config/ae2/common.json')
   if name=='crystal_resonance_generator.md':zh=zh.replace('**发电速率: **','**发电速率:** ')
   if name=='autocrafting.md':zh=zh.replace('**重要: **','**重要:** ')
  # Final semantic and navigation audit against current 1.4.0 sources.
  if v['namespace']=='ae2':
   if name=='crafting_cpu_multiblock.md':
    zh=zh.replace('右击合成CPU会打开', '每个合成CPU只能处理1个请求或任务. 因此, 若想同时请求合成运算处理器与256个平滑石, 就需要2个合成CPU多方块结构.\n\n它们可设置为接受玩家请求, 自动化系统请求(输出总线与接口), 或两者均接受.\n\n右击合成CPU会打开')
    changes.append({'type':'omission_repair','detail':'补齐当前英文的单CPU单任务/并发示例及玩家与自动化请求段落'})
   if name=='mysterious_cube.md':
    zh=zh.replace('<RecipeFor id="not_so_mysterious_cube" />','虽然无法制造神秘方块, 但可以制造它的复制翻版: 没那么神秘的方块.\n\n<RecipeFor id="not_so_mysterious_cube" />')
    changes.append({'type':'omission_repair','detail':'恢复配方小节的不可合成原版与可合成复制品说明'})
   if name=='pattern_provider.md':
    zh=zh.replace('普通、方向、面板。','普通, 方向, 面板/[子部件](../ae2-mechanics/cable-subparts.md).')
    zh=zh.replace('阻挡模式下此功能才可正常运作','此功能也能正确配合阻挡模式运作')
    changes.append({'type':'link_and_meaning_repair','detail':'恢复变种段落的子部件链接; works correctly with 不表示仅阻挡模式才能运作'})
   if name=='autocrafting.md':zh=zh.replace('- <ItemLink id="pattern_provider" />\n','- 负责输出材料的<ItemLink id="pattern_provider" />\n')
   if name=='export_bus.md':changes.append({'type':'source_recipe_correction','detail':'当前 export_bus 页末尾误引用 import_bus 配方; 保留 CFPA export_bus 配方, 与本页方块一致'})
   if name=='channels.md':
    zh=zh.replace('带有8台设备和96个节点','带有8台设备和超过96个节点').replace('实际能减少能量消耗','实际上可能减少能量消耗')
    changes.append({'type':'source_numeric_correction','detail':'x3 行致密线缆 32×3=96, 保留 CFPA 96 修正英文92; 修复正文 over 96 和 might 的限定含义'})
   if name=='singularities.md':zh=zh.replace('<ItemLink id="ender_dust" />和','<ItemLink id="ender_dust" />\\\n和')
  if v['namespace']=='ae2wtlib' and name=='wireless_crafting_terminal.md':
   zh=zh.replace('装入<ItemLink id="ae2wtlib:magnet_card" />','  \n装入<ItemLink id="ae2wtlib:magnet_card" />')
  # Canonical source spans are normalized before comparison below. Existing source anchors
  # remain intact; generated English heading aliases make translated headings linkable.
  # Tooltip macros are visible prose, while embedded config names stay unchanged.
  # Relative link abbreviations in CFPA resolve to the same page; restore canonical source spelling.
  def resolve_link(dest):
   from posixpath import normpath,dirname
   if ':' in dest or dest.startswith('#'):return dest
   page,sep,anchor=dest.partition('#')
   return normpath(dirname(v['path'])+'/'+page)+('#'+anchor if sep else '')
  for link in links(zh):
   for desired in links(src):
    if resolve_link(link)==resolve_link(desired) and link!=desired:zh=zh.replace(']('+link+')',']('+desired+')')
  # Preserve translated heading anchors in incoming CFPA links via explicit original-language anchors.
  source_heads=re.findall(r'(?m)^#{1,6} +(.+)$',src)
  zh_heads=re.findall(r'(?m)^#{1,6} +(.+)$',zh)
  if len(source_heads)==len(zh_heads):
   hindex=[0];anchor_counts=collections.Counter()
   def anchor_heading(m):
    heading=source_heads[hindex[0]];hindex[0]+=1
    slug=re.sub(r'[^\w\s-]','',re.sub(r'<[^>]+>','',heading)).strip().lower().replace(' ','-')
    n=anchor_counts[slug];anchor_counts[slug]+=1
    return '<a name="'+slug+('-'+str(n) if n else '')+'"></a>\n\n'+m[0]
   zh=re.sub(r'(?m)^#{1,6} +.+$',anchor_heading,zh)
  for original,translated in [('crafting-storage','合成存储器'),('dense-cable','致密线缆'),('channel-routing','频道寻路'),('storage-priority','存储优先级'),('providing-to-multiple-places','向多处提供材料'),('pattern-encoding-terminal','样板编码终端'),('special-interactions','特殊交互'),('smart-cable','智能线缆')]:
   zh=zh.replace('#'+translated+')','#'+original+')')
  val=punctuation(zh)
  val=val.replace('**发电速率: **','**发电速率:** ').replace('**重要: **','**重要:** ')
  if val!=zh:changes.append({'type':'punctuation','detail':'仅文本半角化, 保留 JSX/代码/URL'})
  if src.rstrip()!=old.rstrip():changes.append({'type':'source_delta','detail':'当前英文差异见 manuals/diff-index.json; 英文语法/大小写润色不重译, 实质变化按本记录处理'})
  if collections.Counter(tags(re.sub(r'<a name="[^"]*"></a>','',src)))!=collections.Counter(tags(re.sub(r'<a name="[^"]*"></a>','',val))):problems.append({'path':v['path'],'type':'tags','en':tags(src),'zh':tags(val)})
  if collections.Counter(resolve_link(x) for x in links(src))!=collections.Counter(resolve_link(x) for x in links(val)):problems.append({'path':v['path'],'type':'links','en':links(src),'zh':links(val)})
  file=BASE/'files'/target(v);file.parent.mkdir(parents=True,exist_ok=True)
  if not reason:file.write_text(val)
  elif file.exists():file.unlink()
  row={**{k:v[k] for k in ('namespace','format','path','field')},'status':'rejected' if reason else 'accepted','reason':reason or '逐页核对 CFPA 译文及当前源差异, 复用同义正文并保留当前导航/资源 ID; 结构异常另有明确修复记录','source':c,'file':str(file.relative_to(ROOT)),'output_resource_path':target(v),'changes':changes,'english_sha256':hashlib.sha256(src.encode()).hexdigest()}
 if c.get('pr'):
  row['source']['review_status']='local_reviewed_with_cached_discussion'
  row['source']['discussion_evidence']='localization/cfpa_review/pr-discussions.json#'+str(c['pr'])
  row['changes'].append({'type':'pr_discussion_review','detail':('缓存只有自动检查信息, 未发现人工意见; 电池页复制计数器段落已修复' if c['pr']==5997 else '已检查缓存人工审查, 手册措辞建议涉及其他页面, 本条 draconic 页未发现直接意见; 不视为上游批准')})
 row['validation_exceptions']=[]
 if v['format']=='Patchouli':
  if v['path'].endswith('/sensormode.json') and v['field']=='pages.4.text':row['validation_exceptions'].append({'error':'numbers','reason':'1 item 译为单个物品, 另一个 Only 1 sensor card 仍保留数字1, 数量等价'})
  if v['path'].endswith('/hives/nests.json') and v['field']=='pages.0.text':row['validation_exceptions'].append({'error':'numbers','reason':'1 solitary bee 译为一只独居蜜蜂, 数量等价'})
  if v['path'].endswith('/modules/breaker.json') and v['field']=='pages.0.text':
   row['validation_exceptions'] += [{'error':e,'reason':'JAR 中 router/item_router 页面不存在, 修复为实际存在的 router/modular_router'} for e in ['Patchouli controls','resource IDs']]
  if v['path'].endswith('/router/modular_router.json') and v['field']=='pages.6.text':row['validation_exceptions'].append({'error':'Patchouli controls','reason':'仅 $(t:) 悬停可见正文汉化; ecoTimeout/lowPowerTickRate 配置键及其他宏完整保留'})
  if v['path'].endswith('/hive/coal.json') and v['field']=='pages.0.text':
   row['validation_exceptions'] += [{'error':e,'reason':'当前 JAR data/productivebees/recipe/bee_breeding/coal_bee.json 亲本为 magmatic+leafcutter_bee, 修正英文 Blazing/redstone 错误'} for e in ['Patchouli controls','resource IDs']]
 row['source']={**row['source'],'cfpa_commit':p['cfpa_commit'],'target_pack_version':p['target_version'],'target_source':v['source']};D.append(row)
(BASE/'structural-problems.json').write_text(json.dumps(problems,ensure_ascii=False,indent=2)+'\n')
(ROOT/'localization/cfpa_review/decisions/manuals.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print(collections.Counter((d['format'],d['status']) for d in D),'problems',len(problems))
for x in problems:print(x['path'],x.get('field',''),x['type'])
