---
navigation:
  parent: example-setups/index.md
  icon: milky_soul_ball
  title: 奶香灵魂球农场
categories:
  - example
---

# <a name="milky-soul-ball-farm" /> 奶香灵魂球农场

<GameScene zoom="4" interactive={true} paddingLeft="30" paddingRight="30">
  <ImportStructure src="../assets/assemblies/milky_soul_farm.snbt" />
  <Entity id="minecraft:cow" x="2.5" z="1.5" rotationY="170"/>
  <IsometricCamera yaw="200" pitch="20" />
  <BlockAnnotation x="5" y="1" z="1">
    <ItemGrid>
        <ItemIcon id="minecraft:bucket" />
        <ItemIcon id="minecraft:soul_sand" />
    </ItemGrid>
  </BlockAnnotation>
  <BlockAnnotation x="3" y="1" z="1">
    使用器用空桶对牛进行操作.

    ![放置器界面, 已将空桶设为筛选条件](../assets/images/user_empty_bucket.png)
  </BlockAnnotation>
  <BlockAnnotation x="3" y="4" z="1">
    使用器将奶桶用于灵魂沙, 再将得到的奶香灵魂球
    和空桶放回网络存储.

    ![使用器界面, 已将奶桶设为筛选条件](../assets/images/user_milk_bucket.png)
  </BlockAnnotation>
  <BlockAnnotation x="1" y="4" z="1">
    放置器在使用器前方放置灵魂沙.

    ![放置器界面, 已将灵魂沙设为筛选条件](../assets/images/placer_soul_sand.png)
  </BlockAnnotation>
</GameScene>

此农场先让<ItemLink id="user" />用空桶给牛挤奶, 将奶桶存入[网络存储](../nodeworks-mechanics/network-storage.md). 另一个使用器再将这些<ItemLink id="minecraft:milk_bucket" />用于<ItemLink id="minecraft:soul_sand" />, 灵魂沙由<ItemLink id="placer" />放置.

> **注意:** 放置器和使用器的红石模式均设为低电平, 使其持续启用.
