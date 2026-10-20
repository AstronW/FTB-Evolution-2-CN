---
navigation:
  parent: example-setups/index.md
  icon: minecraft:furnace
  title: 自动烧炼子网
categories:
  - example
---

# <a name="automated-smelting-subnet" /> 自动烧炼子网

可使用<ItemLink id="export_chest" />和<ItemLink id="import_chest" />桥接两个网络. 此例将主网络中的`#c:raw_material`物品送入具有一排熔炉的小型网络, 小型网络再将烧炼产物送回
原网络.

<GameScene zoom="4" interactive={true} paddingLeft="30" paddingRight="30">
  <ImportStructure src="../assets/assemblies/automated_smelting.snbt" />
  <IsometricCamera yaw="190" pitch="10" />
  <DiamondAnnotation pos="7.5 4 0.5" color="#ff0000">
    蓝色网络的输出箱在界面中设置为向下推送物品.

    **这两个箱子互不连接, 它们分别属于两个独立
    网络.**
  </DiamondAnnotation>
  <DiamondAnnotation pos="5.5 4 0.5" color="#ff0000">
    绿色网络的输出箱在界面中设置为向上推送物品.

    **这两个箱子互不连接, 它们分别属于两个独立
    网络.**
  </DiamondAnnotation>
  <BoxAnnotation min="5 0.75 0" max="8 1 1" color="#B02E26">
    <ItemImage id="storage_card" />红色频道存储卡中的物品由输出箱抽取, 输出箱用`*`过滤器匹配全部物品.
  </BoxAnnotation>
  <BoxAnnotation min="5 2 0" max="8 2.25 1" color="#3C44AA">
    <ItemImage id="storage_card" />蓝色频道存储卡接收输入箱以轮询方式推送的物品.
  </BoxAnnotation>
</GameScene>

