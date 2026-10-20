# 特色内容第 002 批: 暂停菜单支持对话

目标 1.4.0. 翻译整合包 `ftb:issues` 原生对话的 5 个非空显示字段: 获取支持、加入 Discord、反馈问题、取消. 复用项目专名表的 Discord. 这是整合包自定义对话, 不存在模组官方/CFPA 同条目来源. 空正文与 Cancel 的末尾空格保留, 两个打开链接动作及其 URL、对话类型、列数均不变. 不接触其他玩家配置或存档.

输出 `.minecraft/datapacks/ftb/data/ftb/dialog/issues.json`. 与当前英文快照结构逐叶对比, 仅允许清单内 5 个文本字段发生变化. 未游戏内验收.

构建与检查: `python localization/custom_batches.py batch-002 --build`, `python localization/custom_batches.py batch-002`.
