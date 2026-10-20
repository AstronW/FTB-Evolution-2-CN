---
navigation:
  parent: index.md
  title: Energized Power
  position: 60
  icon: energizedpower:solar_panel_5
---
<Column alignItems="center" fullWidth={true}>
  # <Color id="light_purple">Energized Power</Color>

  <ItemImage id="energizedpower:solar_panel_5" scale="2"/>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">发电机</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="energizedpower:basic_machine_frame"/>
  ### <Color id="aqua">移除燃煤引擎</Color>
</Row>

燃煤引擎已移除.原本需要燃煤引擎的热能发电机,热力发电机和便携燃煤引擎,现改用 **基础机器框架** .原本售卖燃煤引擎的电工村民改卖热能发电机.

<ItemImage id="minecraft:air" scale="0.25"/>

<Row>
  <ItemImage id="energizedpower:thermal_generator"/>
  ### <Color id="aqua">热力发电机</Color>
</Row>

每桶熔岩可产生10,000 FE(50,000),与奥瑞科技熔岩发电机一致;Powah岩浆发电机不在此列.

<ItemImage id="minecraft:air" scale="0.25"/>

***

<Column alignItems="center" fullWidth={true}>
  ## <Color id="gold">太阳能板</Color>
</Column>

<ItemImage id="minecraft:air" scale="0.25"/>

高等级太阳能板的发电量远低于默认值.I级和II级没有改动.

| 太阳能板 | 峰值输出 |
|---|:---:|
| <ItemImage id="energizedpower:solar_panel_3"/> 等级 III | 64 FE/t (128) |
| <ItemImage id="energizedpower:solar_panel_4"/> 等级 IV | 256 FE/t (2,048) |
| <ItemImage id="energizedpower:solar_panel_5"/> 等级 V | 512 FE/t (16,384) |
| <ItemImage id="energizedpower:solar_panel_6"/> 等级 VI | 4,096 FE/t (131,072) |
| <ItemImage id="energizedpower:solar_panel_7"/> 等级 VII | 16,000 FE/t (524,288) |

> <Color id="yellow">III级和IV级太阳能板应直接连接储能设备.</Color>III级仅能传输64 FE/t(512),IV级仅能储存256 FE(81,920).
