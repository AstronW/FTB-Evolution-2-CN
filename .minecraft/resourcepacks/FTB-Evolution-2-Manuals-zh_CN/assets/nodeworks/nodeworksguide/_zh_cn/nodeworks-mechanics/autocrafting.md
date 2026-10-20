---
navigation:
  parent: nodeworks-mechanics/index.md
  title: 自动合成
  icon: crafting_core
categories:
  - mechanic
---

# <a name="auto-crafting" /> 自动合成

自动合成能把"想要64把铁镐"变成实际的64把铁镐.
告诉网络有哪些配方, 在网络中储备原料,
再由<ItemLink id="crafting_core" />执行制作.

<GameScene zoom="2" interactive={true} paddingTop="5" paddingLeft="30" paddingRight="30">
  <IsometricCamera yaw="160" pitch="20" />
  <ImportStructure src="../assets/assemblies/autocrafting_example.snbt" />
</GameScene>

## <a name="getting-it-working" /> 搭建自动合成

需要四类组件, 且都位于同一网络:

1. **CPU.** 放下<ItemLink id="crafting_core" />, 至少连接一个
   <ItemLink id="crafting_storage" />, 再将核心连到
   <ItemLink id="node" />. 参阅[合成CPU](../items-blocks/crafting_cpu.md),
   了解增加缓存, 冷却块和基板等扩展.
2. **配方.** 将每个配方写入
   <ItemLink id="instruction_set" />(原版3×3合成)或
   <ItemLink id="processing_set" />(其他配方), 再放入
   <ItemLink id="instruction_storage" />或
   <ItemLink id="processing_storage" />, 并接入网络.
3. **原料.** 原材料必须位于[网络存储](./network-storage.md). 通过<ItemLink id="storage_card" />接入的任意箱子都有效.
4. **请求方式.** 使用<ItemLink id="inventory_terminal" />手动
   点击, 或在<ItemLink id="terminal" />上运行脚本,
   调用`network:craft(...)`.

全部就绪后, 网络可制作的物品会显示在物品终端中, 可用过滤器或按住左Alt显示加号图标; `network:craft("...")`会返回
构建器, 而非nil.

## <a name="requesting-a-craft" /> 发起合成

### <a name="from-the-inventory-terminal" /> 通过物品终端

打开终端, 找到物品并`Alt+click`. 输入数量后确认.
终端顶部的 **合成队列** 显示所有排队物品. 合成
完成后, 该物品会带有小标记, 供你取走. 下次
打开终端时, 它会与其他物品一起显示.

按住`Alt`可突出显示网络掌握的所有自动合成物品,
即使当前库存为零也会显示.

### <a name="from-a-script" /> 通过脚本

脚本可通过`network:craft`排队合成, 并指定产物去向:

<LuaCode>
```lua
-- 产物就绪后会自动存入网络存储
network:craft("minecraft:door")
```
</LuaCode>

也可链式调用`:connect(fn)`, 在合成完成时立即执行自定义代码.

<LuaCode>
```lua
local furnace = network:get("someFurnaceCard")
network:craft("minecraft:charcoal"):connect(function(item: ItemsHandle?)
  if item then
    furnace:insert(item)
  end
end)
```
</LuaCode>

完整API见[network:craft](../lua-api/network.md#craft)和[CraftBuilder](../lua-api/craft-builder.md).

## <a name="cancelling-a-craft" /> 取消合成

右击<ItemLink id="crafting_core" />打开界面. 有任务运行时会显示 **"取消"**
按钮. 点击后中止合成,
将缓存中的全部物品返还网络存储, 并释放CPU.

## <a name="processing-sets-need-a-handler" /> 加工配方集需要处理器

<ItemLink id="instruction_set" />配方可以直接运行. 原版3x3合成
是完整独立的操作, CPU知道如何执行.

<ItemLink id="processing_set" />则不同. 加工配方集仅 *声明*
配方, 例如"8个粗铁变成8个铁锭", 却不知道 **如何**
实际完成转换. 必须有某个对象将粗铁放入熔炉,
再取出铁锭, 这个对象就叫 **处理器** .

有两种注册方式:

### <a name="with-a-processing-handler-block" /> 使用加工处理器方块

<GameScene zoom="5" interactive={true}>
  <IsometricCamera yaw="200" pitch="20" />
  <ImportStructure src="../assets/assemblies/basic_processing_handler.snbt" />
  <BoxAnnotation min="0 2 0" max="1 2.25 1" color="#3C44AA">
    蓝色频道存储卡朝向熔炉顶面.
  </BoxAnnotation>
  <BoxAnnotation min="0 0.75 0" max="1 1 1" color="#B02E26">
    红色频道存储卡朝向熔炉底面.
  </BoxAnnotation>
</GameScene>

将<ItemLink id="processing_handler" />接入网络, 在界面中绑定
配方. 将背面接入主网络, 再从正面引出小型
管道子网, 连接实际执行配方的机器.
CPU会代你控制机器, 无需编写脚本. 对大多数
"从一侧输入, 从另一侧输出"的机器,
这是合适的选择.

### <a name="with-a-scripted-handler" /> 使用脚本处理器

需要自定义时序, 条件路由或多步骤
流程时, 可在<ItemLink id="terminal" />上编写Lua处理器:

<LuaCode>
```lua
local furnace = network:get("someFurnaceCard")
network:handle("...", function(job: Job, inputs: InputItems)
  -- 将粗铁送入熔炉顶面, 如同上方的漏斗
  furnace:face("top"):insert(inputs.rawIron)
  -- 等待产物出现, 再从熔炉底部取出, 如同下方的漏斗
  job:pull(furnace:face("bottom"))
end)
```
</LuaCode>

若尝试自动合成需要加工配方集但未注册处理器的物品,
合成会失败, 并提示哪个配方缺少处理器.

完整编写方式见[network:handle](../lua-api/network.md#handle), [Job](../lua-api/job.md)和
[InputItems](../lua-api/input-items.md).

## <a name="when-something-goes-wrong" /> 故障排查

合成失败时, <ItemLink id="crafting_core" />周围会反复
出现红石粉尘粒子云, 直至
打开核心界面关闭错误提示, 或
发起新的合成并成功完成. 出现异常时, 可先找红色粉尘,
核心本身就是最快定位哪个CPU
报错的方法.

![](../assets/images/crafting_cpu_erroring.png)

CPU报告的具体消息包括:

| 消息 | 含义 |
| -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 位于(x, y, z)的合成CPU未组装 | 核心未接触<ItemLink id="crafting_storage" />, 或核心未接入网络. |
| 缺少原料: N×物品, ... 没有可用配方且存储不足. | 网络无法取得这些物品, 也没有生产它们的配方. 请在联网箱子中补货, 或编写配方. |
| 未为X注册处理器. 请在已连接终端的脚本中添加`network:handle("recipe", ...)`调用. | X是没有Lua处理器的加工配方集. 见上方[加工配方集需要处理器](./autocrafting.md#processing-sets-need-a-handler). |
| 合成需要N种不同物品, CPU只能容纳M种. 请增加缓存或升级等级. | CPU的<ItemLink id="crafting_storage" />数量不足, 无法容纳合成中间步骤所需的不同物品类型. 请增加缓存. |
| 合成缓存中一种物品最多需要N个, CPU只能容纳M个. 请升级缓存等级或增加方块. | 同类问题的另一维度: 某一步的数量会超出缓存的单种物品容量. |
