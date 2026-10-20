"""Reviewed Nodeworks 0.10.6 manual changes, preserving source line boundaries."""
from pathlib import Path
import hashlib,json,shutil,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'localization'))
import manual_translation as m
BASE=Path(__file__).parent

def write(path,data):
 backup=BASE/'before'/path.relative_to(ROOT)
 if path.exists() and not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,backup)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

pages=m.sources();records=[]
for key,text in pages.items():
 path=m.BASE/'translations'/Path(key).with_suffix('.json')
 if key not in {'nodeworks/items-blocks/recipe_sets.md','nodeworks/lua-api/card-handle.md'}:continue
 oldpath=BASE/'before'/path.relative_to(ROOT)
 old=json.loads((oldpath if oldpath.exists() else path).read_text());out={}
 for i,line in m.segments(text):
  index=i
  if key.endswith('recipe_sets.md') and i>=96:index=i-11
  if key.endswith('card-handle.md') and i>=374:index=i-42
  if (key.endswith('recipe_sets.md') and 85<=i<=94) or (key.endswith('card-handle.md') and 332<=i<=369):continue
  out[str(i)]=old[str(index)]
 if key.endswith('recipe_sets.md'):
  out.update({
   '85':'用空鼠标指针右击已填入产物的槽位, 可将其标为 **可选产物**',
   '86':'(以`?`标记显示). 适用于概率副产物, 例如磨粉机额外产出的',
   '87':'粉末. 合成任务只等待必定产出的物品. 可选产物出现后会直接',
   '88':'进入网络存储, 数量不超过设定值. 如果副产物是主产物的',
   '89':'额外一份, 同一刻内多产出的那份就会算作',
   '90':'副产物. CPU 不会为可选产物规划合成, 因此每个配方集',
   '91':'至少保留一个必定产出的物品. 编辑器不允许将最后一个也标为可选.',
   '93':'如果模组配方记录了各产物的概率, JEI 的(+)按钮会自动标记',
   '94':'概率产物. 未记录概率的模组则需要手动标记.',
   '97':'> 已知的任意配方类别(烧炼 / 高炉 / 模组配方)都可以使用. JEI 中某输入若显示多个',
   '98':'> 候选物品, 如`#minecraft:smelts_to_glass`中的不同沙子, 就会记录为这个',
   '99':'> 标签, 开启替代后即可使用你已有或可合成的任意成员.',
  })
 else:
  out.update({
   '332':'### data',
   '334':'以嵌套表返回所监视方块实体保存的数据; 若该方块没有实体, 则返回`nil`.',
   '335':'这些数据就是方块写入磁盘的内容, 例如熔炉的',
   '336':'燃烧与烧炼进度, 箱子中的物品, 机器的能量或配方状态.',
   '337':'键名由模组决定, 因此需要先查看目标方块',
   '338':'实际返回了哪些数据.',
   '349':'数字和字符串保持原样. NBT 没有布尔值, 因此标志位',
   '350':'以`0`或`1`读取. 列表索引从 1 开始. 若一个方块保存的值',
   '351':'超过 8192 个, 数据就会被截断, 并在表中设置`truncated = true`.',
   '353':'每个方块最多每秒读取一次数据, 因此每刻轮询的',
   '354':'开销很低, 但看到的数据可能是一秒前的. 方块被',
   '355':'替换时会立即重新读取. 仅保存在内存中而从未写入磁盘的',
   '356':'内容不会出现在返回值中.',
   '358':'### energy',
   '360':'若方块有能量存储, 则返回一个`EnergyInfo`; 否则返回`nil`.',
   '361':'它有`stored`和`capacity`两个字段, 单位采用加载器的能量',
   '362':'单位(FE). 读取字段前应检查是否为`nil`, 编辑器会在',
   '363':'缺少检查时发出警告. 与`:data()`不同, 此方法始终返回当前数据.',
   '369':'    network:get("generator_switch"):set(true) -- 设置变量',
  })
 assert set(out)=={str(i) for i,_ in m.segments(text)},key
 write(path,out);records.append({'page':key,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'translated_lines':len(out)})
 dest=BASE/'sources'/key;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
write(m.BASE/'source_manifest.json',{k:hashlib.sha256(v.encode()).hexdigest() for k,v in pages.items()})
write(BASE/'core-manual-deltas.json',records)
