# 2026-10-18 项目清理

本次清理限定于项目目录, 不访问实际游戏目录执行删除, 不跟随 .minecraft/mods 或 quest-inputs 的实例链接.

已删除:

- 项目内 .Trash-0: 23 份已被删除的旧版 remaining-1.4.0-language-detail.json. 当前压缩明细 .json.gz 已验证可正常解析并保留.
- .workbuddy/tmp: 已完成批次的临时译稿、参考导出、一次性生成/修复脚本与无用提取文件. .workbuddy/memory 保留.
- localization/cfpa_review/manuals/validation: 每次原生解析检查重新生成的源文副本、中文副本与 AST 缓存. 解析结果报告、哈希和裁决保留.
- 项目 Python 字节码缓存与残留 Java .class. 当前 Java 校验使用 .java 源文件运行.

第 117 批仍使用的 Resourceful Config 嵌套 JAR 已迁至 localization/vendor/jar-in-jar, 并更新 manifest.json 与 README 的路径. 已与当前目标实例 AuthMe JAR 中的原始条目逐字节核对一致, 未修改内容或源哈希.

保留当前译文、术语、源文快照、历史版本对照、CFPA 原件及 PR 审校证据、dist 当前发布包、安装/回退记录和最近修正前快照. 这些文件仍用于检查、来源追踪或恢复, 不因时间较早就删除.

.gitignore 已补充本地回收站、临时工作目录、Java 编译产物、生成的解析缓存与嵌套 JAR 输入.

删除清单、文件数、字节数与依赖迁移哈希见同名 JSON. 清理后的检查结果在该 JSON 的 verification 字段记录.
