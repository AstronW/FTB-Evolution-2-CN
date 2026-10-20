---
navigation:
  title: 概览
  position: 0
item_ids:
- nodeworks:nodeworks_book
---

# <a name="Nodeworks" /> <a name="nodeworks" /> Nodeworks

可编程的物流与自动化网络.

<GameScene zoom="3" interactive={false} paddingTop="30" paddingRight="30" paddingLeft="10">
  <ImportStructure src="assets/assemblies/subnet.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <RemoveBlocks id="minecraft:sandstone" />
</GameScene>

## <a name="Sections" /> <a name="sections" /> 目录

- [入门指南](./getting-started.md)
- [脚本参考](./lua-api/index.md)
- [Nodeworks机制](./nodeworks-mechanics/index.md)
- [物品与方块](./items-blocks/index.md)
- [搭建示例](./example-setups/index.md)

脚本终端的编辑器会在悬停于已记录的标识符时显示签名和
简要说明. 悬停时按<Color id="green">[ <KeyBind id="key.nodeworks.open_docs" /> ]</Color>可打开对应手册页.

有关如何扩展本手册, 请参阅[编写文档](https://github.com/damienfamed75/nodeworks/blob/main/docs/authoring.md)
中的编写说明.
