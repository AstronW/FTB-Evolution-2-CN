# FTB Evolution 2 1.5.1 简体中文汇总包

本次基于实际 1.5.1 实例更新任务书、自定义提示、语言及手册, 并修复 JAR 版本变化引起的额外静态检查失败. [适配与来源记录](../updates/1.5.1/README.md) 包含逐批差异、术语、复用与检查边界.

## 发布内容

- `dist/FTB-Evolution-2-1.5.1-zh_CN.zip`: 语言和资源型手册覆盖.
- `dist/FTB-Evolution-2-1.5.1-zh_CN-install.zip`: 完整安装包, 含内层资源包 ZIP、任务书中文、整合包中文数据、Stellaris 手册数据包及运行时提示脚本.
- `dist/FTB-Evolution-2-1.5.1-zh_CN-manifest.json`: 成员清单与 SHA-256. 两个 ZIP 另有 `.sha256` 文件.

汇总包共 31648 个语言键、95 个独立分组名称、991 个手册/书籍资源文件、51 个任务书中文文件、64 个整合包数据文件、7 个运行时脚本. 资源文件包含书籍结构及目录元数据, 不将 991 个文件称为 991 页. 任务书单独包含 4193 个语言键; 语言、页面、字段和分组数不相加.

## 构建与校验

```bash
python project.py check
python build.py
```

全量源文静态检查 363 项全部通过, 完整输出见 [project-verification-1.5.1.json](project-verification-1.5.1.json). 发布产物成员与内容哈希、ZIP CRC 校验通过. 独立纯源码副本移除 project.json, 不包含游戏实例、模组 JAR、CFPA 检出、dist 历史安装记录或本机依赖, `python build.py` 通过; 详见 [source-only-build-1.5.1.json](source-only-build-1.5.1.json). 未执行 Windows 原生环境测试.

当前 165 页核心手册通过 GuideME 原生解析与 AST 结构对照; 317 页补充手册通过来源、格式、链接与内容检查. 其他既有来源、CFPA、任务书、运行时脚本和批次检查均纳入全量入口. 静态候选与结构通过不等于实际客户端配方或布局已验收.

## 安装状态

**本次尚未安装到游戏, 尚未游戏内验收.** 更新器恢复为英文的 6 个对话/提示文件, 对应中文已在完整安装包中. 使用前关闭游戏并备份; 按安装包内 INSTALL.md 合并明确文件, 资源包 ZIP 保持压缩并启用为最高优先级.

维护者可在确认 project.json 指向当前 1.5.1 实例后运行 `python localization/release_pack.py install --enable`, 工具会按清单备份并安装; `revert` 按本地安装记录还原. 不整体复制工作副本, 不用旧任务结构覆盖当前任务, 不覆盖未列入载荷的新版配方或玩家数据. 本次未创建 1.5.1 安装记录.

FancyMenu 图片文字、既定排除模组与硬编码英文边界保持既有状态, 不因本次适配宣称全部游戏内界面已完成.
