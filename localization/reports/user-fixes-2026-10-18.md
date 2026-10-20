# 2026-10-18 玩家反馈修复

目标为 project.json 指定 FTB App 1.4.0 / MC 26.1.2 实例, 已核对 instance.json 与 .minecraft/mods 链接. 原始英文、CFPA 原件、任务结构、配方、交易逻辑和存档不变.

## 修复内容

1. Nutritional / Nutritional Balance 采用用户指定的营养均衡; Nutrients/Nutrient 采用营养. 同步任务书、模组名语言键、营养属性、进度、JEI 说明和食物提示. 食物前缀来自当前 JAR 硬编码, 另用客户端脚本修复, 单改语言 JSON 不足以生效.
2. 喷气背包飞行任务中 Simply Jetpacks 是原文误指. 当前实例为 Iron Jetpacks 9.0.3, 中文更正为铁制喷气背包. 见 source_corrections.md.
3. Horse Power 对应当前 Horse Powered, 统一为马力.
4. Hephaestus/Hephaestus Forge 统一为匠神, Hephaestus Tools 为匠神工具.
5. 制作合金的末句改为 `&e注意&r: 本整合包中, &e末影接口&r的&2合金炉&r用一个铁锭和一个煤炭炼钢; &eEnergized Power&r的&2合金炉&r同样只需一个铁锭和一个煤炭.`. 原始源文不改, 格式校验只对 quest_format_corrections.json 精确记录的源文/译文对允许增加这两组颜色, 其他保护继续执行.
6. Stellaris 统一为群星.
7. NauTec/Nautec/NauTec 2 统一为海蓝科技.
8. Auroral 统一为极光.
9. 新增客户端名称桥接, 根据当前真实模组 ID 映射 33 个已有明确译名的模组, 通过 KubeJS 的元数据名称接口供提示显示使用. 未审定专名继续保留英文, 不凭名称猜译. 包含用户指定的全部模组.
10. Nodeworks 既有 111 键中文已存在手册资源包中, 但汇总包只输出了普通批次的单个分类键. 修复打包器后按键合并, 补回 110 个缺失键, `item.nodeworks.celestine_shard` 现输出天青石碎片, 不重译已有正文.
11. Dimensional Resources 同步为维度资源, 并检查同类跨阶段遗漏. 共补回 282 个既有键: Nodeworks 110, FTB 工业奇械 164, FTB 手册入口 8. 2 个重叠工业奇械格式标签按普通批次的空格格式同步手册资源, 无未裁决冲突.

## 可维护来源与验收

- 用户裁决同步到任务词表、可维护任务书、手册翻译与 extra_resources、普通语言 TSV. 各批次历史来源保留, 与旧快照差异另存 reviewed-revisions.json / overlay-revisions.json.
- 改前文件快照在 user-fixes-2026-10-18/before, 不用于构建. 不改历史来源文件来消除检查失败.
- 新增 test_release_language_merge.py 回归检查, 修复前在 FTB 手册入口缺失处失败, 修复后检查每个手册语言键都存在于汇总结果且译文正确.
- `python project.py check` 全部 329 项通过, 包含当前 JAR 绑定、任务结构、手册原生解析、全部普通批次与客户端模拟/源绑定检查. 随后营养措辞进一步统一, 第 140 批 build/check 再次通过.
- release_pack.py build/check 与安装后的逐文件 SHA-256 核验通过. 最终完整安装包、资源包和安装记录仍使用 dist/ 既有稳定路径. 安装按文件清单备份, 未整体覆盖实例目录. 初次安装写入 126 文件, 新增 2 个客户端脚本; 营养措辞末次更新仅替换资源包.
- 游戏原有启用列表已包含最终汇总 ZIP, 且位于最高优先级. 安装未修改 options.txt.
- 最终语言值扫描仅有 `海蓝科技(Nautec)的指南` 合理双语提示保留英文, 已有中文名称, 不属于漏翻. 资源 ID、链接、语言键和代码中的英文仍保留.

**尚未游戏内验收**: 客户端须完整重启以加载新脚本, 再检查食物营养提示、模组名、天青石碎片、任务颜色与手册入口. 静态检查及模拟 API 不能证明实际渲染、JEI 缓存和跨模组事件顺序的最终表现. 本次不将它们写成已通过游戏内验收.
