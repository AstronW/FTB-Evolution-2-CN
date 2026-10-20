# 1.4.0 客户端显示修复

本批按 2026-10-18 玩家反馈维护. `mod-names.json` 记录当前 JAR 元数据名、规范中文与 JAR 哈希. `mod_names.js` 使用当前 KubeJS 8.0.7 的 `Platform.getInfo(id).setName` 接口同步已有中文模组名, 包含用户指定的 8 个模组及已有明确译名的模组. 未审定的模组名继续保留英文.

`nutrients.js` 仅修复 Nutritional 1.2.3 的食物提示硬编码前缀 `Nutrients: `. 原生 `NutritionTooltip.onTooltip` 使用 Component.literal, 不读取 `tooltip.nutritional.nutrients`. 当前 KubeJS LOW 优先级事件在该模组之后处理提示. 脚本使用 dynamicTooltips, 通过中文语言键检查启用, 保留原始各子组件、数值和颜色, 不改营养逻辑.

`manifest.json` 记录脚本目标与哈希以及当前实际 API/提示实现 class 哈希. 汇总安装器只按此清单安装 2 个新增 client_scripts 文件. 不覆盖整合包现有 tooltips.js.

检查:

```
python localization/client_fixes/verify_sources.py
node localization/client_fixes/verify_runtime.cjs
```

模拟检查覆盖中文前缀、英文语言保持、营养类型/数值子组件、颜色、不相关提示及全部名称映射. 它不启动 Minecraft. 安装后需要重启客户端, 实测物品提示、JEI 与 Jade 的名称显示, 尚未进行游戏内验收.

## 已有中文模组名补接 (2026-10-18)

上一轮仅通过任务词表收集 33 项, 未覆盖模组原生中文中的名称标签. 本轮按当前 JAR 元数据名、原生英文名称标签与有效中文标签逐项核对, 新增 112 项, 共 145 项. 神秘农业和应用能源2已纳入; 逐项出处与暂缓理由见 mod-name-audit.json, 每条新增映射的 source_evidence 绑定源键及原始中文. 只使用已有中文候选, 不根据模组 ID 或物品名前缀猜译.

Animal Pen 的候选都是带木材名的物品, Auth Me 候选为设置标题, NeoSync 的新克隆疑似误译, Refined Storage 及 3 个关联模组存在术语/含义冲突, 这 7 项保留原显示并单列, 不声称全部模组名已汉化. 其余无完全匹配名称标签的模组也不据此认定没有中文名.

修改 mod-names.json 后运行 `python localization/client_fixes/build_mod_names.py`, 自动生成 mod_names.js 并更新脚本哈希. `verify_sources.py` 检查生成结果、已批准审计条目、当前 JAR 与中文标签; `verify_runtime.cjs` 检查完整映射实际执行, 并固定神秘农业/应用能源2的遗漏回归用例. 原生中文只在新增显示映射中转换为项目半角标点, 上游资源不改写.

## 用户裁决已关闭上述 7 项暂缓

同日后续用户明确: Refined Storage 为精致存储, Quartz Arsenal 不翻译, NeoSync 为新克隆, Auth Me 不翻译, Animal Pen 模组名为动物围栏. 当前映射为 151 项, 上述 7 项全部已裁决, 不再待复核. 配置/模组名 Quartz Arsenal 覆盖见 ordinary/batch-315. 精确显示名与授权记录见 user-name-decisions.json, 原始候选记录保留用于追溯.

## Quartz Arsenal 最新裁决

用户后续明确无线合成符合模组内容, 要求采用该译名. 当前有效显示名为精致存储 - 无线合成, 配置标题为精致存储 - 无线合成 配置. 取代上文保留英文的历史要求, 不再将无线合成称为误译. 已同步显示映射和第 315 批 6 个语言键.
