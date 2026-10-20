---
navigation:
  parent: example-setups/index.md
  icon: minecraft:cobblestone
  title: 刷石机
categories:
  - example
---

# <a name="cobblestone-generator" /> 刷石机

刷石机是<ItemLink id="breaker" />最简单的用途.
如下所示, 将破坏器放在刷石机前方.

<GameScene zoom="5" interactive={true} paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/cobble_gen.snbt" />
  <IsometricCamera yaw="200" pitch="30" />
  <RemoveBlocks id="minecraft:sandstone" />
  <RemoveBlocks id="minecraft:sandstone" />
  <RemoveBlocks id="minecraft:stone" />
</GameScene>

将破坏目标设为`minecraft:cobblestone`, 红石
模式设为 **低电平** , 使其持续启用.

![破坏器界面, 目标过滤设为圆石](../assets/images/breaker_cobblestone.png)

若网络中有<ItemLink id="terminal" />, 也可使用下面的
脚本实现相同效果, 并同时控制多个破坏器.

<LuaCode>
```lua
local breaker_1 = network:get("breaker_1")
scheduler:second(function()
    breaker_1:mine() -- 持续开采
end)
```
</LuaCode>
