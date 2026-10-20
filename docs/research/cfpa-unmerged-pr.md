# CFPA 未合并 PR 翻译的使用

核查日期：2026-10-17。目标为 FTB Evolution 2 1.4.0 / Minecraft 26.1.2。本次仅研究，未下载或应用 PR，未修改 CFPA。

## 已核实事实

- 未合并不是技术障碍：GitHub 明确支持取得 PR 提交并在本地测试。官方命令为 `git fetch origin pull/ID/head:BRANCH_NAME`，也可使用 `gh pr checkout PULL-REQUEST`。[GitHub 文档](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/checking-out-pull-requests-locally#modifying-an-inactive-pull-request-locally)
- PR API 的 `GET /repos/{owner}/{repo}/pulls/{pull_number}` 返回 `head.sha`、`diff_url`、`patch_url`；使用 `Accept: application/vnd.github.diff` 可取得差异。应记录 head SHA 以固定来源。[API 文档](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request)
- CFPA 使用 CC BY-NC-SA 4.0。复用和修改应保留署名及许可链接、标记修改；分享改编译文时须遵守非商业性和相同方式共享要求。[CFPA 授权说明](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package#授权方式)、[许可条款](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- GitHub 规定向有许可证的仓库贡献内容时原则上沿用该许可证，独立协议可能优先。因此 PR 应逐项查看许可和来源声明，不能仅凭“公开可下载”判断。[GitHub D.6](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#6-contributions-under-repository-license)
- CFPA 按模组先选目标版本，再依次查回退版本，只选第一个存在的版本；局域 `packer-policy.json` 可显式引用其他版本或文件。[打包规则](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/blob/main/Packer-Doc.md#全局配置文件)
- 本地上游快照 `719672954d9df4ea51877e3d5ce2912148273682` 的 26.1 配置回退顺序是 1.21、1.20、1.19，不能简单把各版本目录全部叠加。[配置](../../CFPA/config/packer/26.1.json#L17)、[固定提交来源](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/blob/719672954d9df4ea51877e3d5ce2912148273682/config/packer/26.1.json#L17-L21)

## 本项目建议

可以把 PR 作为可追踪的候选译文层。先按新实例实际 JAR 的命名空间、英文语言键和原文筛选，再检查 JSON、占位符、格式码及审查意见；同键英文变化需复核。优先级建议为本项目人工修订 > 经核验的 PR 译文 > 按上游规则选出的 CFPA 基线；PR 默认只补缺，冲突单列。记录 PR 编号、作者、路径、head SHA、采纳键和修改说明，方便撤回及合并后去重。手册另外验证其版本结构，不套用语言键合并。

当前公开列表可见未合并的 [#6145 Nemo's Inventory Sorting](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/6145) 标为 26.1.x；这仅说明存在候选，未确认本包安装该模组或译文可直接使用。[PR 列表](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pulls)
