"""Translate all eight changed pack overrides, retaining current UpgradeEntry tags."""
from pathlib import Path
import hashlib,json,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'localization'));import manual_extra_translation as m
BASE=Path(__file__).parent;GAME=Path(json.loads((ROOT/'project.json').read_text())['target_instance'])
D={
'Tools':'工具','# ε-Series tools':'# ε-系列工具',
'The ε (epsilon) series is our standard tool product line. All tools are unbreakable, run on <Color id="energy">Energy</Color>,':'ε 系列是我们的标准工具产品线. 所有工具都无法损坏, 由<Color id="energy">能量</Color>驱动,',
'and are [upgradable](fundamentals/upgrade_system.md).':'并且[可以升级](fundamentals/upgrade_system.md).',
'## Modular Mining Tools':'## 模块化挖掘工具','### Default upgrades':'### 默认升级','### Default upgrade':'### 默认升级',
'The Drill, Shovel, Axe and Hoe are designated *modular mining tools*. Switching equipment mode cycles through the 5':'钻头, 锹, 斧和锄属于 *模块化挖掘工具*. 切换装备模式可循环选择 5 种',
'available base mining speeds:':'基础挖掘速度:',
'- **Off**: Block breaking disabled, including in creative mode.':'- **关闭**: 禁止破坏方块, 包括创造模式.',
'- **Slow**: 3.0':'- **慢速**: 3.0','- **Normal**: 9.0':'- **正常**: 9.0','- **Fast**: 20.0':'- **快速**: 20.0','- **Turbo**: 75.0':'- **超速**: 75.0',
'The upgrade system can raise the mining level (limit) and expand the set of blocks the tool is effective on. The Shovel,':'升级系统可以提高挖掘等级(上限), 并扩展工具适用的方块范围. 锹,',
'Axe, and Hoe are effective on their respective materials. The Drill is effective on both *pickaxe* and *shovel*':'斧和锄适用于各自对应的材料. 钻头可开采 *镐* 和 *锹*',
'harvestable materials for mining convenience.':'适用的材料, 以方便采矿.',
"> ε-Series Shovel's default upgrade module grants Silk Touch.":'> ε-系列锹的默认升级模块提供精准采集效果.',
'## Other Mining Tools':'## 其他挖掘工具',
'The Wrench and Shears do not have the variable speed or the ability to change effective blocks via the upgrade system.':'扳手和剪刀无法调节速度, 也不能通过升级系统改变适用方块.',
'They still support the enchantment upgrade modules.':'它们仍然支持附魔升级模块.',
'## Melee weapons':'## 近战武器','### Melee weapons':'### 近战武器',
'The Sword and Axe are designated *melee weapons*. They share certain upgrade modules with the [signature series weapons](weapons/index.md)':'剑和斧属于 *近战武器*, 与[特制系列武器](weapons/index.md)共享部分升级模块,',
'including enchantment modules (Razor and Looting) and target filters.':'包括附魔模块(剃刀和抢夺)及目标过滤器.',
'> The [Equipment Damage Modifier](fundamentals/damage_modifiers.md) system applies to all ε-Series melee weapons.':'> [装备伤害修正](fundamentals/damage_modifiers.md)系统适用于所有 ε-系列近战武器.',
'## Miscellaneous tools':'## 杂项工具',
'These tools do not currently provide extra capabilities beyond their baseline. It is still recommended to obtain them,':'这些工具目前只有基础功能, 没有额外能力. 不过由于制造成本较低,',
'given their cheaper Fabrication cost.':'仍然建议制作.',
'## Compatible Upgrades':'## 兼容升级','### All ε-Series tools':'### 所有 ε-系列工具',
'- **Resonance-Tuned Servos**: Max rank 1. Suppresses the vibrations the held tool emits.':'- **共振调谐电机**: 最高 1 级. 抑制手持工具发出的振动.',
'- **Augmented Equipment Battery**: Max rank 4. Multiplies energy capacity by 4 at rank 1, doubling':'- **强化装备电池**: 最高 4 级. 1 级时能量容量乘以 4, 此后每级翻倍,',
'  each rank up to 32x at rank 4. Also fits [AL/1C armor](armor.md).':'  4 级时最高 32x. 也适用于 [AL/1C 盔甲](armor.md).',
'### Mining tools':'### 挖掘工具','The Drill, Shovel, Axe, Hoe, Shears, and Wrench.':'钻头, 锹, 斧, 锄, 剪刀和扳手.',
'- **Overclocked Harvest Matrix**: Max rank 5. Applies Fortune at level 1, 2, 3, 5, or 7 by rank.':'- **超频采收矩阵**: 最高 5 级. 按等级提供 1, 2, 3, 5 或 7 级时运.',
'- **Stabilized Harvest Matrix**: Max rank 1. Applies Silk Touch.':'- **稳定采收矩阵**: 最高 1 级. 提供精准采集.',
'- **Mining Subspace Link**: Max rank 1. Sends broken block drops straight into your inventory.':'- **亚空间采掘链接**: 最高 1 级. 将破坏方块的掉落物直接送入你的物品栏.',
'> The two Harvest Matrices share an exclusive set. A tool can carry Fortune or Silk Touch, never both.':'> 两种采收矩阵互斥. 工具只能具有时运或精准采集之一, 无法同时拥有两者.',
'### Modular mining tools':'### 模块化挖掘工具','The Drill, Shovel, Axe, and Hoe.':'钻头, 锹, 斧和锄.',
'- **ε Cutter Rev.000**: Max rank 1. Makes the tool effective on every block, on top of its own':'- **ε 切割器 Rev.000**: 最高 1 级. 在工具原有材料范围之外, 使其对所有',
'  material set.':'  方块都有效.',
'### Single tool modules':'### 单种工具模块',
'- **Prospector Nanites**: Max rank 1. ε Drill. Vein-mines up to 64 ores at once, spending extra':'- **纳米探矿机器**: 最高 1 级. 用于 ε 钻头. 一次最多连锁开采 64 个矿石, 每多开采一个方块',
'  energy per additional block.':'  都会额外耗能.',
'- **Lumber Felling Unit**: Max rank 1. ε Axe. Fells up to 256 logs at once along with the':'- **树木倾倒单元**: 最高 1 级. 用于 ε 斧. 一次最多砍伐 256 个原木及其',
'  surrounding leaves, at no extra energy cost.':'  周围树叶, 不额外消耗能量.',
"- **ε Anglers' Kit**: Max rank 5. ε Fishing Rod. Applies Lure and Luck of the Sea at the installed":'- **ε-垂钓者套装**: 最高 5 级. 用于 ε 钓鱼竿. 按安装等级提供饵钓和海之眷顾',
'  rank.':'  附魔.',
'The ε Sword and ε Axe are also part of `#ltxi:weapons`, so they take the weapon-side modules:':'ε 剑和 ε 斧也属于`#ltxi:weapons`, 因此可安装武器侧模块:',
'Combat Yield Protocol, Severance Algorithm, Combat Subspace Link, Biometric Obfuscation, and the':'战利品协议, 高效切割算法, 亚空间战斗链接, 生物识别混淆, 以及',
 'three Engagement Protocols. See [Weapons](weapons/index.md) for what each one does.':'三种开火协议. 各自用途见[武器](weapons/index.md).',
'## Stats':'## 属性',
'Installed via the [Upgrade System](../fundamentals/upgrade_system.md).':'通过[升级系统](../fundamentals/upgrade_system.md)安装.',
'- **Echo Suppressor**: Max rank 1. Suppresses the vibrations this weapon emits, keeping Sculk':'- **回响抑制装置**: 最高 1 级. 抑制武器发出的振动, 防止幽匿',
'  Sensors and Wardens from noticing your fire.':'  感测体和监守者察觉你开火.',
'- **//ERR~MAG-Z!!-NE//∞**: Max rank 1. Replaces the ammunition source with an infinite one.':'- **//ERR~MAG-Z!!-NE//∞**: 最高 1 级. 将弹药来源替换为无限弹药.',
'  No recipe exists for this module.':'  此模块没有合成配方.',
'- **Combat Yield Protocol**: Max rank 5. Applies Looting to your kills, at level 1, 2, 3, 5, or 7':'- **战利品协议**: 最高 5 级. 使击杀获得抢夺效果, 按等级分别为 1, 2, 3, 5 或 7',
'  by rank.':'  级.',
'- **Severance Algorithm**: Max rank 5. Applies the [Razor](../enchantments.md) enchantment at':'- **高效切割算法**: 最高 5 级. 按安装等级提供[剃刀](../enchantments.md)',
'  the installed rank.':'  附魔.',
'- **Combat Subspace Link**: Max rank 1. Mob drops from your kills go straight into your inventory.':'- **亚空间战斗链接**: 最高 1 级. 被你击杀的生物掉落物直接进入物品栏.',
'- **Biometric Obfuscation**: Max rank 1. Tags its damage as `minecraft:no_anger`, so striking':'- **生物识别混淆**: 最高 1 级. 将伤害标为`minecraft:no_anger`, 因此攻击',
'  neutral mobs does not provoke them.':'  中立生物不会激怒它们.',
'- **Engagement Protocol: Extermination**: Max rank 1. Engages any entity, regardless of hostility.':'- **开火协议: 灭绝**: 最高 1 级. 可攻击任意实体, 不限敌意程度.',
'- **Engagement Protocol: Preemption**: Max rank 1. Engages anything at Neutral Enemy hostility':'- **开火协议: 先发**: 最高 1 级. 可攻击敌意为中立敌人',
'  or above.':'  或以上的目标.',
'- **Engagement Protocol: Rectification**: Max rank 1. Engages Hostile entities only.':'- **开火协议: 矫正**: 最高 1 级. 仅攻击敌对实体.',
'> The three Engagement Protocols share an exclusive set. Only one target filter can be':'> 三种开火协议互斥, 同时只能安装',
'> installed at a time.':'> 一种目标过滤器.',
'The *Daybreak* is a heavy rocket launcher specializing in eliminating high threat targets. Upon impact, it will spawn':'*破晓* 是专门消灭高威胁目标的重型火箭发射器. 命中后会产生',
"a swarm of 7 Homing Bomblets. For a direct hit, these will all be targeting the impacted entity (if it's still alive,":'一群共 7 枚制导子炸弹. 直接命中时, 它们都会锁定被击中的实体(如果它还活着),',
 'that is) or will idle until a valid target wanders into their range. These bomblets can only acquire a target once,':'否则会等待有效目标进入范围. 每枚子炸弹只能锁定一次目标,',
 'and will only damage their target. If you need widespread destruction, consider the [Hanabi](hanabi.md).':'且只会伤害自己的目标. 需要大范围破坏时, 可以考虑[花火](hanabi.md).',
"Don't let its size fool you, *Serenity*'s LightFrags are engineered to tear apart low threat, unarmored enemies at close":'别被体积骗了, *静谧* 的光弹专门用于在近距离撕碎低威胁, 无护甲的敌人.',
'range. As a downside, it will [struggle](../fundamentals/damage_modifiers.md) against armored and higher threat targets.':'代价是面对有护甲或高威胁目标时会[力不从心](../fundamentals/damage_modifiers.md).',
'## Shells':'## 炮弹',
'Hanabi can fire several types of shells. After extensive field research, we have replaced the standard-issue explosive':'花火可以发射多种炮弹. 经过大量实地研究, 我们已用新型火花弹替换制式爆炸',
'shells with our new Sparkler shells. Other types must be unlocked via [Equipment Upgrade Modules](../fundamentals/upgrade_system.md).':'炮弹. 其他类型需通过[装备升级模块](../fundamentals/upgrade_system.md)解锁.',
'### Sparkler':'### 火花弹',
'This shell creates a strong primary explosion, then splits into 14 bomblets which deal massive amounts of explosive damage':'该炮弹先产生一次强烈爆炸, 再分裂成 14 枚子炸弹, 在大片圆形区域内造成大量',
'in a large circular area.':'爆炸伤害.',
'### Flame':'### 火焰',
'Creates a stationary flame field that lingers for **5 seconds** and continuously burns everything inside it. Not':'产生一个持续 **5 秒** 的固定火焰区域, 持续灼烧其中的一切. 不建议',
'recommended against highly mobile targets.':'用于对付高机动目标.',
'### Cryo':'### 霜冻',
'Cryo shells blast enemies in a large area with ice. Recommended for crowd control or enemies weak to ice.':'霜冻炮弹以寒冰打击大范围敌人. 适合群体控制或对付弱冰敌人.',
'### Electric':'### 电能',"Electric shells' specialty is wet and underwater combat.":'电能炮弹擅长潮湿环境和水下战斗.',
'### Acid':'### 强酸','Acid shells specialize against highly armored or high threat targets. Their blast radius is smaller, but':'强酸炮弹专门对付重甲或高威胁目标. 爆炸范围较小, 但',
 'they deal increased damage to compensate.':'以更高伤害作为补偿.',
'### Gloom Gas':'### 阴郁气体','Gloom Gas shells weaken enemy damage and abilities.':'阴郁气体炮弹削弱敌人的伤害和能力.',
'- Damage is tagged `#minecraft:is_fire`, both impact and flames.':'- 命中和火焰伤害均带有`#minecraft:is_fire`标签.',
'- `#minecraft:is_explosion` damage tag.':'- 带有`#minecraft:is_explosion`伤害标签.',
'- 3x bonus damage against `#ltxi:weak_to_flame` enemies':'- 对`#ltxi:weak_to_flame`敌人造成 3x 额外伤害',
'  - Strays, Polar Bears, Snow Golems':'  - 流浪者, 北极熊, 雪傀儡',
'- 8x bonus damage against `#ltxi:weak_to_cryo` enemies':'- 对`#ltxi:weak_to_cryo`敌人造成 8x 额外伤害',
'  - By default, this tag is `#minecraft:freeze_hurts_extra`: Striders, Blazes, Magma Cubes':'  - 默认此标签为`#minecraft:freeze_hurts_extra`: 炽足兽, 烈焰人, 岩浆怪',
'- Applies [*Frostbite III*](../fundamentals/mob_effects.md#frostbite) for 20 seconds':'- 施加持续 20 秒的[*霜冻 III*](../fundamentals/mob_effects.md#frostbite)',
'- 3x bonus damage if either criteria met:':'- 满足以下任一条件时造成 3x 额外伤害:',
'  - Target is in rain or water':'  - 目标处于雨中或水中',
'  - Is tagged `#ltxi:weak_to_electric`: Turtles, Axolotls, Guardians, Elder Guardians, Fish, Dolphins, Squids, Glow Squids, Tadpoles':'  - 具有`#ltxi:weak_to_electric`标签: 海龟, 美西螈, 守卫者, 远古守卫者, 鱼, 海豚, 鱿鱼, 发光鱿鱼, 蝌蚪',
'- Applies [*Corroding III*](../fundamentals/mob_effects.md#corroding) for 10 seconds':'- 施加持续 10 秒的[*腐蚀 III*](../fundamentals/mob_effects.md#corroding)',
'- Applies [*Gloom III*](../fundamentals/mob_effects.md#gloom) for 30 seconds':'- 施加持续 30 秒的[*阴郁 III*](../fundamentals/mob_effects.md#gloom)',
'- **Hanabi Launch Boost**: Max rank 2. Raises shell projectile speed.':'- **花火发射加速**: 最高 2 级. 提高炮弹飞行速度.',
'### Shell Cores':'### 炮弹核心','Each core unlocks one of the shell types described above. Sparkler shells need no core.':'每个核心解锁上述一种炮弹类型. 火花弹无需核心.',
'- **Acid Shells**: Max rank 1. Unlocks **Acid** shells.':'- **花火核心 / 强酸**: 最高 1 级. 解锁 **强酸** 炮弹.',
'- **Cryo Shells**: Max rank 1. Unlocks **Cryo** shells.':'- **花火核心 / 霜冻**: 最高 1 级. 解锁 **霜冻** 炮弹.',
'- **Electric Shells**: Max rank 1. Unlocks **Electric** shells.':'- **花火核心 / 电能**: 最高 1 级. 解锁 **电能** 炮弹.',
'- **Flame Shells**: Max rank 1. Unlocks **Flame** shells.':'- **花火核心 / 火焰**: 最高 1 级. 解锁 **火焰** 炮弹.',
'- **Gloom Gas Shells**: Max rank 1. Unlocks **Gloom Gas** shells.':'- **阴郁气体装弹**: 最高 1 级. 解锁 **阴郁气体** 炮弹.',
'- **ARCOIRIS Engine**: Max rank 1. Unlocks all five shell types at once. No recipe exists for this':'- **花火核心 / 炫彩**: 最高 1 级. 一次解锁全部五种炮弹. 此模块没有',
'  module.':'  合成配方.'}
labels={'Base damage':'基础伤害','Base direct hit damage':'基础直击伤害','Base splash damage':'基础溅射伤害','Base bomblet damage':'基础子炸弹伤害','Range':'射程','Projectile speed':'弹射物速度','Trigger cooldown':'扳机冷却','Charge time':'蓄力时间','Blast radius':'爆炸半径','Bomblet damage':'子炸弹伤害','Flame field damage':'火焰区域伤害','Fire Rate':'射速','Fire rate':'射速'}
names={'Aurora':'极光','Daybreak':'破晓','Hanabi':'花火','Mirage':'幻影','Nova':'新星','Serenity':'静谧','Stargazer':'瞻星'}
def translate(s):
 if s in D:return D[s]
 if s.startswith('    title: '):return '    title: '+names.get(s[11:],D.get(s[11:],s[11:]))
 if s.startswith('# *'):
  for en,zh in names.items():
   if f'*{en}*' in s:return s.replace(f'*{en}*',f'*{zh}*')
 if s.startswith('> *') and 'Intrinsics* is pre-installed at rank 1.' in s:
  en=next(n for n in names if n+' Intrinsics' in s);return f'> *{names[en]}特性模块* 默认安装为 1 级. 移除后可重新制造替代品.'
 if s.startswith('- Trigger: '):return '- 扳机: '+{'Automatic':'全自动','Semi Auto':'半自动','Charge-up fusion':'蓄力聚变'}[s.split(': ',1)[1]]
 if s.startswith('- Projectile: '):return s.replace('- Projectile: ','- 弹射物: ').replace('[LightFrag]','[光弹]').replace(' pellets',' 颗弹丸').replace('Rockets','火箭').replace('Shell Grenades','榴弹')
 if s.startswith('- '):
  for en,zh in labels.items():
   if s.startswith('- '+en+': '):return s.replace('- '+en+': ','- '+zh+': ',1).replace(' sec',' 秒').replace('Varies (see below)','不定(见下文)').replace('9.0 x pellet, 63.0 max','每颗弹丸 9.0, 最高 63.0').replace('10.0, *20.0 if shell impacts in rain or water*','10.0, *在雨中或水中命中时为 20.0*').replace('4.0 every 4 ticks (100.0 total damage potential)','每 4 刻造成 4.0(理论总伤害为 100.0)')
 if not s.strip() or s.startswith(('<','---','navigation:','item_ids:','  -','    icon:','    position:','    parent:')):return s
 raise AssertionError(('Unreviewed visible source',s))
