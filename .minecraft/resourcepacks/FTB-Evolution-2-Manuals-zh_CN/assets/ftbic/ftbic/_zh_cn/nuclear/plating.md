---
navigation:
  title: 反应堆隔板
  icon: ftbic:reactor_plating
  parent: nuclear/index.md
  position: 4
item_ids:
  - ftbic:reactor_plating
  - ftbic:heat_capacity_reactor_plating
  - ftbic:containment_reactor_plating
---

# <Color id="gold">反应堆隔板</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="reactor_plating" scale="2" />

  隔板改变 **反应堆外壳** 本身的总热容量,以及发生最坏情况时的爆炸半径.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Row>
  <ItemImage id="reactor_plating" />
  ### <Color id="aqua">反应堆隔板</Color>
</Row>

降低反应堆熔毁时的爆炸破坏.

<RecipeFor id="reactor_plating" />

<Row>
  <ItemImage id="heat_capacity_reactor_plating" />
  ### <Color id="aqua">高热容反应堆隔板</Color>
</Row>

增加反应堆总热容量,使其更慢达到临界,更适合脉冲式设计.

<RecipeFor id="heat_capacity_reactor_plating" />

<Row>
  <ItemImage id="containment_reactor_plating" />
  ### <Color id="aqua">密封反应堆隔板</Color>
</Row>

防护失效时大幅削弱爆炸强度,为激进设计提供保障.

<RecipeFor id="containment_reactor_plating" />
