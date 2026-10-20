# 2026-10-19 玩家反馈修复

目标: project.json 指定的 FTB Evolution 2 1.4.0 实例. 来源为当前 JAR, 实际整合包 datapack/KubeJS, 已维护的译文与已审定模组名称. 原模组 JAR, 实际配方, 任务结构和玩家数据不改动.

## 处理结果

| 反馈 | 结果与原因 |
| --- | --- |
| Nodeworks UI | 111 个原生语言键在最终包内均存在, 仅模组专名保留英文. 剩余 UI 为代码字面量. 按用户最新要求不再汉化这部分, 不安装客户端代码补丁. `nodeworks-*-candidates.txt` 仅为排查证据, 不计为待译任务. |
| 任务书模组名不同步 | 从当前已审定的 `client_fixes/mod-names.json` 同步 32 个模组, 任务书可维护译文 85 处, 词表 2 处. 包含充能能源, 群星, 极光, 矿石晶洞, 新克隆等. 映射逐项见 `quest-name-changes.json`. 不改组件动作, 资源 ID 或命令. |
| AE2 处理器的硅配方 | FTB Materials 将 ae2:silicon 统一到 ftbmaterials:silicon_gem. RecipeFor 查询改为实际统一后的产物, 配方本身不改动. |
| FTB 工业奇械合金及其他统一材料 | 同一原因. 修改合金页的青铜, 琥珀金, 殷钢, 康铜, 钢, 以及粉碎机/粉末页的煤粉查询. 共 4 页 8 处统一映射. |
| Kindred Spirits / Oracle Index 目录 | 补入 4 个 `_meta.json`, 共 26 个目录名称, 保持页面路径, 顺序和 icon. 使用当前 schema 1 的 translated/zh_cn 路径. Oracle Index 的 45 个语言键原先已齐全, 本轮补的是独立导航元数据. 开发文档栏目名一并翻译, 开发者 API 正文仍沿用原有范围. |
| GuideME 全量配方引用 | 扫描当前有效的 802 篇文档, 其中 376 页有 844 处可见配方组件. 826 处找到静态候选. 另外修复极光手册 4 处把配方 ID 当物品 ID 的 RecipeFor 用法, 改为 Recipe. 排除 Markdown 注释与 fenced 示例. |
| 有配方但不能渲染 | Powah 带电雪球只有 energizing 配方, 当前 GuideME 没有该类型渲染器. 保留查询, 添加准确的非空说明: 1 个雪球 + 500,000 FE -> 1 个带电雪球. 不声称恢复了动态配方框. Nodeworks 的灵魂沙灌注在其专属 Guide 注册了渲染器, 不误报为不支持. |
| 本来没有制作配方的 18 处 | 8 处被整合包禁用 (Powah 初级/基础反应堆及热力发电机, Just Dyna Things 的 4 种太阳能板), 1 处玩家天线珍珠通过实体交互获取, 1 处创造储能单元, 8 处上游页面引用但当前版本没有配方的条目. 保留组件并添加可见的非空说明, 不恢复禁用配方, 不猜测旧物品到新物品的映射. 逐项见 component-corrections.json. |
| Patchouli 首页 | 可以汉化. 当前 GuiBookLanding 以 Component.translatable 读取 book.landingText, 即使该值是英文整句也可作为语言键覆盖. 补入动物围栏, LaserIO, Just Dire Things, 资源蜜蜂 4 本书的 9 个名称/副标题/介绍字段. 不替换服务端 book.json, 不改书籍逻辑或 i18n 开关. |

Ender IO 的另一本未完成指南使用 `guidebook.enderio.book_title` / `guidebook.enderio.landing_text`, 当前 JAR 没有对应英文语言正文; CFPA 1.21 的候选也只是 Book Title / Landing Text 对应的“书名”/“文本”占位符. 没有将其虚构为完整介绍页. Building Gadgets 2 仍遵循项目建筑辅助内容排除范围.

## 来源与构建

- `before/` 是本轮修改前的任务书译文, 词表, 构建工具快照.
- `manifest.json` 绑定当前输入 SHA-256, 基础页面 SHA-256 与 33 个明确覆盖文件. `pack/` 是生成产物.
- `metadata-translations.json`, `landing-translations.json`, `component-corrections.json` 是可维护来源. 统一材料依据实际 `config/ftbmaterials/unifier-db.json`, 不能将此数据库改成游戏配方修复.
- 新首页字段先查当前官方中文与本地 CFPA 各版本: 相关 CFPA 的 book.json 仍为英文原句, 因此按当前源文人工翻译; 保留 LaserIO / Just Dire Things 现有专名, 不另创模组规范名称.
- `feedback_fixes.py` 验证来源, 只在发布汇总的最后一层应用明确覆盖. 其他阶段生成的源页面保持原貌, 原有格式保护断言继续执行.
- `guideme-recipe-audit.json` 是逐组件清单; `guideme-recipe-audit-inputs.json` 固定当前扫描输入, 没有无法解析而被静默跳过的配方 JSON.

```bash
python localization/quest_translation.py build
python localization/feedback_fixes.py build
python localization/feedback_fixes.py check
python localization/audit_guideme_recipes.py
python localization/verify_feedback_native.py
python project.py check
python localization/release_pack.py build
python localization/release_pack.py check
python localization/release_pack.py install --enable
python localization/release_pack.py check
```

## 校验与安装

- 11 项单元回归检查通过, 包括模组名同步, 导航键/图标/顺序, Patchouli 原句语言键打包, 配方组件修复, 注释排除及不安装 Nodeworks 代码补丁.
- 项目全量 331 项检查通过, 包含所有已完成批次. 本轮修改的 25 个 Markdown 页面与 25 个 YAML 页头另通过当前实例 GuideME 原生解析器 / SnakeYAML.
- 任务书 51 文件 / 4178 键结构检查通过. 33 个新覆盖文件已合入发布资源包.
- 已安装 126 个明确清单文件并逐文件备份, 保持汉化资源包最高优先级. 备份目录和哈希见 install-result.json, 最新安装总记录见 dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json. 安装后 release_pack.py check 通过.
- 未启动或操作客户端. 826 处静态候选不等于已完成 826 处游戏内渲染验收. 动态 KubeJS, 条件配方, 标签解析, 客户端同步和加载优先级仍须实测. 重启客户端后重点检查 AE2 处理器, 工业奇械合金, 极光相关页, 两本 Oracle Index 目录及四本 Patchouli 首页.

本轮随后追加钠第 316 批, 当前全项目共 334 项检查通过, 单元回归为 14 项. 最新发布包包含本页全部修复与 Sodium 的 105 个语言键; 后续安装备份和覆盖核验见 `../ordinary/batch-316/install-result.json` / `installed-coverage.json`.
