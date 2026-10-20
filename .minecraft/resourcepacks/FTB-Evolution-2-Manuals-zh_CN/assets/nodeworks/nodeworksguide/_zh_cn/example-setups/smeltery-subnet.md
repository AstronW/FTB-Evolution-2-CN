---
navigation:
  parent: example-setups/index.md
  icon: minecraft:furnace
  title: 冶炼子网
categories:
  - example
---

# <a name="smeltery-subnet" /> 冶炼子网

专用子网能将网络职责分开,
并复用配方.

<GameScene zoom="3" interactive={true} paddingLeft="30" paddingRight="30" paddingTop="20">
  <ImportStructure src="../assets/assemblies/roundrobin_smeltery_subnet.snbt" />
  <IsometricCamera yaw="200" pitch="20" />
  <BoxAnnotation min="0 0.75 0" max="3 1 1" color="#B02E26">
    <ItemImage id="storage_card"/>红色存储卡从熔炉取出成品.
  </BoxAnnotation>
  <BoxAnnotation min="1 3 1" max="2 3.25 2" color="#3C44AA">
    <ItemImage id="storage_card"/>蓝色存储卡接收加工处理器的所有原料.
  </BoxAnnotation>
  <BoxAnnotation min="0 2 0" max="3 2.25 1" color="#80C71F">
    <ItemImage id="storage_card"/>黄绿色存储卡接收输入箱轮询分配的物品.
  </BoxAnnotation>
  <BlockAnnotation x="1" y="2" z="1">
    已开启轮询.

    频道设为<Color id="green">黄绿色</Color>.
  </BlockAnnotation>
</GameScene>

上方是 **冶炼** 子网示例, 其中的<ItemLink id="processing_storage" />通过<ItemLink id="broadcast_antenna" />广播配方. 任意
网络都可用<ItemLink id="link_crystal" />配对, 调用这些配方.

接着使用三台<ItemLink id="processing_handler" />, 分别绑定网络中的三个加工
配方集, 全部将原料推送到<ItemLink id="import_chest" />.
输入箱设为轮询, 将物品送往另一频道的存储卡,
这些存储卡专门朝向各熔炉顶面.
另外用红色存储卡朝向熔炉底面.

更多信息见[自动合成](../nodeworks-mechanics/autocrafting.md).
