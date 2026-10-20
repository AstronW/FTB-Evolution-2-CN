"""Apply reviewed 1.4.1 quest deltas while retaining immutable 1.4.0 inputs."""
from pathlib import Path
import difflib, collections, hashlib, json, shutil, sys, zipfile
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'localization'))
import quest_translation as q
BASE=Path(__file__).parent; BEFORE=BASE/'before'
GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def backup(p):
 dest=BEFORE/p.relative_to(ROOT)
 if p.is_file() and not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
def write(p,d):backup(p);dump(p,d)
assert json.loads((GAME/'instance.json').read_text())['version']=='1.4.1'
# Stable English strings are matched to their old resolved translations; changed
# paragraphs have explicit reviewed translations below, never guessed indexes.
changes={
 'Any Gun Modifier':'任意枪械改装件',
 '&3Keeping Cool':'&3保持冷却',
 "Every &aCrafting Storage&r and &aCo-Processor&r in a &eNodeworks&r CPU makes &bheat&r, and more of it when packed against other CPU parts. When your coolant can't keep up, the CPU slows down.":'&eNodeworks&r CPU 中的每个&a合成缓存&r和&a合成协处理器&r都会产生&b热量&r, 紧贴其他 CPU 部件时产热更多. 冷却能力不足时, CPU 就会减速.',
 '&aCoolants&r count as part of the CPU, so you can use them to link parts together. ':'&a冷却块&r也算 CPU 的一部分, 因此可以用来连接各个部件. ',
 'Any coolant touching a CPU block cools it, and each one gets a &bcluster bonus&r for every other coolant next to it. A solid wall of coolant works far better than single blocks spread around.':'冷却块会冷却与其接触的 CPU 方块, 每相邻一个其他冷却块, 它就会获得一份&b集群加成&r. 集中铺成一面墙, 效果远好于零散放置.',
 '&aCrafting Coolant&r: 1 cooling, +1 per neighboring coolant':'&a合成冷却块&r: 冷却能力为 1, 每相邻一个冷却块额外 +1',
 '&3Adamantite Coolant&r: 2 cooling, +2 per neighboring coolant':'&3精金冷却块&r: 冷却能力为 2, 每相邻一个冷却块额外 +2',
 '&dAeternium Coolant&r: 3 cooling, +3 per neighboring coolant':'&d永恒金属冷却块&r: 冷却能力为 3, 每相邻一个冷却块额外 +3',
 '&6Aurichalcum Coolant&r: 4 cooling, +4 per neighboring coolant':'&6奥利哈刚冷却块&r: 冷却能力为 4, 每相邻一个冷却块额外 +4',
 'A single layer of &3Adamantite Coolant&r against your CPU is enough to fully cool any part of it. Higher tiers do the same job with fewer blocks.':'在 CPU 旁铺一层&3精金冷却块&r, 就足以让其任意部件充分冷却. 更高级的冷却块能用更少的方块达到同样效果.',
 'Your mana pool grows by 50 with every magic level, so leveling is the long-term answer.':'每提升一个魔法等级, 魔力池就会增加 50, 因此升级才是长久之计.',
 'To remove an &5Enchantment&r, fill the &dPurifier&r with 3 buckets of blood, then right-click it with the item you want to disenchant and with a &cBlook&r. One random enchantment is moved onto the &cBlook&r, which becomes an &5Enchanted Book&r, and all 3 buckets are used up.':'要移除一项&5附魔&r, 先向&d净化器&r装入 3 桶血液, 再分别手持待祛魔的物品和&c血之书&r右击净化器. 物品上的一项随机附魔会转移到&c血之书&r上, 使其变为&5附魔书&r, 并消耗全部 3 桶血液.',
 "To remove a &cCurse&r, you only need 1 bucket of blood and the cursed item; no &cBlook&r is needed. Each curse level removed uses 1 bucket. Curses on the &4Vengeance Pickaxe&r can't be removed.":'要移除&c诅咒&r, 只需 1 桶血液和受诅咒的物品, 无需&c血之书&r. 每移除 1 级诅咒消耗 1 桶血液. &4复仇镐&r上的诅咒无法移除.',
 "Infuse an &cEnchanted Bullet Modifier&r on a Tier I Ara Vitae to make a &cBlood Bullet&r, then slot it into a gun. Each shot draws 50 EV from your network in place of a bullet, so the gun reloads even if you don't have bullets.":'在 I 级命血祭坛上灌注&c附魔子弹改装件&r, 制成&c气血子弹&r并装入枪械. 每发子弹消耗网络中的 50 EV, 替代实体弹药, 因此即使没有子弹也能装填枪械.',
 'When the network cannot pay, the gun falls back on whatever bullets you have to reload with.':'网络无法支付消耗时, 枪械会改用你持有的实体子弹装填.',
 'The higher the tier, the more area that it covers. This pack lets fake players use watering cans, so a &2Clicker&r from &eJust Dire Things&r can work one for you.':'等级越高, 覆盖范围越大. 本包不允许模拟玩家使用洒水壶, 因此&eJust Dire Things&r的&2点击器&r无法替你操作.',
}
changes.update({"A &aCrafting Core&r and a touching &2Crafting Buffer&r form the start of a crafting CPU. Connect the core to a Node so the network can use it.": "一个&a合成核心&r与相邻的&2合成缓存&r构成合成 CPU 的基础. 将核心连接到节点, 网络才能使用它.", "Add &2Crafting Coolant&r against the buffer before expanding. Buffers and co-processors generate heat, and insufficient cooling slows every craft. A starter buffer can be cooled by two coolant blocks.": "扩展前, 先在合成缓存旁放置&2合成冷却块&r. 合成缓存和合成协处理器都会发热, 冷却不足会拖慢所有合成. 入门合成缓存用两个冷却块就能冷却.", "&2Crafting Co-Processors&r add parallel crafts. Coolant blocks become stronger when touching other coolant blocks, but split their cooling between the hot blocks they touch. Keep heat sources spread out and coolant grouped together.": "&2合成协处理器&r可增加并行合成数量. 冷却块与其他冷却块相邻时效果更强, 但冷却能力会分摊给所有接触的发热方块. 应让热源分散, 冷却块集中.", "&2Crafting Substrate&r touching buffers or co-processors increases speed once cooling is covered.": "冷却足够后, 让&2合成基板&r接触合成缓存或合成协处理器, 可以进一步提高速度."})
records=[]
for source in sorted(q.SOURCE.rglob('*.json5')):
 backup(source);rel=source.relative_to(q.SOURCE);old=q.load_source(BEFORE/source.relative_to(ROOT));new=q.load_source(GAME/source.relative_to(ROOT/'.minecraft'))
 transpath=ROOT/'localization/translations'/rel.with_suffix('.json');backup(transpath)
 trans=json.loads((BEFORE/transpath.relative_to(ROOT)).read_text()) if (BEFORE/transpath.relative_to(ROOT)).exists() else {}
 oldsegs=q.segments(old);mapping={}
 terms=json.loads((ROOT/'localization/terms.json').read_text())
 for i,en in enumerate(oldsegs):
  zh=trans.get(str(i),terms.get(en));assert zh is not None,(rel,i,en)
  mapping.setdefault(en,set()).add(zh)
 # The upstream typo was already translated as prints. Keep its exact translation.
 for en in list(mapping):
  if 'ptinyd' in en:mapping[en.replace('ptinyd','prints')]=mapping[en]
 newsegs=q.segments(new)
 aligned={}
 for block in difflib.SequenceMatcher(a=oldsegs,b=newsegs,autojunk=False).get_matching_blocks():
  for offset in range(block.size):
   oi=block.a+offset;aligned[block.b+offset]=trans.get(str(oi),terms.get(oldsegs[oi]))
 out={}
 for i,en in enumerate(newsegs):
  if en in changes:zh=changes[en]
  elif i in aligned:zh=aligned[i]
  elif en in mapping and len(mapping[en])==1:zh=next(iter(mapping[en]))
  elif en in terms:zh=terms[en]
  else:raise AssertionError((rel,i,'Needs manual review',en,mapping.get(en)))
  out[str(i)]=zh
  if en not in mapping or zh not in mapping[en]:records.append({'file':str(rel),'segment':i,'source':en,'translation':zh})
 write(transpath,out)
 source.write_bytes((GAME/source.relative_to(ROOT/'.minecraft')).read_bytes())
