---
navigation:
  title: 入门指南
  position: 10
---

# <a name="getting-started" /> 入门指南

## <a name="required-materials" /> 所需材料

Nodeworks网络利用<ItemLink id="celestine_shard" />的反射特性工作.

## <a name="growing-celestine" /> 培育天青石

天青石的生长方式类似<ItemLink id="minecraft:amethyst_cluster" />:
从母岩<ItemLink id="budding_celestine" />上长出晶芽.

## <a name="first-nodeworks-network" /> 第一个Nodeworks网络

先搭建一个无需编写脚本的简单网络, 使用物品终端查看
任意数量的相连箱子中的物品.

<GameScene interactive={true} zoom="5">
  <IsometricCamera yaw="200" pitch="10" />
  <ImportStructure src="assets/assemblies/first_network.snbt" />
</GameScene>

- 此网络包含以下组件:
  - 1个<ItemLink id="network_controller" />
  - 1个<ItemLink id="inventory_terminal" />
  - 若干<ItemLink id="pipe" />, 用于连接所有设备
  - 若干<ItemLink id="node" />, 用于将箱子等外部方块接入网络
  - 1张<ItemLink id="storage_card" />, 安装在节点朝向箱子的那一面

### <a name="expanding-your-nodeworks-network" /> 扩展Nodeworks网络

- [移动物品](./example-setups/moving-items.md)
- [自动合成](./nodeworks-mechanics/autocrafting.md)
- [搭建示例](./example-setups/index.md)
