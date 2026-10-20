---
navigation:
  parent: index.md
  title: Powah
  position: 30
  icon: powah:reactor_hardened
---
<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">Powah</Color>

  <ItemImage id="powah:reactor_hardened" scale="2"/>

  Powah所有发电机的发电量均低于默认值,最高等级削弱最多.反应堆和热力发电机从硬化级起步.详见[已移除的发电机](removed.md).
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

> <Color id="yellow">所有数值单位均为FE/t,等级依次为:</Color>初级,基础,硬化,烈焰,钻石,富生,下界.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">发电机</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:furnator_starter"/>
  ### <Color id="aqua">熔炉发电机</Color>
</Row>

* <Color id="green">调整后:</Color> 16, 64, 128, 256, 512, 1,024, 4,096
* <Color id="gray">默认:</Color> 20, 80, 200, 800, 2,000, 8,000, 40,000

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:magmator_starter"/>
  ### <Color id="aqua">岩浆发电机</Color>
</Row>

* <Color id="green">调整后:</Color> 16, 64, 128, 256, 512, 1,024, 4,096
* <Color id="gray">默认:</Color> 20, 80, 200, 800, 2,000, 8,000, 40,000

输出传输速率从初级的80 FE/t提升至下界级的160,000 FE/t.每桶熔岩提供100,000 FE.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:reactor_hardened"/>
  ### <Color id="aqua">反应堆</Color>
</Row>

* <Color id="green">调整后:</Color> 128, 512, 2,560, 12,800, 64,000 (硬化级至下界级)
* <Color id="gray">默认:</Color> 2,500, 10,000, 25,000, 100,000, 500,000

能量缓存降为默认值的十分之一:从硬化级的250,000 FE提升至下界级的50,000,000 FE.

硬化级反应堆有独立配方:使用晶质铀,硬化电容和绝缘外壳,一次合成四个.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:thermo_generator_hardened"/>
  ### <Color id="aqua">热力发电机</Color>
</Row>

* <Color id="green">调整后:</Color> 64, 128, 256, 512, 2,048 (硬化级至下界级)
* <Color id="gray">默认:</Color> 100, 200, 400, 800, 2,000

热力发电机使用工业冷却液冷却,不能用水.部分热源也有调整.详见[冷却液,蒸汽与燃料](coolant_and_fuel.md).

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="powah:solar_panel_starter"/>
  ### <Color id="aqua">太阳能板</Color>
</Row>

* <Color id="green">调整后:</Color> 8, 16, 32, 64, 128, 256, 1,024
* <Color id="gray">默认:</Color> 20, 60, 100, 200, 400, 800, 2,000

太阳能板的能量缓存也大幅缩小:从初级的1,000 FE提升至下界级的20,000,000 FE.