# Refresh the work-copy structures from the new upstream without ever writing
# them to the game. These are inputs, not installation payloads.
base=GAME/'config/ftbquests/quests'
for p in base.rglob('*'):
 if p.is_file() and 'lang' not in p.relative_to(base).parts:
  dest=ROOT/'.minecraft'/p.relative_to(GAME);backup(dest);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
write(ROOT/'localization/source_manifest.json',{str(p.relative_to(q.SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(q.SOURCE.rglob('*.json5'))})
namespath=ROOT/'localization/quest_item_names.json';names=json.loads(namespath.read_text());jar=next((GAME/'mods').glob('ftb-evolution-companion-*.jar'))
with zipfile.ZipFile(jar) as z:en=json.loads(z.read(names['language_file']))
assert all(en[k]==v['en'] for k,v in names['entries'].items())
link=ROOT/'.minecraft/quest-inputs'/jar.name
if not link.exists():link.symlink_to(jar)
names['source_jar']=str(link.relative_to(ROOT));write(namespath,names)
extra=ROOT/'localization/quest_extra_labels.json';groups=json.loads(extra.read_text())
for group in groups:
 p=ROOT/group['source'];backup(p)
 if p.name=='ftb-en_us.json':raw=(GAME/'kubejs/assets/ftb/lang/en_us.json').read_bytes()
 else:
  with zipfile.ZipFile(next((GAME/'mods').glob('Replication-*.jar'))) as z:raw=z.read('assets/replication/lang/en_us.json')
 parsed=json.loads(raw);assert all(parsed[k]==v['en'] for k,v in group['entries'].items())
 p.write_bytes(raw);group['source_sha256']=hashlib.sha256(raw).hexdigest()
write(extra,groups)
dump(BASE/'quest-deltas.json',records)
print('Reviewed new/changed quest fragments:',len(records))
