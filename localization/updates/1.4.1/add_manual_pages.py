"""Four new player manual pages, translated against the current source."""
from pathlib import Path
import json,sys,zipfile
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'localization'))
import manual_extra_translation as m
BASE=Path(__file__).parent
translations={
'upgrade_station.md':{
2:'    title: 升级站',9:'# 升级站',13:'升级站可以集中调整你的 ε 系列或特制系列装备. 放入一件有效',14:'装备, 即可管理它的升级和灯光颜色.',16:'## 灯光颜色',18:'可以将装备的主(P), 副(S)或能量(E)灯光通道设为任意 RGB 颜色. 前提是',19:'该装备支持对应通道. 如果打开子界面后看不到某个通道, 就说明这件装备',20:'不支持修改它.',22:'> 所有颜色修改都必须应用后才会生效!'},
'abyssal_enchanter.md':{
2:'  title: 深渊附魔台',10:'# <Color id="light_purple">深渊附魔台</Color>',14:'  消耗试剂, 液态经验和激光束, 为书或物品添加你选定的附魔.',17:'## <Color id="gold">放置</Color>',19:'附魔台是单个物品, 放置后以所在方块为中心, 占据 3x3 且高两格的空间. 放置前该空间必须空出, 因此也能建在水下. 破坏任意部分都会使整座附魔台连同内部物品一起掉落为一个物品.',21:'工作时, 周围的碎石环会升起并转动, 柱中的核心会亮起, 底座上方则会升起一道光柱.',25:'## <Color id="gold">附魔</Color>',27:'1. 将书或能接受目标附魔的物品放入顶部槽位.',28:'2. 将试剂放入其下方的槽位. 试剂决定附魔种类: 石英对应锋利, 红石对应效率, 黑曜石对应耐久等. JEI 的 **激光附魔** 类别列出了所有配方.',29:'3. 用界面中的箭头选择等级. 默认选择最高等级.',30:'4. 向储罐填入液态经验, 再将激光束对准附魔台任意方块的任意外侧面.',32:'每级需要一组试剂, 因此锋利 V 消耗的石英是锋利 I 的五倍. 完成后, 书或物品会移到输出槽. 如果物品已有较低等级的同种附魔, 就会将其提升到新等级.',34:'如果多种附魔使用同一种试剂, 可用 **»** 按钮切换.',38:'## <Color id="gold">超限附魔</Color>',40:'附魔台最多可超过附魔正常上限五级, 因此锋利最高可达 X. 用箭头将等级调至上限之上, 等级文字就会显示为金色.',42:'超过上限后, 每提升一级, 所需总 AP 和液态经验都是前一级的四倍: 锋利 VI 为 4x, 锋利 VII 为 16x, 锋利 X 为 1,024x. 所需光束功率继续按通常曲线上升, 试剂数量则保持在正常最高等级的用量.',44:'只有物品能进行超限附魔. 顶部放书时等级不能超过正常上限, 因此需要将剑, 镐或盔甲本身放入附魔台.',48:'## <Color id="gold">液态经验</Color>',50:'储罐只接受液态经验(`c:experience`流体标签), 包括经验藻液和其他模组的经验流体. 容量约为 2.1 百万桶, 放多时可用管道抽回. 20 mB 相当于一点经验.',54:'## <Color id="gold">光束功率</Color>',56:'每种附魔都有两项以 AP 计的消耗:',58:'* 开始工作所需的 **光束功率**.',59:'* 完成前需要吸收的 **总量**. 光束高于最低要求时, 完成得更快.',61:'两者都会随等级和附魔稀有程度快速增长. 锋利 I 需要 10 AP 光束, 锋利 V 需要 250 AP 光束和总计 250,000 AP, 荆棘 III 则需要 720 AP 光束. 经验修补等宝藏附魔消耗翻倍. 界面和 JEI 会显示准确数值.',65:'## <Color id="gold">纯度</Color>',67:'光束纯度达到 **3.0** 时, 总能获得指定种类和等级的附魔. 低于该值时结果可能变化, 纯度越低越容易变化:',69:'* 等级可能浮动, 通常降低一级, 偶尔提高一级.',70:'* 可能变为适用于同一物品的另一种附魔.',71:'* 可能获得所选附魔, 并额外获得一个随机的 I 级附魔.',73:'纯度低于 **0.5** 时, 还有概率额外附加诅咒. 书或物品不会被销毁, 界面会显示当前光束的稳定程度.',77:'## <Color id="gold">合成</Color>',81:'功率, 经验, 纯度, 诅咒及超限附魔选项位于`config/nautec-common.toml`. 整合包作者可用`nautec:laser_enchanting`配方添加自定义试剂.',83:'要禁止附魔台提供某种附魔, 可在配置的`abyssalEnchanterBlacklist`中列出其 ID(`modid:*`可屏蔽整个模组), 或将其加入`nautec:abyssal_enchanter_blacklist`附魔标签. 被禁止的附魔无法制作, 不会出现在低纯度随机结果中, 也会从 JEI 隐藏. 默认禁止元素魔艺的灵魂绑定.'},
'deep_sea_reservoir.md':{
2:'  title: 深海储液库',13:'# <Color id="light_purple">深海储液库</Color>',17:'  一座 3x3x3 的储罐, 单种流体容量远超其他储罐.',20:'## <Color id="gold">放置</Color>',22:'储液库是单个物品, 放置后占据 3x3x3 的空间. 对着方块放置时, 它会以该方块为中心, 在上方建成 3x3x3 的结构, 液位表朝向你. 该空间必须先空出(空气, 水或可以覆盖的植物), 因此也能建在海床上.',24:'如果水流到原本建在干燥位置的储液库, 就会按水流规则穿过框架: 从侧面横向流入, 或从上方流下, 不会从下方往上流.',26:'破坏任意部分都会使整个储液库掉落为一个物品. 物品会保留等级和全部流体, 因此可以搬走装满的储液库.',30:'## <Color id="gold">注入与抽出</Color>',32:'* 3x3x3 结构每个方块的所有外侧面都连接同一个储罐, 管道接触任意位置都能使用.',33:'* 手持桶或其他流体容器右击可注入或抽出流体.',34:'* 空手右击打开界面. 鼠标拿着流体容器点击界面中的液位表, 也能注入或抽出.',35:'* 正面的玻璃条会按当前液位显示内部流体.',36:'* 红石比较器可读取装满程度.',38:'每次只能存储一种流体. 完全清空后, 就能重新接受任意流体.',42:'## <Color id="gold">等级</Color>',44:'| 等级 | 容量 | 升级 |',46:'| I | 500,000,000 桶 | 基础储液库 |',47:'| II | 2,000,000,000 桶 | <ItemLink id="reservoir_upgrade_2"/> |',48:'| III | 10,000,000,000 桶 | <ItemLink id="reservoir_upgrade_3"/> |',49:'| IV | 50,000,000,000 桶 | <ItemLink id="reservoir_upgrade_4"/> |',51:'每级外观都会变化: II 级带钢制框架和铆接箍带, III 级增加铜箍, 管道与阀轮, IV 级则增加发光海晶水晶饰边.',53:'升级必须按顺序安装. 手持下一级升级右击储液库, 或将其放入界面的升级槽, 即可立即生效.',55:'界面的 **移除升级** 会取出并返还最高一级升级, 使储液库下降一级. 如果现有流体超过降级后的容量, 按钮会要求再次点击确认, 并显示将损失的量. 超过较低等级容量的部分会被销毁.',59:'## <Color id="gold">合成</Color>',69:'各级容量位于`config/nautec-common.toml`.'},
'osmosis_filter.md':{
2:'  title: 渗透过滤器',10:'# <Color id="light_purple">渗透过滤器</Color>',14:'  无需燃料, 原料或光束, 即可自行产水.',17:'## <Color id="gold">使用</Color>',19:'放在任意位置后, 就会以每秒 1,000 mB(1 桶)的速度向储罐产水. 储罐达到 16,000 mB(16 桶, 可配置)时停止. 过滤时正面的面板会亮起.',21:'* 手持空桶右击可取出 1,000 mB 水. 其他流体容器也可使用.',22:'* 管道可从任意一面抽水, 无法向内输入任何东西.',23:'* 默认每面都会输出水. [侧面配置](nautec:getting_started/utilities.md)可分别开关各面.',25:'空手右击可查看储罐, 每秒产水量及输入 AP. Jade 也会显示储罐和产水速度.',27:'将水与盐送入[搅拌机](mixer.md)可制作盐水, 也可以送入[燃烧能源炉](nautec:getting_started/combustion_dynamo.md).',31:'## <Color id="gold">更强的光束</Color>',33:'渗透过滤器不需要光束, 但从任意面输入激光束可以加速: 每 40 AP 使产水量翻倍, 最高每秒 1,024,000 mB(两者均可配置).',35:'| 光束 | 每秒产水量 |',37:'| 无 | 1,000 mB |',44:'当光束使每秒产量超过 16,000 mB 时, 储罐容量会改为一秒的产量, 防止两次抽取之间因装满而停工. 光束减弱时, 储罐内已有的水会保留; 只是停止继续产水, 直到你取出一部分.',46:'更强光束可加速的所有机器见[更强的光束](nautec:getting_started/stronger_beams.md).'}
}
manifest=json.loads(m.MANIFEST.read_text());candidates=json.loads((ROOT/'localization/reports/update-1.4.1-assessment.json').read_text())['manual_new_page_candidates'];reviews=[]
for row in candidates:
 path=row['path']
 with zipfile.ZipFile(row['source']) as z:text=m.normalize(z.read(path).decode('utf-8-sig'))
 lines=text.splitlines();data=translations[Path(path).name]
 for i,zh in data.items():lines[i]=zh
 out='\n'.join(lines)+'\n'
 # New native document names also appear as item names in batch-317 below.
 for folder,content in [(m.SOURCES,text),(m.TRANSLATIONS,out)]:
  p=folder/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 target=m.target_for(path,{path:'assets/ltxi/guides/ltxi/guide' if '/ltxi/' in path else 'assets/nautec/guides/nautec/guide'})
 manifest['documents'][path]={'path':path,'source':row['source'],'format':'md','group':path.split('/')[1],'target':target,'english_words_approx':m.word_count(text),'source_sha256':m.digest(text)}
 reviews.append({'path':path,'native_chinese':False,'cfpa_local_candidate':False,'pr_candidate':'No matching cached reviewed PR document; no unverified PR adopted','reason':'New gameplay machine or equipment upgrade instructions; linked by updated pages','translated_lines':len(data)})
manifest['known_pages']=sorted(m.known_pages());m.MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(BASE/'new-manual-review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
