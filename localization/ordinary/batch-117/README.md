# 第 117 批: resourcefulconfig

## 范围

Dedicated server properties screen and shared UI constants.

- 语言键: 32, 唯一英文文本 32
- 中文值: 31, 保留的非正文值: 1
- 英文源: `localization/vendor/jar-in-jar/resourcefulconfig-neoforge-26.1-4.0.1.jar` 的 `assets/resourcefulconfig/lang/en_us.json`
- 来源说明: Jar-in-jar: .minecraft/mods/authme-neoforge-9.2.1+26.1.jar!META-INF/jars/resourcefulconfig-neoforge-26.1-4.0.1.jar, extracted to localization/vendor/jar-in-jar/resourcefulconfig-neoforge-26.1-4.0.1.jar for batch checking
- 产物: `.minecraft/kubejs/assets/resourcefulconfig/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

Jar-in-jar (authme 内嵌), 校验用解包副本; 服务端属性沿用原版用语: 白名单/每日消息/允许飞行/玩家对战.

## 待办

游戏内验收未做, 需在目标实例确认界面文案长度, 悬停换行与格式码渲染.
