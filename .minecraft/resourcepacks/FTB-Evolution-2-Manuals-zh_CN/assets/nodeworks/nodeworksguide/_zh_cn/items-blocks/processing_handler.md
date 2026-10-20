---
navigation:
  parent: items-blocks/index.md
  icon: processing_handler
  title: 加工处理器
categories:
  - autocrafting
description: registers a processing set handler using a micro-network
item_ids:
- nodeworks:processing_handler
---

# <a name="processing-handler" /> 加工处理器

用于以下配方的方块式处理器:
[加工配方集](./recipe_sets.md#processing-set). 将它接入
网络并绑定配方,
[合成CPU](./crafting_cpu.md)便会将原料送入
机器并取回产物, 无需编写Lua.

<GameScene zoom="5" interactive={true} paddingLeft="30" paddingRight="30">
  <IsometricCamera yaw="160" roll="0" pitch="10" />
  <ImportStructure src="../assets/assemblies/basic_processing_handler.snbt" />
  <BoxAnnotation min="0 2 0" max="1 2.25 1" color="#3C44AA">
    蓝色频道存储卡朝向熔炉顶面.
  </BoxAnnotation>
  <BoxAnnotation min="0 0.75 0" max="1 1 1" color="#B02E26">
    红色频道存储卡朝向熔炉底面.
  </BoxAnnotation>
</GameScene>

## <a name="two-sides" /> 两个侧面

处理器有正面和背面:

- **背面** 接入主网络, 其中包含
  <ItemLink id="crafting_core" />和
  <ItemLink id="processing_storage" />.
- **正面** 连接由管道, 节点和存储卡构成的独立 **微型网络** .
  处理器本身充当这一侧的控制器, 因此
  正面不需要, 也不允许放置<ItemLink id="network_controller" />
  .

将背面接入主网络, 从正面引出一小段管道,
连接实际执行配方的机器.

## <a name="binding-a-recipe" /> 绑定配方

右击处理器打开界面, 从主网络的加工配方存储器中
选择一个<ItemLink id="processing_set" />.
配方集的每种原料在界面中各有一行, 可设置
频道颜色; 配方产物另外共用一种频道颜色.

## <a name="channel-routing" /> 频道路由

处理器使用频道来决定微型网络中的
哪张<ItemLink id="storage_card" />接收各项物品:

- **输入频道** : 每种原料一个, 默认蓝色. CPU
  开始合成时, 会将各原料推送至微型网络中
  频道与该原料颜色匹配的存储卡.
    - *原料也遵守存储卡过滤器, 因此可按表达式,
    物品数据或可堆叠性进行自定义路由.*
- **输出频道** : 共用一个颜色, 默认红色. 处理器
  监视微型网络中属于该频道的存储卡,
  将成品取回主网络.

上方熔炉示例中, 顶部蓝色存储卡
接收原料, 熔炉完成加工,
底部红色存储卡收集产物.

同一台机器需要将不同原料送入不同槽位时,
可以使用不同颜色, 例如一侧送燃料,
另一侧送加工原料.

## <a name="compared-to-a-scripted-handler" /> 与脚本处理器比较

加工处理器相当于无需脚本的
[`network:handle(...)`](../lua-api/network.md#handle). 当配方只需"从一侧送入原料,
从另一侧取出产物"时, 使用此方块即可. 需要自定义
时序或多步骤流程时, 则使用脚本处理器.

## <a name="Recipe" /> <a name="recipe" /> 配方

<RecipeFor id="processing_handler" />
