---
navigation:
  title: 挤压机
  icon: ftbic:extruder
  parent: machines/index.md
  position: 5
item_ids:
  - ftbic:extruder
---

# <Color id="gold">挤压机</Color>

<Column alignItems="center" fullWidth={true}>
  <ItemImage id="extruder" scale="2" />

  将金属加工成 **锭** , **板** 和 **棒** ,为大量合成提供这些基础材料.
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<RecipeFor id="extruder" />

<ItemImage id="minecraft:air" scale="0.25"/>
***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">配方类型</Color>
</Column>

挤压机有三类配方产物,具体由配方决定:

* **锭** :2粉→1锭
* **板** :1锭→1板
* **棒** :1锭→2棒

除非配置禁用,FTB Materials注册的每种金属都有这三类配方.合成所需的板和棒(用于齿轮,线和机器部件)几乎都来自这里.

<ItemImage id="minecraft:air" scale="0.25"/>

**参数:** LV级,缓存38,400 FE,耗能24 FE/t.
