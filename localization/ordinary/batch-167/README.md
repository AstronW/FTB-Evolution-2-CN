# 第 167 批: puffish_skills

## 范围

Official zh_cn gaps: shop point label, cost tooltip and command feedback

- 语言键: 8, 唯一英文文本 8
- 中文值: 8, 保留的非正文值: 0
- 英文源: `.minecraft/mods/puffish_skills-0.19.2-26.1-neoforge.jar` 的 `assets/puffish_skills/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/puffish_skills/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

命令反馈必须保持占位符的文本顺序, 因此写成 已添加 %s 级到分类 %s, 归属 %s 的句式, 不按中文语序调换.

## 待办

游戏内验收未做, 需在目标实例确认名称长度, 悬停换行与格式码渲染.