manifest=json.loads(m.MANIFEST.read_text());review=[]
for r in json.loads((ROOT/'localization/reports/update-1.4.1-assessment.json').read_text())['pack_asset_changes']:
 if '/ltxi/' not in r['path']:continue
 source=GAME/r['path'];path=r['path'].removeprefix('kubejs/');text=source.read_text();out='\n'.join(translate(s) for s in text.splitlines())+'\n'
 for folder,data in [(m.SOURCES,text),(m.TRANSLATIONS,out)]:
  p=folder/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
 # Snapshot the exact effective English in the work copy for future checks.
 p=ROOT/'.minecraft'/r['path'];b=BASE/'before'/p.relative_to(ROOT)
 if p.exists() and not b.exists():b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(p.read_bytes())
 p.write_bytes(source.read_bytes())
 manifest['documents'][path]={'path':path,'source':str(source),'format':'md','group':'ltxi','target':m.target_for(path,{path:'assets/ltxi/guides/ltxi/guide'}),'english_words_approx':m.word_count(text),'source_sha256':m.digest(text)}
 review.append({'path':path,'reason':'Native Chinese is shorter and omits pack-specific upgrade instructions; retain current KubeJS components and update prose.','term_source':'Current LTXI 2.4.0 native zh_cn item/upgrade names, preserving weapon IDs and recipe components.'})
manifest['known_pages']=sorted(m.known_pages());m.MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(BASE/'ltxi-override-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
