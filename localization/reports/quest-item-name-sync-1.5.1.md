# 任务书物品名同步 (1.5.1, 2026-10-23)

任务书先于普通物品文本翻译, 部分任务标题, 任务/奖励说明中的物品名与当前游戏内名称不一致. 本轮以当前实际生效的中文物品名为准, 修正任务书可维护译文 `localization/translations/chapters/*.json`, 再由 `quest_translation.py build` 重新生成. 逐条映射见 [quest-item-name-sync-1.5.1.json](quest-item-name-sync-1.5.1.json).

## 依据与方法

- 生效名称按加载顺序合并: 当前 `.minecraft/mods` JAR 自带 zh_cn < 目标实例 KubeJS 资源 < 本项目发布资源包 (普通批次, 定制内容, 手册, CFPA 审校子集, 2026-10-19 反馈覆盖).
- 候选来源: (1) 任务/任务目标/奖励标题英文与所含物品英文名相同, 但中文不同; (2) 章节引用模组的物品英文名出现在说明原文中, 而对应中文段落未出现当前物品名.
- 每条映射限定章节, 并要求该段英文原文含对应物品英文名, 必要时再限定片段编号. 同名异物按上下文区分, 例如 Refined Storage 本体用 输入总线/输出总线/成型面板/破坏面板, Cable Tiers 分级版本沿用其 精英输入器 等现名; Modular Routers 的 投掷器模块 (Dropper) 与 投掷模块 (Flinger) 分开处理.
- 共修改 36 个章节的 714 个文本片段, 涉及较多的是 Nautec (共振→共鸣, 海蓝水晶→海棱水晶, 生物反应器→生物反应机等), 通用存储, 资源生产, 烹饪与酿造和物流. 群系与实体名随同步: 海底热泉, 荧光海林, 热泉爬行者; 强化 热泉甲壳. 菌种名按当前 `bacteria.nautec.*` 同步: 铁菌→嗜铁菌, 金菌→嗜金菌, 钻石菌→嗜金刚菌, 绿宝石菌→嗜绿宝石菌, 青金石菌→嗜青金菌, 金属菌→嗜金属菌, 石头菌→嗜岩石菌, 造藻菌→成藻菌, 钙质菌→嗜钙菌, 嗜盐菌→盐细菌, 产甲烷菌→甲烷菌, 硫磺菌→嗜硫菌; "金属和宝石菌" 等泛称不改.

## 有意保留

- 已有术语裁决的概念词: Shimmerweave 仍作 微光编织 (仅 Shimmerweave Fabric 物品改为 微光布), 见 TERMINOLOGY.md.
- 充能能源手册: 当前物品名为 JAR 的 `Energized Power 指南`, 但模组名已审定为 充能能源, `test_feedback_fixes` 要求任务书使用审定模组名, 故不改.
- S'nore 任务标题保留 雪酥夹心(S'nore) 说明; 压印器并发压印模板 标题按英文分色结构保留 "压印器" 前缀.
- 仅全角/半角标点或空格不同的名称 (如 Just Dire Things 的 `升级：…`, `流体抽屉（1x1）`) 按 STYLE.md 使用半角, 不视为不一致.
- 泛称和其他模组同名词不改: 计算机, 提取机, 放置/破坏模块, Oritech 分级速度插件, 龙骨剑等复合名; Powah 粗晶质铀 (当前物品名 天然晶质铀（普通） 带矿石等级, 原文泛指掉落物).

## 未处理

- 手册与 Patchouli 中的同类名称未在本轮范围内复核.

## 校验

- `python localization/quest_translation.py build` / `check`: 51 文件完整.
- `python localization/verify_quests.py`: passed.
- `python project.py check`: 全部通过.
- 未启动游戏, 未做游戏内验收.
