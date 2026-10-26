# 第 347 批: MFFS Fortron 名称覆盖

2026-10-23 用户裁决: 所有 Fortron 统一为福特朗, Fortron Capacitor 为福特朗能量储存器. 当前 `mffs-5.8.39.jar` 自带 `zh_cn.json` 的 5 个键保留英文 Fortron, 本批以项目覆盖改写, 其余官方中文不动. 逐键英文、官方中文与本批译文见 `source-review.json`.

- `block.mffs.coercion_deriver` 官方 Fortron 衍生器 → 福特朗衍生器. 手册仍称强制推导机, 本批只统一 Fortron, 未裁决该机器名.
- `screen.mffs.fortron.tooltip` 补出原文 force energy 的"力场"; 句末改半角标点.

## 验证

- `python localization/ordinary_translation.py batch-347 --build`: 英文源与 JAR 一致, 占位符、数值与标点检查通过.
- 输出 `.minecraft/kubejs/assets/mffs/lang/zh_cn.json`; 未修改 JAR, 未游戏内验收.
