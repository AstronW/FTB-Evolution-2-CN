# 1.5.1 增量适配与校验输入修复

目标: project.json 指定的 FTB Evolution 2 1.5.1 / Minecraft 26.1.2 / NeoForge 26.1.2.121. 本次仅写可维护译文、来源快照、工作副本及发布包, 未安装到游戏, 未游戏内验收. 更新前检查见 `../../reports/update-1.5.1-assessment.md`.

## 分批成果

| 阶段 | 结果与证据 |
| --- | --- |
| 任务书 | 51 文件 / 4193 键 / 8205 片段全部解决. 新增 12 个护甲示例标签, 适配 5 个修改键. `quest-translations.json` 逐条绑定当前英文, `quest-deltas.json` 记录生成片段. 新结构只用于工作副本输入, 不随安装包覆盖任务结构. |
| 特色文案 | 自定义第 006 批修正 +3 徒手伤害. 既有 42 条未变来源复核复用. 新绑定 `../../custom/source-bindings-1.5.1.json`; 第 001-005 批版本标签保留来源语义, 不为升级伪造历史批次. |
| 关键手册 | 27 个当前核心页面有源变更, 含迁移后的物品移动页和新增多配方加工处理器页; 168 个片段逐条审阅. 现有不变段落按旧英文匹配复用. 全部核心范围 165 页. `core-manual-translations.json` / `core-manual-deltas.json`. 优先理由: Nodeworks 自动合成主线与跨机器处理接口、FTBIC 主线合金页, 直接影响任务推进和基本操作. |
| 其他手册增量 | Nautec 两种生物反应机的菌落替换逻辑, Stellaris 罐头与流体单元的饮水要求, 共 4 页 / 6 个变化行. `extra-manual-translations.json` / `extra-manual-deltas.json`. 补充手册共 317 页 / 97009 近似英文词. |
| 普通语言 | 5 个既有已选覆盖键更新: 动态修复参数 3 键、Spirit Attuned 名称、Demonic 描述. `language-translations.json`、`../../ordinary/overlay-revisions.json`. 原 332 批逐源比对后携带, `ordinary-rebind.json` 保留差异和原件指针. |
| 新观察语言 | 第 338-346 批处理 45 个原生中文缺口及 1 条控制器消息改写. 42 个新观察键复用当前模组原生中文, 不额外生成易陈旧的覆盖. `new-language-review.json`. Neo Vitae 20 条变化键复核原生中文, `native-language-review.json`. |

Nodeworks 硬编码 UI 保持英文. 手册正文、语言 JSON 和提示按既有范围处理. 不改变配方、任务逻辑、JAR、CFPA 原件或玩家数据. DeepNull 等失效键和旧特性兼容译文未为凑统计主动清理; 无法从语言文件找到旧键时保留兼容输出并记录, 不推断注册内容被删除. FancyMenu 图片内嵌文字仍属既存未完成项.

## 来源与复用

- `before/` 保存被修改的 1.4.1 可维护输入与必要输出原件, 历史报告未覆写.
- 为获得可靠英文逐行差异, 从官方发布 ZIP 的 manifest 定位 Nodeworks 0.10.6, 下载后与此前记录的 JAR SHA-256 完全匹配. 仅文本快照进入 `old-sources/`, JAR 保留在仓库外. URL 与校验证据见 `historical-download.json`.
- 当前核心英文全文另保存为 `../../manuals/sources/`, 今后无需依赖被更新器删除的旧 JAR 来匹配段落. 当前变更页的原始字节另见 `sources/`.
- 当前 CFPA 固定提交及所有版本目录、已缓存固定 PR 的精确新键检索未命中; `cfpa-candidate-search.json` 记录检索范围. 未声称实时穷尽未来上游 PR. 新术语沿用既有项目上下文, 原生中文优先复用. 原生第三方许可与 CFPA 署名继续随包保留.
- Witchery 两个相关类及 Mystical Agriculture 缓降升级类的当前 javap 输出与旧证据逐字相同, 保留在 `code-evidence/`. 代码勘误改绑相关 class 字节, 无关类更新不再触发整 JAR 失效.

## JAR 版本相关检查的修复

`../../source_archive.py` 将模组身份与资源身份分开: 从当前目标实例读取顶层/递归嵌套资源, 按 mod ID 定位唯一提供者, 按资源路径与已审阅 SHA-256 验证内容. 保留完整外层、内层 JAR 哈希作为来源证据, 不将无关二进制变化等同于英文变化.

- 普通语言全部 341 个当前批次、Companion 任务名称和补充手册使用资源绑定. 第 117 批直接读取 AuthMe 的嵌套英文资源, 不要求事先提取旧 JAR 副本.
- 模组显示名按当前 mod ID 和实际英文/中文证据验证. 运行时兼容脚本仍锁定实际相关 class 字节, 不放松 API 校验.
- CFPA 官方修订输入分别校验原生中文资源与许可证; 反馈覆盖校验实际目录元数据、book 原文、基础产物、输出及非 JAR 配置/配方来源. JAR 全包哈希仅作 provenance, 不再因改名或无关内容变化失败.
- 不存在来源时拒绝; 同一 mod ID 安装两份版本时拒绝; 无法确定的嵌套来源拒绝. 不回退读取目标实例之外的旧 JAR. 不创建旧文件名别名或自动接受新英文.
- `python project.py check` 在整合包版本与项目基线不同时, 输出一次 `needs_source_review`, 提供审计入口, 返回 2; 不继续产生数十个旧输入失败. 审阅适配后才运行当前版本全量检查.
- 发布元数据独立放在 `../../release.json`. 一键打包不读取 project.json、实例、模组 JAR、CFPA 或安装记录.

## 校验与发布

最新结果见 `../../reports/project-verification-1.5.1.json`、`../../reports/source-only-build-1.5.1.json` 和 `../../reports/release-pack-1.5.1.md`. 版本改名、嵌套输入、真正英文变化、无关外层变化、重复 mod ID、旧实例回退、反馈资源漂移与版本预检均有回归检查. 初始 47 项失败已修复, 未通过关闭断言获得结果. 全量入口让普通语言批次在同一 Python 进程中复用只读 JAR 索引, 每批仍独立记录结果与异常, 任一批失败不会跳过后续批次.

构建更新工作副本, 发布工具只打包明确清单. 未对游戏重新应用被更新器还原的 6 个中文文件; 它们对应的译文已进入 1.5.1 安装包, 后续应按发布工具清单备份安装. 未进行客户端资源重载、悬停、手册导航、配方显示或交互验收.
