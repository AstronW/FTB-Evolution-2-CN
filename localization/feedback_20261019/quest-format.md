# 任务书 & 转义修复 (2026-10-19)

已核对 `project.json` 的目标实例为 FTB Evolution 2 1.4.0, `.minecraft/mods` 指向该实例. 工作副本的全部 51 个任务书英文文件与目标实例逐字节一致. 本轮没有修改英文源、任务逻辑或术语.

全量扫描 51 文件 / 4178 键的中文任务书, 找到两处非法的普通 `&`: `chapters/gearing_up.json5` 中任务 `496903AB7E8A0A92` 的标题和第一段说明. 可维护译文片段为 233 与 347. 英文源均写作 `Iron's Gems \&\ Jewelry`, 中文误写成 `Iron's Gems & Jewelry`. 本次恢复与源文相同的转义, 显示名称仍为 `Iron's Gems & Jewelry`. 修改前的两条译文保存于 `quest-format-before.json`.

通过 `javap -c -p` 核对当前 `ftb-library-neoforge-26.1.2.9.jar` 的 `dev.ftb.mods.ftblibrary.util.TextComponentParser`:

- `parse()` 字节码偏移 146-162 判断前一字符是否为反斜杠; 转义后的 `&` 不走格式码分支.
- 偏移 360-378 对未转义的 `& ` 抛出 `Invalid formatting! You must escape whitespace after & with \\&!`. 错误消息末尾的 `!` 是报错标点.
- 格式码分支读取 `&` 后一个字符, `r` 是重置格式码. `&r!` 合法, 不需要附加空格. 未批量改动其他合法的 `&r!`.
- 支持 `0-9a-f`, `k-o`, `r`, `z` 及六位十六进制颜色. JSON 文本组件走组件解析, 其中普通 `&` 不按 FTB 格式码检查.

`quest_translation.py` 构建/检查和 `verify_quests.py` 独立检查现在都会拒绝普通文本中的未转义 `&`, 非法代码与不完整十六进制颜色. 新增 `tests/test_quest_format.py` 覆盖本次错误、转义、合法 `&r!`、彩虹/十六进制颜色与 JSON 组件中的普通 `&`. 修复前全任务书回归扫描明确报错, 修复后 5 项测试通过. 扫描未发现其他非法格式码.

版本、输入 JAR 哈希和修复范围见 `quest-format-verification.json`. 任务书构建、检查与独立结构检查均通过. 全项目检查结果见 `../reports/project-migration-verification.json`. 静态检查不能替代游戏内排版验收, 本轮未运行游戏进行可视确认.

已重新构建汇总资源包及安装包, 使用 `release_pack.py install` 按清单备份并安装到目标实例, 随后 `release_pack.py check` 通过并确认安装文件哈希一致. 备份路径及逐文件哈希见 `../../dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json`.
