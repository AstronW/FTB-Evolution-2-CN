# 第 316 批: 钠 (Sodium) 0.9.2 设置界面

目标实例来自 project.json, FTB Evolution 2 1.4.0 / Minecraft 26.1.2. 当前发行 JAR 为 sodium-neoforge-0.9.2+mc26.1.2.jar, 实际主体位于 META-INF/jarjar/net.caffeinemc.sodium-neoforge-0.9.2+mc26.1.2-mod.jar. 主体内只有 en_us.json, 共 105 个键 / 101 个独立值. 既有整合汉化包没有 Sodium 覆盖. 之前的外层 JAR 扫描漏掉这个命名空间, 是此次遗漏的原因.

已补齐全部 105 个键, 包括四个设置分页, 各选项和悬停描述, 各档取值, 性能影响, 搜索, 按钮及界面可见提示. 不改图形设置值, 配置行为或模组 JAR. 纯日志/错误堆栈没有额外扩展范围, 仅维护原生语言表中可见的提示键.

## 来源审校

- 当前有效英文为内嵌 JAR 的 assets/sodium/lang/en_us.json. manifest.json 固定外层及内层 SHA-256, source-en_us.json 固定当前键与原文. 构建直接只读内嵌 JAR, 不分发原模组.
- 对照本地 CFPA 当前提交的 Sodium 1.16 / 1.18, Rubidium 1.18 与 Embeddium 1.20. 不把描述里的旧行为带入新版本. 原文相同也逐项审阅, 例如旧译把帧率误标为 TPS, 已按当前英文修正.
- 19 个经审阅的短标签复用本地 CFPA 译名; 38 个有本地候选的键按当前原文重新适配; 48 个键按当前源文翻译. 另逐键对照两个未合并 PR 的候选, 不整文件覆盖.
- [CFPA PR #4962](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/4962), DHJComical, head 46c8541b9e67741e501987e9d31de7719ee843ae: 有 58 个同键候选, 其中 55 个英文完全相同. 检查评论中流畅/高品质, 树叶透明关系及纹理术语建议. 当前项目使用半角标点, 不采用中文引号建议. 本批没有直接采用整份 PR 文件.
- [CFPA PR #3675](https://github.com/CFPAOrg/Minecraft-Mod-Language-Package/pull/3675), Ginsway, head 864beef0b60f87963ab815d25481e5fa70ccfbbb: 审阅 1.20-fabric 候选, 53 个同键, 34 个原文相同. 旧版生物群系混合值只有一个占位符, 不能应用到当前 `%sx%s Blocks` 的两个占位符. 当前两个 %s 均保留.
- PR #6054 的 288 个迁移文件已逐页检索, 不含 sodium 命名空间变更. 原始 API 搜索/评论/文件清单及固定 head 的候选文件在 pr-sources/, 哈希见 review-inputs.json.
- 所有当前键的原文, 候选, 比较及采用范围见 source-review.json. CFPA CC BY-NC-SA 4.0 许可与发行包现有署名保留, 原始仓库未改写.

## 校验

```bash
python localization/ordinary_translation.py batch-316 --build
python localization/ordinary_translation.py batch-316
python -m unittest discover -s localization/tests
python project.py check
python localization/release_pack.py build
python localization/release_pack.py check
python localization/release_pack.py install --enable
python localization/release_pack.py check
```

105/105 个键通过当前源文, 格式占位符, 换行, 数值, 单位, 字面标识和半角标点检查. 5x5, OpenGL 4.4, ARB_buffer_storage, NVIDIA 驱动版本 536.23 等按原文保留. 新增三个回归用例验证内嵌语言读取及内外 JAR 变动时拒绝未审阅输入.

最终发布包及安装校验记录见本目录 build/check/install 记录. 静态覆盖与安装哈希不代表游戏内排版验收; 重启客户端后检查 视频设置 中的分页, 全屏模式, 区块更新, 透明方块细分, 流体和纹素插值选项及其说明.

已完成全项目 334 项检查与 14 项单元回归. 已重新构建并安装, 126 个清单文件全部先备份; 安装包内 Sodium 覆盖实测为 105/105 键, 缺失列表为空, 见 installed-coverage.json. 这里的实测是文件与哈希核对, 不是游戏内 UI 实测.
