# FTB Evolution 2 1.4.0 汇总汉化包

将已通过静态校验的各阶段译文汇总为一个可安装的资源包加一份实例级安装清单。本文只描述汇总产物的组成、命令与边界, 不替代各阶段的原文适配记录。

## 产物

| 文件 | 内容 |
| --- | --- |
| `dist/FTB-Evolution-2-1.4.0-zh_CN.zip` | 资源包本体, 根目录含 `pack.mcmeta` 与 `assets/`, 可直接放进实例的 `resourcepacks/` |
| `dist/FTB-Evolution-2-1.4.0-zh_CN-install.zip` | 完整安装包, 按实例目录结构提供资源包 ZIP、任务书语言、整合包数据、Stellaris Wiki 数据包与运行时脚本 |
| `dist/FTB-Evolution-2-1.4.0-zh_CN-manifest.json` | 逐成员的 SHA-256 清单与统计 |
| `dist/*.sha256` | 两个 ZIP 的字节哈希, 供分发核对 |

资源包内另有 `ATTRIBUTION.md`(本汇总), `ATTRIBUTION-CFPA.md`, `CFPA-LICENSE.txt` 与 `licenses/ANIMAL-PEN-LICENSE.txt`, 保留上游署名与许可, 不把混合产物标为单一许可。

## 命令

在项目根目录运行:

```bash
python localization/release_pack.py plan      # 只汇总列出覆盖范围, 不写文件
python localization/release_pack.py build     # 生成 dist 下的 ZIP 与清单
python localization/release_pack.py check     # 复核 dist 产物及已安装结果
python localization/release_pack.py install   # 按明确清单安装到 project.json 的 target_instance
python localization/release_pack.py install --enable  # 同时写入 options.txt 启用资源包
python localization/release_pack.py revert    # 按安装记录还原被覆盖的文件
```

`install` 只写清单内的文件: 资源包 ZIP、任务书 `config/ftbquests/quests/lang/zh_cn/`、两个整合包数据文件和 5 个 KubeJS 脚本。被覆盖的原文件先备份到 `<实例>/.cn-backup-<时间戳>/`, 安装记录写入 `dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json`。不复制整个工作副本, 不修改模组 JAR、配方或存档。`check` 会按记录核对已安装文件的哈希。

`--enable` 写 `options.txt` 时把资源包**追加到列表末尾**, 不是插到开头。`resourcePacks` 数组是"最低优先级在前": 默认第一项就是 `vanilla`, 本项目手册包也是刻意放在末尾做高优先级覆盖。插到开头会被 `mod_resources` 压过, 只有末尾才能真正覆盖模组自带资源。

## 安装结果

本轮恢复飞马原文已有说明后, 已通过全项目 327 项检查和发布包检查, 并安装到 `/home/astronw/.ftba/instances/ftb evolution 2`. 按清单写入 124 个文件, 备份 62 个原有文件, 启用汇总资源包. 安装后文件哈希核验通过; 备份为 `/home/astronw/.ftba/instances/ftb evolution 2/.cn-backup-20261018-102823`, 完整记录见 `dist/FTB-Evolution-2-1.4.0-zh_CN-installation.json`. 未进行游戏内验收.

仍未进行游戏内验收: 资源优先级实际效果、物品名、任务悬停、手册翻页与链接点击都需要在简体中文客户端中实际检查. Stellaris Wiki 以服务端数据包安装, 需确认整合包实例的数据包加载与同步.

## 组成来源

汇总完全由清单驱动, 不扫描工作副本后整拷:

| 组成 | 来源清单 | 数量 |
| --- | ---: | ---: |
| 语言覆盖 | `localization/ordinary/batch-*/manifest.json`、`localization/custom/source-bindings-1.4.0.json`、`custom/batches/batch-004` 的自建键与 CFPA 审校合并 | 30,799 键 |
| 分组名称 | CFPA 审校 `collapsible_groups/group_lang` | 76 条 |
| 手册与书籍 | FTB 指南/FTBIC/Nodeworks 手册包、已审校 CFPA/PR 手册、Patchouli 可见字段、本轮 305 页 | 961 个成员, 含 674 页 Markdown/MDX |
| 任务书 | `localization/quest_translation.py` 输出 | 51 个 JSON5 文件 |
| 整合包数据 | `custom/batches/batch-001`(游商定义)、`batch-002`(支持对话框) | 2 个文件 |
| 运行时脚本 | `custom/batches/batch-004` | 5 个脚本 |

语言文件按资源包语义逐键合并, 不做整文件覆盖; 出现同键不同译时会直接报错而不是静默取一方。`group_lang` 单独保留, 不并入 `lang`。

## 覆盖边界

- 本包为本轮静态校验通过的汇总产物. 普通文本、手册语言键、分组名称与文档型手册的当前范围内剩余量均为 0, 见 [剩余汉化工作](remaining-1.4.0-summary.md)。
- 排除范围按 `localization/language_scope.json` 执行, 建筑装饰类模组不产出译文。
- 经审阅刻意保留英文的条目共 615 条(普通批次记录的 `reviewed_non_prose_values`), 多为模组名、专名与非散文串。其中如 `mtr` 的 Mod Menu 英文简介仍为英文, 属既有保留决定, 未在本轮改写。
- `power_armor` 命名空间是 1.3.2 的残留, 当前 1.4.0 无对应源且无清单, 已从产物中排除。脚本对"工作副本有输出但没有阶段清单"的情况直接断言失败, 避免不可追溯的译文混入。
- 静态校验不等同于游戏内验收。资源优先级、物品名、任务悬停、手册翻页与链接点击尚未在实际游戏会话中检查。

## 校验状态

构建前运行 `python project.py check`, 144 项检查中 143 项通过, 仅 `localization/cfpa_review/manuals/validate_native.py` 未重跑: 该脚本会先清空自己的临时目录(205 个文件), 被会话级删除保护拦截, 属环境问题而非译文问题。它的输入已由 `cfpa_review_build.py check` 复核为未变更(逐条裁决文件哈希与手册源哈希一致), 因此既有证据仍然成立。

汇总产物自身的校验: `release_pack.py check` 通过, 逐成员比对 ZIP 内容与清单; 全部 JSON 成员可解析且非空, 无路径逃逸成员; 资源包 `pack.mcmeta` 声明 `min_format` 84、`max_format` 97, 与当前 26.1.2 使用的资源包格式一致。
