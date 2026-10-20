# CFPA 开放 PR 候选审计

核查日期: 2026-10-17. 仅抓取候选与原文, 未采用或翻译任何条目, 未写 GitHub 或修改 CFPA 工作树.

## 已核实范围

- 通过 GitHub connector 只读取得 [CFPA 开放 PR API](https://api.github.com/repos/CFPAOrg/Minecraft-Mod-Language-Package/pulls?state=open&per_page=100&page=1), 4 页数量分别为 100, 100, 100, 91, 合计 391 个开放 PR. 已包含草稿, 来源版本不限. 最后一页不足 100 条. API 快照并非事务快照, 抓取期间变化仍可能导致极小时间差.
- 对全部 391 个 PR 取得跨页 changed filenames, 逐路径匹配当前目标实例 JAR 内发现的 388 个 assets 命名空间. 命中 31 个 PR / 661 个路径. 这是候选筛选, 不是人工判定每个候选均适用.
- 下载其中 649 个文本文件, 并补抓 15 个未修改但与中文配套的同目录英文语言文件和 1 个未修改的手册英文页. 请求共 665 项, 657 项成功. 7 个 404 经 PR file status 确认为已删除文件; 另 1 个为 #6123 Better Advancements 26.2 未提交同目录 en_us.json. [PR #6123](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/6123).
- 所有内容按 PR fork 的 head SHA 固定, 保留作者、路径、blob SHA、base SHA. 31 个相关 PR 另保存完整 changed-file detail, 包括 status、previous_filename 及 API 提供的 patch. [GitHub PR 文件 API](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files).

## 缓存约定

- `open-pr-pages.json`: 四页完整 PR 元数据, 含 head/base SHA、作者、草稿状态.
- `changed-files.json`: 全部 391 个 PR 的文件名结果, 未仅按标题筛选.
- `relevant-pr-index.json`: 按实际命名空间筛选的 31 个 PR 与 661 个路径.
- `relevant-pr-files-detailed.json`: 31 个 PR 的跨页详细变更, 保留原始 patch.
- `file-cache-index.json`: 所有请求与相对 `cache_file`, `status=ok` 才存在缓存文件. `change_status=removed` 是预期不可在 head 中读取的删除项. UTF-8 缓存用 `files/NNNN.txt`, 换行统一为 LF, 不视作字节级原件副本.
- `download-index.json`: 主线程语言扫描入口, 61 个 `/lang/zh_cn.json` 候选, 其中 60 个配有同 head 的 `en_us.json`; 路径为绝对路径. `group_lang` 与手册文档不在该语言入口中, 仍可从总缓存索引获取.

## 限制与下一步

本次全部当前开放 PR 均已穷举. 历史已关闭但未合并 PR 的补充检索范围见下节, 并未穷举. GitHub 之外的翻译未包括. 仅匹配已安装命名空间; 旧命名空间迁移但可人工映射的资源、嵌套 JAR 独有资源等仍可能需要额外检索. 排除的建筑装饰模组也保留候选, 由主线程按项目范围排除.

中文和英文只是候选资料, 尚未逐条审核语义、术语、占位符、许可证声明或 PR 审查意见. 缺少 head 英文不能计算为已适配覆盖; 同键但英文变化也不能直接抵扣人工工作. 候选是否采用仍遵循根目录 AGENTS.md 与 [既有 PR 来源规则](../../../docs/research/cfpa-unmerged-pr.md).

终端直接联网 DNS 失败, 实际下载均经可用 GitHub connector 完成. CFPA 原仓库与游戏实例只读, 未执行 PR 合并或安装.

## 补充: 旧目录布局与历史关闭 PR

首次筛选只处理当前布局. 随后发现早期 PR 使用 `projects/<version>/assets/<slug>/<namespace>/...`, 已对全部 391 个开放 PR 的文件清单补扫此布局, 追加 14 个相关开放 PR / 808 个文本路径. 因此最终开放候选来自 45 个 PR. 上述初次筛选的 31 个 PR 数量仅描述初次当前布局结果.

[GitHub 历史关闭未合并搜索](https://api.github.com/search/issues?q=repo%3ACFPAOrg%2FMinecraft-Mod-Language-Package%20is%3Apr%20is%3Aclosed%20-is%3Amerged&per_page=100&page=1) 返回 1351 个结果, `incomplete_results=false`. 因数量较大, 仅按主要剩余模组及 FTB/AE2 等关键词做标题定向检索, 没有声称穷举历史. 查询及原始响应保存到 `closed-target-search.json`. 命中的 16 个历史 PR 均获取 changed files, 其中 7 个有当前已装命名空间的候选文件, metadata/文件清单分别保存在 `closed-relevant-pr-metadata.json` 与 `closed-target-changed-files.json`. metadata 保存全部 7 个相关关闭 PR 的完整元信息, 候选作者及 SHA 也在总缓存索引固定.

旧布局及历史检索共追加 842 次文件请求, 全部成功. 包括 Productive Bees, Apotheosis, PneumaticCraft 旧手册, FTB 各语言、MFFS 等资源. 某些关闭 PR 的 fork 虽已删除, 其 head SHA 在 CFPA 仓库仍可读取; 成功内容按原 SHA 保存, 没有把不可读取资源计作候选.

最终总缓存索引有 1507 次请求, 1499 项成功. `download-index.json` 更新为 99 个普通语言候选, 含 2 个 `format=lang` 历史语言文件, 16 个来自关闭 PR. 新旧路径均提取真实 version/slug/namespace, 不依赖缓存 `.txt` 后缀推断原格式. 有 2 个语言候选缺少同目录英文, 只能待核验, 不能抵扣精确覆盖. 完整机器汇总见 `audit-summary.json`; `legacy-and-closed-file-cache-index.json` 保存本次追加子集.

以上是资料可获取性与源文候选盘点, 未处理历史关闭原因或审查意见, 不等于可以直接采用关闭 PR. 已合并 PR 未重复遍历.
