---
navigation:
  parent: nodeworks-mechanics/index.md
  title: 网络存储
  icon: minecraft:chest
categories:
  - mechanic
---

# <a name="network-storage" /> 网络存储

网络存储是Nodeworks网络将物品与流体视为自身资源的
共享池. 安装<ItemLink id="storage_card" />的方块
都会加入该池. 脚本可以读写其中内容,
<ItemLink id="inventory_terminal" />可显示和操作它,
合成系统也从中拉取原料.

<GameScene zoom="5" interactive={true} paddingLeft="50" paddingRight="60">
  <ImportStructure src="../assets/assemblies/network_storage.snbt" />
  <BoxAnnotation min="2.25 1.1 0.1" max="2 1.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />将此箱子纳入网络存储.
  </BoxAnnotation>
  <BoxAnnotation min="2.25 0.1 0.1" max="2 0.9 0.9" color="#AA83E0">
    <ItemImage id="nodeworks:storage_card" />将此箱子纳入网络存储.
  </BoxAnnotation>
  <BlockAnnotation x="3" y="1" z="0">
    可使用<ItemLink id="inventory_terminal" />查看网络存储的内容.
  </BlockAnnotation>
</GameScene>

## <a name="what&#x27;s-in-the-network-storage-pool" /> <a name="whats-in-the-network-storage-pool" /> 哪些内容属于网络存储

所有通过<ItemLink id="storage_card" />接入的方块中的全部内容. 断开
存储卡所在节点的连接时, 该方块会立即退出存储池.

### <a name="not-in-the-pool" /> 不属于存储池的内容

<ItemLink id="io_card" />对应的方块不属于网络存储.
脚本必须显式地向IO卡对应方块输入或取出物品.
`network:find`不会看到其中内容, <ItemLink id="inventory_terminal" />和<ItemLink id="portable_inventory_terminal" />也不会列出它们.

## <a name="priority-and-routing" /> 优先级与路由

各<ItemLink id="storage_card" />的 **优先级** 决定
`network:insert`/`:tryInsert`填充存储的顺序. 写入先进入
优先级最高且匹配的卡片, 填满后再流向较低优先级卡片.
优先级相同的两张卡按连接顺序填充.

脚本可通过注册路由, 为特定物品覆盖默认优先级,
具体见[`network:route`](../lua-api/network.md#route).

可直接在卡片界面设置优先级. 界面说明见
[存储卡](../items-blocks/storage_card.md#configuring-priority),
也可使用<ItemLink id="card_programmer" />将优先级及其他
卡片设置批量复制到多张卡片.

## <a name="scripting-with-network-storage" /> 通过脚本操作网络存储

脚本读写此共享池的全部函数, 见[网络API](../lua-api/network.md)
页面.

## <a name="viewing-and-managing-through-the-inventory-terminal" /> 通过物品终端查看与管理

<Row align="center">
  <BlockImage scale="3.3" id="inventory_terminal" />
  <ItemImage scale="4" id="portable_inventory_terminal" />
</Row>

<ItemLink id="inventory_terminal" />和<ItemLink id="portable_inventory_terminal" />是无需编写脚本即可
查看和操作网络存储的主要方式.
它以可搜索网格显示整个存储池, 可将物品取入
玩家物品栏, 存回网络, 或请求合成. 显示的全部
内容都实时来自本网络相连的存储卡.

界面详情见[物品终端](../items-blocks/inventory_terminal.md)
页面.
