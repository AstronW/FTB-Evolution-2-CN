---
navigation:
  title: 海洋之眼
  icon: nautec:eye_of_the_sea
  position: 15
  parent: getting_started/getting_started-index.md
item_ids:
  - nautec:eye_of_the_sea
---

# <Color id="light_purple">海洋之眼</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="eye_of_the_sea" scale="2"/>
  一种可以反复使用的海洋版末影之眼. 投出后它会飞向它正在寻找的最近结构.
</Column>

***

## <Color id="gold">投掷</Color>

右键点击投出海洋之眼. 它会在搜索时嗡鸣片刻(快捷栏上方会有消息提示, 搜索结束前无法再次投掷), 然后升起并像末影之眼一样飞向最近的匹配结构, 约四秒后爆成一团气泡. 它永远不会掉落, 也不会被消耗, 因此你可以随意投掷, 两次投掷之间需等待两秒.

如果约 1,600 格内没有匹配的结构, 海洋之眼会留在你手中, 并显示一条消息.

水晶晶洞埋在海床之下, 因此当海洋之眼开始盘旋或下降时, 晶洞的中心就在你脚下. 从那里垂直向下挖.

***

## <Color id="gold">更换目标</Color>

潜行右键点击可切换海洋之眼寻找的目标. 提示框和快捷栏上方的消息会显示当前目标. 顺序如下:

| 目标 | 寻找 |
|---|---|
| 水晶晶洞 | 含有<ItemLink id="prismarine_crystal"/>的石头和深板岩晶洞 |
| 海蓝科技 废墟 | 带有<ItemLink id="aquatic_catalyst"/>的暗海晶石拱门 |
| 研究前哨站 | 沉没的研究站, 参见[结构](structures.md) |
| 传送门 | 水下传送门平台, 参见[传送门](nautec:deep_engineering/gateway.md) |
| 海底废墟 | 原版的冷水和暖水海底废墟 |
| 海底神殿 | 原版海底神殿 |

新的海洋之眼默认从水晶晶洞开始, 每只海洋之眼都会记住自己的目标. 你自己建造的传送门不是它的目标. 每种结构中有哪些物品, 参见[结构](structures.md).

***

## <Color id="gold">水上的好运</Color>

每次成功找到目标的投掷还会搅动你周围的水域. 在接下来的 5 分钟内, 你附近形成[幸运钓鱼区](fishing.md)的频率会加倍. 再次投掷会重新开始计算这 5 分钟.

***

## <Color id="gold">合成</Color>

一个末影珍珠和一个海晶碎片, 以任意摆放方式合成.

<Recipe id="nautec:eye_of_the_sea"/>

搜索范围, 两次投掷之间的等待时间, 以及钓鱼加成的持续时间和强度都可在 `config/nautec-common.toml` 中调整.
