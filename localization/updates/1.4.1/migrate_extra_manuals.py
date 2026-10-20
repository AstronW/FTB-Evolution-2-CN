"""Rebind reviewed manual sources and apply six Nautec incremental translations."""
from pathlib import Path
import difflib,hashlib,json,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[3];BASE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'localization'));import manual_extra_translation as m
GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
def backup(p):
 b=BASE/'before'/p.relative_to(ROOT)
 if p.exists() and not b.exists():b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,b)
def write(p,s):backup(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
changes={
 'deep_oceans.md':{38:'* <ItemLink id="budding_prismarine"/>生成在海床顶部. 留意它发出的微光.',49:'* 海晶母岩与海沟中一样, 生成在海床顶部.'},
 'eye_of_the_sea.md':{23:'如果约 1,600 格内(生物群系为 3,200 格内)没有匹配目标, 眼睛会留在手中, 并显示消息说明.',41:'| 海晶礁 | 最近的海晶礁生物群系, 是寻找<ItemLink id="budding_prismarine"/>的最佳地点 |',42:'| 深渊海沟 | 最近的深渊海沟生物群系 |',43:'| 荧光海林 | 最近的荧光海林生物群系 |',44:'| 海底热泉 | 最近的海底热泉生物群系 |',46:'新制作的眼睛默认寻找水晶晶洞, 每颗眼睛都会记住自己的目标. 你自行建造的传送门不会成为目标. 寻找生物群系时, 眼睛会飞向最近一片目标生物群系的边缘. 各类结构的内容见[结构](structures.md).'},
 'stronger_beams.md':{41:'| [搅拌机](nautec:laser_chemistry/mixer.md) | 10 AP | 增加每周期加工次数, 每 10 AP 加工一次, 最多 64 次; 超过 640 AP 后缩短周期 |',54:'| [渗透过滤器](nautec:laser_chemistry/osmosis_filter.md) | 无 | 每 40 AP 使产水量翻倍 |'},
 'utilities.md':{25:'扳手有四种模式. 潜行并右键点击空气可在它们之间切换; 提示框和快捷栏上方的消息会显示当前模式.',29:'* 连接: 点击两次即可让两个激光方块互相对准. 先右击发射光束的方块, 例如<ItemLink id="prismarine_laser_relay"/>, <ItemLink id="laser_junction"/>或<ItemLink id="aquatic_catalyst"/>, 将其存为起点. 再右击光束要到达的方块, 例如另一个中继器或机器. 扳手会转动起点, 让它朝第二个方块发射, 并转动第二个方块以接收起点的光束; 对转接器则改为开启对应的输出面或输入面. 两个方块必须在同一直线上, 且在光束射程内. 如有障碍物, 快捷栏上方会显示提示. 连接后保存的起点会清空, 可以继续下一次连接. 右击空气或不收发激光的方块也会清空起点; 已保存起点时, 提示框会显示其位置. 此模式操作机器时不会打开界面. 中继器从背面接收光束, 从正面发射, 因此将其向拐角后的下一处连接会使其转离原本接收的光束; 此时会显示警告. 需要转弯时应使用<ItemLink id="laser_junction"/>.'},
 'budding_prismarine.md':{23:'最容易找到它的地方是海晶礁, 大约每隔一个区块就有一些, 位于海床顶部和海晶石斑块中. 它也会生成在深渊海沟和荧光海林的海床顶部, 以及每个 Glow Grotto 的地面. 原版温暖海洋和深层温水海洋的海床顶部偶尔也会有一个. 在深渊海沟的幸运区域钓鱼也有机会将其作为宝藏钓上来. 用精准采集开采它, 然后放置到你想养殖它的地方.',25:'该方块会发出微光和零星光点, 可以留意海床上暗淡的亮光, 夜间最容易辨认. 要前往对应生物群系, 将<ItemLink id="eye_of_the_sea"/>设为海晶礁后抛出.'},
 'mixer.md':{21:'空手右击可打开界面. 它有四个原料槽, 一个输出槽, 一个输入储罐和一个输出储罐, 每个储罐可容纳 64,000 mB(64 桶, 可配置).',29:'工作时搅拌头会旋转. <ItemLink id="prism_monocle"/>显示输入功率, Jade 还会显示储罐, 混合进度和同时加工的次数.',64:'搅拌机需要 10 AP. 更强的光束会先增加同时加工的次数: 每 10 AP 增加一次, 每周期最多 64 次(可配置). 周期结束时, 实际加工数量取决于原料, 输入储罐和输出空间. 因此在 640 AP 下, 放入一组盐和 64,000 mB 水, 可在一个 5 秒周期内制成 64,000 mB 盐水.',66:'达到 64 次加工后, 更多 AP 会转而缩短周期: 速度为(光束 ÷ (加工次数 × 10))的平方根. 低于 640 AP 时, 位于两个 10 AP 档位之间的余量只会略微加速.',68:'| 光束 | 每周期加工次数 | 速度 |',69:'|---|---|---|',70:'| 10 AP | 1 | ×1(正常) |',71:'| 40 AP | 4 | ×1 |',72:'| 640 AP | 64 | ×1 |',73:'| 2,560 AP | 64 | ×2 |',74:'| 5,760 AP | 64 | ×3 |',75:'| 10,240 AP | 64 | ×4 |',77:'配方表中的时间指 ×1 速度下的单个周期.'}
}
before_manifest=BASE/'before'/m.MANIFEST.relative_to(ROOT)
manifest=json.loads((before_manifest if before_manifest.exists() else m.MANIFEST).read_text());records=[]
resource_index={}
for jar in sorted((GAME/'mods').glob('*.jar')):
 with zipfile.ZipFile(jar) as z:
  for name in z.namelist():
   if name in manifest['documents']:resource_index[name]=jar
for path,entry in manifest['documents'].items():
 oldsource=m.SOURCES/path;backup(oldsource)
 oldzh=m.TRANSLATIONS/path;backup(oldzh)
 origin=Path(entry['source'])
 if not origin.exists():
  assert path in resource_index,path
  origin=resource_index[path]
 if origin.suffix=='.jar':
  with zipfile.ZipFile(origin) as z:text=m.normalize(z.read(path).decode('utf-8-sig'))
 else:text=m.normalize(origin.read_text())
 previous=(BASE/'before'/oldsource.relative_to(ROOT)).read_text()
 if m.digest(text)!=entry['source_sha256']:
  assert Path(path).name in changes,path
  translated=(BASE/'before'/oldzh.relative_to(ROOT)).read_text().splitlines();a=previous.splitlines();b=text.splitlines();assert len(a)==len(translated)
  out={}
  for block in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_matching_blocks():
   for offset in range(block.size):out[block.b+offset]=translated[block.a+offset]
  out.update(changes[Path(path).name])
  for i,line in enumerate(b):
   if i not in out:assert not line.strip(),(path,i,line);out[i]=''
  write(oldzh,'\n'.join(out[i] for i in range(len(b)))+'\n')
  records.append({'page':path,'old_sha256':entry['source_sha256'],'new_sha256':m.digest(text),'translated_changed_lines':len(changes[Path(path).name])})
 write(oldsource,text);entry['source']=str(origin);entry['source_sha256']=m.digest(text);entry['english_words_approx']=m.word_count(text)
manifest['target_pack_version']='1.4.1';manifest['known_pages']=sorted(m.known_pages())
write(m.MANIFEST,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
write(BASE/'extra-manual-deltas.json',json.dumps(records,ensure_ascii=False,indent=2)+'\n')
