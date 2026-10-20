# 第 061 批: compressium

## 范围

Compressed blocks: 20 materials x 9 tiers.

- 语言键: 180, 唯一英文文本 180
- 中文值: 180, 保留的非正文值: 0
- 英文源: `.minecraft/mods/compressium-26.1.2.1.jar` 的 `assets/compressium/lang/en_us.json`
- 产物: `.minecraft/kubejs/assets/compressium/lang/zh_cn.json`
- 校验: `verification.json` (`in_game_tested: false`)

## 术语与处理

上游 zh_cn 使用 block.* 键而英文源使用 item.* 键, 键名不一致导致这些方块在游戏内仍是英文; 本批补 item.* 键, 名称沿用上游既有中文 (如 压缩铁块, 压缩钻石块).

## 待办

游戏内验收未做, 需在目标实例确认名称宽度, 悬停换行与格式码渲染.
