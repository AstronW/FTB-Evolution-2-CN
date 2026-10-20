# CFPA复用审校: mods

目标: 当前1.4.0实例的有效英文源. 输入3031条, 接受3030条, 拒绝1条; 737条记录本地修改(含标点规范及语义修订). CFPA来源2744条, PR来源275条, 当前JAR损坏JSON的官方同键修复来源12条. 不改CFPA原资源或JAR.

审阅按模组分组, 对农作物派生系列和GeoOre矿物前缀/后缀逐组比较; 保留来源完整对象. PR参考6035, 6054, 6060, 6157; 已读取相关人类讨论快照. 6054讨论指出部分文本与其他PR重叠且审阅较粗, 故逐条核对说明而不以PR获通过为依据. 6060要求不随意更改已合并文本, 此处仅修复明显错译/当前源变更和本地标点.

## 主要裁决

- GeoOre: GeOre物件统一矿晶, cluster矿晶簇, budding矿晶母岩, 大/中/小型矿晶芽, shard矿晶碎片; 世界生成结构保留矿石晶洞. 矿物前缀保持同系列一致; 晶质铀矿与铀分别识别, 不按英文字符串全局替换. 任务书已有矿晶术语与之匹配.
- Cable Tiers: Elite精英, Ultra终极, Mega极巨, Creative创造. interface原候选超级/究极修订为终极/极巨, 与general_storage任务书及配置一致. 集成堆叠升级选项描述设备等级, 不暗示堆叠升级也分级.
- Productive Farming: 灌溉槽加速的是动物, 修复候选植物错译; 补回鱼菜共生将营养水泵入作物农场的操作. 农作物种子/箱装/茎/菌落派生关系核对; 葫芦巴修复胡卢巴写法. 现任务书涉及的农场控制器/灌溉槽保持一致.
- Animal Pens: 损坏官方JSON不是全部可原样恢复. 花粉占位符编号及最大值已由CFPA正确候选覆盖; 水族罐/变种/蘑菇煲采用表意完整且一致的CFPA候选. 材质围栏同英文候选列表截断为前三种木材, 11条直接用当前JAR提取出的同键官方名, pale_oak按当前资源ID将围栏模板适配为苍白橡木动物围栏. 动物笼tip直接采用CFPA并删除无源的陆行限定. tooltip分行只译本行内容, 触发进度条件ID和 <item>/<entity> 保留.
- XyCraft: Kivi磊岩, Xychorium Xy晶, Bio Resin生物树脂; 补新源Bio/Glowing/selected/Vapor Collector限定及测试版无视觉效果说明. 标签仅在ID/语境同义时映射. 保留模组名称和作者专名.
- Hostile Neural Networks: Data Model数据模型, Data Center数据中心, Fabrication Directive制造指令单. 修复应用选择配置的参数语法, attunement调谐. trivia恢复源行数, 哞菇恢复The Last of Us典故, 不引入新增情节. 文本中_jeb按原文保留, 不做无证据源文纠正.
- Enchantment Descriptions: 修复黑暗中受伤而非额外伤害、buff只指增益、返回地表而非附近方块、附近熔岩而非强加行走条件等. 未延伸翻译无候选内容.
- Iron Furnaces: Augment统一强化组件; 移除右击模式切换误加的潜行条件, 隐藏设置适配新版Hide. rainbow_gen1/2保留各自拼接边界, 旧版连接器条件不带入. spooky字母数字梗保留并附中文释义.
- Paraglider: 试炼通过证/耐力圈/心之容器保持同模组体系. 修正雕像无精华的主语、anti-vessel是取回容器而非清空属性, 初始生命值不等于容器数量. 保留全部颜色码.
- Mystical Agriculture: 当前soulium_spawner页单数改复数, 512物品与燃料机制未变, 复用仍适用; 炉子旧页面ID改名可确认, Patchouli链接完整. 自动跨越高度释义修正.

## 未采用

`book.mysticalagriculture.entry.slow_falling_augment.page.1`: 当前英文说缓降升级会阻止Slowness, 旧中文说获得缓降. 疑似英文复制错误, 暂缺机制证据, 不擅将候选当作源文勘误, 单列拒绝. 其余候选接受不代表整模组/整本手册已完整.

## 校验

3031输入/输出标识一一对应. 接受项全部通过cfpa_review_format.invariant_errors: 英文半角标点、printf参数/百分号、颜色码、资源ID、URL、Patchouli控制、数值及字面换行. 数字词和数字形式逐项回查; 结构检查是语义审校后的补充. 未游戏内测试, 未安装到目标实例.


## 后续机制复核

总集成阶段进一步用当前 JAR 字节码解决残页解锁和缓降升级的原文错误, 更新了原先暂缓结论. 最终接受/拒绝数以 `../review-summary.json` 和对应 decisions JSON 为准, 本文件前段保留初审记录. 证据见 `../code-evidence/`.
