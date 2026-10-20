---
navigation:
  parent: lua-api/index.md
  title: CardHandle
  icon: blank_card
categories:
  - api_types
description: reference to a single card in a network
---

# <a name="CardHandle" /> <a name="cardhandle" /> CardHandle

引用网络中的一张卡片. 可通过[`network:get(alias)`](network.md#get)取得,
也可从[HandleList](handle-list.md)取得, 它由[`network:getAll(type)`](network.md#getAll)返回.

<ItemImage scale="6" id="blank_card" />

---

## <a name="Properties" /> <a name="properties" /> 属性

- **`.name`**
  - 卡片别名, 与终端侧栏中的名称相同

---

## <a name="inventory-cards" /> 物品栏卡片 <ItemImage scale="0.5" id="nodeworks:storage_card" /> <ItemImage scale="0.5" id="nodeworks:io_card" />

*适用于IO卡和存储卡.* 两者提供相同Lua API,
区别在于网络如何对待它们所连接的方块. 世界中的
具体行为见<ItemLink id="storage_card" />和<ItemLink id="io_card" />
页面.

### <a name="face" /> face

将访问范围限制为相邻方块的指定面, 适合各面
提供不同物品栏的方块, 例如熔炉的输入与输出.

默认选择卡片所朝向的面.

<GameScene zoom="5" interactive={true} paddingLeft="50" paddingRight="60">
  <ImportStructure src="../assets/assemblies/furnace_and_terminal.snbt" />
  <BoxAnnotation min="0 0.9 0" max="1 1.1 1" color="#00ff00">
    `card:face("top")`
  </BoxAnnotation>
  <BoxAnnotation min="1.1 0 0" max="0.9 1 1" color="#00ff00">
    `card`
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
local card = network:get("io_1")
card:insert(coal)
card:face("top"):insert(inputItem)
```
</LuaCode>

### <a name="slots" /> slots

按槽位索引将卡片访问范围限制为指定槽位, 索引从1开始.

<ItemGrid>
  <ItemIcon id="minecraft:cobblestone" />
  <ItemIcon id="minecraft:stone" components="minecraft:enchantment_glint_override=true,custom_name=Selected" />
  <ItemIcon id="minecraft:oak_planks" />
  <ItemIcon id="minecraft:diorite" components="minecraft:enchantment_glint_override=true,custom_name=Selected" />
  <ItemIcon id="minecraft:deepslate" />
  <ItemIcon id="minecraft:stick" />
</ItemGrid>

<LuaCode>
```lua
local card = network:get("io_1")
card:slots(2, 4):find("*") -- 选择石头和闪长岩
```
</LuaCode>

### <a name="find" /> find

扫描卡片物品栏, 寻找匹配过滤器的物品或流体. 语法与
[`network:find`](network.md#find)相同, 但范围仅限于
本卡片的槽位和储罐, 而非网络中的所有存储卡.

<LuaCode>
```lua
local coalInCard = card:find("minecraft:coal")
if coalInCard then
  print(coalInCard.count, "coal in this card")
end
```
</LuaCode>

### <a name="findEach" /> <a name="findeach" /> findEach

与[find](./card-handle.md#find)相同, 但返回[ItemsHandle](./items-handle.md)列表.
每项按物品ID及是否含NBT数据区分.

例如网络中既有附魔钻石剑, 又有未附魔钻石剑,
就会将它们分成不同条目.

<ItemGrid>
  <ItemIcon id="minecraft:cobblestone" />
  <ItemIcon id="minecraft:cobblestone" />
  <ItemIcon id="minecraft:oak_planks" />
  <ItemIcon id="minecraft:cobblestone" />
  <ItemIcon id="minecraft:oak_planks" />
  <ItemIcon id="minecraft:stick" />
</ItemGrid>

<LuaCode>
```lua
local allItems = card:findEach("*")
for _, val in allItems do
  print(val.name)
end
-- 圆石
-- 橡木木板
-- 木棍
```
</LuaCode>

### <a name="insert" /> insert

将物品或流体移 *入* 此卡片的物品栏. 要么全部装下并
完成移动, 要么完全不移动, 不会只传输一部分.
全部送达时返回`true`, 无法完全装下时返回`false`.
与[`network:insert`](network.md#insert)对应, 但仅作用于本卡片.

<LuaCode>
```lua
local coal = network:find("minecraft:coal")
if coal and card:insert(coal, 32) then
  print("stored 32 coal in this card")
end
```
</LuaCode>

### <a name="tryInsert" /> <a name="tryinsert" /> tryInsert

类似[`insert`](card-handle.md#insert), 但尽可能移动能装下的部分,
不要求全部成功. 返回实际送达数量, 范围为0至请求数量.
未能装下的部分留在来源中, 适合允许部分传输的情况.

<LuaCode>
```lua
local coal = network:find("minecraft:coal")
if coal then
  local moved = card:tryInsert(coal)
  print("moved", moved, "of", coal.count, "coal")
end
```
</LuaCode>

### <a name="count" /> count

返回本卡片物品栏中匹配过滤器的
总数量, 流体以mB计.

过滤语法与[find](network.md#find)完全相同.

<LuaCode>
```lua
print(card:count("#minecraft:coals"))
```
</LuaCode>

---

## <a name="redstone-card" /> 红石卡 <ItemImage scale="0.5" id="nodeworks:redstone_card" />

*仅适用于<ItemLink id="redstone_card" />.* 上述物品栏方法不适用,
红石卡的`card:find()`为nil.

### <a name="powered" /> powered

输入红石信号大于0时返回`true`.

<GameScene zoom="5" interactive={true} paddingTop="10" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/redstone_read_lever.snbt" />
  <BoxAnnotation min="1.2 0.2 1.2" max="1 0.8 1.8" color="#F53B68">
    <ItemImage id="nodeworks:redstone_card" />
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
local card = network:get("redstone_1")
print(card:powered())
-- true
```
</LuaCode>

### <a name="strength" /> strength

返回输入红石信号强度, 范围0至15.

<GameScene zoom="5" interactive={true} paddingTop="10" paddingBottom="40" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/redstone_read_strength.snbt" />
  <BoxAnnotation min="3.2 1.2 0.2" max="3 1.8 0.8" color="#F53B68">
    <ItemImage id="nodeworks:redstone_card" />
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
local card = network:get("redstone_1")
print(card:strength())
-- "14"
```
</LuaCode>

### <a name="set" /> set

输出红石信号. 布尔值映射为15或0, 类似<ItemLink id="minecraft:lever" />. 数值会限制在0至15之间.

<GameScene zoom="5" interactive={true} paddingTop="10" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/redstone_set_true.snbt" />
  <BoxAnnotation min="3 1 0.2" max="4 1.1 0.8">
    强度15
  </BoxAnnotation>
  <BoxAnnotation min="4.2 1.2 0.2" max="4 1.8 0.8" color="#F53B68">
    <ItemImage id="nodeworks:redstone_card" />
  </BoxAnnotation>
  <RemoveBlocks id="minecraft:stone" />
</GameScene>

<LuaCode>
```lua
local card = network:get("redstone_1")
card:set(true) -- 如同拉杆, 输出强度15的信号
card:set(false) -- 将输出信号设为0
```
</LuaCode>

可以用数字指定输出信号强度.

<GameScene zoom="5" interactive={true} paddingTop="10" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/redstone_set_low.snbt" />
  <BoxAnnotation min="3 1 0.2" max="4 1.1 0.8">
    强度3
  </BoxAnnotation>
  <BoxAnnotation min="4.2 1.2 0.2" max="4 1.8 0.8" color="#F53B68">
    <ItemImage id="nodeworks:redstone_card" />
  </BoxAnnotation>
  <RemoveBlocks id="minecraft:stone" />
</GameScene>

<LuaCode>
```lua
local card = network:get("redstone_1")
card:set(3)
```
</LuaCode>

### <a name="onChange" /> <a name="onchange" /> onChange

注册回调, 每当输入红石信号强度变化时触发.

<GameScene zoom="5" interactive={true} paddingTop="10" paddingLeft="60" paddingRight="30">
  <ImportStructure src="../assets/assemblies/redstone_onchange.snbt" />
  <BoxAnnotation min="3.2 1.2 0.2" max="3 1.8 0.8" color="#F53B68">
    <ItemImage id="nodeworks:redstone_card" />
  </BoxAnnotation>
  <BoxAnnotation min="0 1 0" max="3 2 2">
    红石时钟/脉冲器
  </BoxAnnotation>
</GameScene>

<LuaCode>
```lua
local card = network:get("redstone_1")
-- 红石火把亮灭时打印"state changed"
local lastPowered = card:powered()
card:onChange(function(strength: number)
    local powered = strength > 0
    if lastPowered == powered then
        return
    end
    lastPowered = powered
    print("state changed")
end)
```
</LuaCode>

> **提示:** 建议开启["自动运行"](../items-blocks/scripting_terminal.md#autorun), 对应设备为<ItemLink id="terminal" />
> , 适用于`:onChange`等回调.

![](../assets/images/autorun.png)

## <a name="observer-card" /> 侦测卡 <ItemImage scale="0.5" id="nodeworks:observer_card" />

*仅适用于<ItemLink id="observer_card" />.* 上述物品栏方法
不适用, 侦测卡的`card:find()`为nil. 它会监视
安装面前方的方块, 提供ID, 属性和变化事件.

### <a name="block" /> block

返回目标位置方块的ID, 格式为`"namespace:path"`字符串.

<LuaCode>
```lua
local watcher = network:get("watcher_1")
print(watcher:block())
-- "nodeworks:celestine_cluster"
```
</LuaCode>

即使目标区块未加载, 也会返回缓存方块; Minecraft
会加载区块以读取数据. 大规模脚本应优先使用`:onChange`,
而不是每刻轮询`:block()`.

### <a name="state" /> state

返回所监视方块的属性表, 键为方块的
属性名, 如`age`, `facing`, `waterlogged`, `lit`, `axis`等. 值
根据属性类型返回数字, 布尔值或小写
字符串. 空气和其他无属性方块返回空表.

<LuaCode>
```lua
local s = network:get("watcher_1"):state()
if s.age == 3 then
    print("fully grown")
end
```
</LuaCode>

不同方块提供不同属性, `state()`的结果完全取决于
所监视的方块. 需要按方块种类分支时, 可先调用`:block()`以
确定当前检查的具体方块.

### <a name="onChange" /> <a name="onchange" /> onChange

注册回调, 在所监视方块ID或任一状态
属性变化时触发, 替换同一卡片上原有的处理器. 处理器
收到新方块ID和新属性表.

<LuaCode>
```lua
local watcher = network:get("watcher_1")
local breaker = network:get("breaker_1")

watcher:onChange(function(block: string, state: { [string]: any })
    if block == "nodeworks:celestine_cluster" then
        breaker:set(true)
        scheduler:delay(2, function() breaker:set(false) end)
    end
end)
```
</LuaCode>

注册后的首次轮询只会静默记录初始状态.
因此脚本重启时, 不会对早已进入最终形态的方块
触发虚假的变化事件.

> **提示:** 与红石`:onChange`相同, 此类回调通常需要
> 自动运行. 在以下位置开启["自动运行"](../items-blocks/scripting_terminal.md#autorun):
> <ItemLink id="terminal" />, 使处理器在重新登录后继续响应.
