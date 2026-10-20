# 手册原文勘误

只修正中文覆盖文件; 英文源, 配置和游戏机制均未修改. 以下按零起始行号定位.

## ftb/power/index.md#30

英文: * **Lava is worth 10,000 FE per bucket** in the Oritech Lava Generator, the Energized Power Thermal Generator and the Powah Magmator.

中文: * 奥瑞科技熔岩发电机和Energized Power热力发电机的 **每桶熔岩提供10,000 FE** ;Powah岩浆发电机则为100,000 FE.

依据: Powah-7.0.4-alpha.jar: magmator_fuel.json energy_produced=10000; MagmatorBlockEntity.postTick uses a 100 mB batch, so a 1000 mB bucket yields 100000 FE. Rechecked local bytecode; no local fuel-map override found.

## ftb/power/coolant_and_fuel.md#91

英文: A bucket of lava is worth **10,000 FE** in every generator that burns it as fuel:

中文: 将熔岩用作燃料时,各发电机每桶的发电量如下(奥瑞科技与Energized Power为 **10,000 FE** ,Powah例外):

依据: Powah-7.0.4-alpha.jar: magmator_fuel.json energy_produced=10000; MagmatorBlockEntity.postTick uses a 100 mB batch, so a 1000 mB bucket yields 100000 FE. Rechecked local bytecode; no local fuel-map override found.

## ftb/power/coolant_and_fuel.md#95

英文: * Powah Magmator: 10,000 (already the default)

中文: * Powah岩浆发电机:100,000(当前模组每100 mB产生10,000 FE)

依据: Powah-7.0.4-alpha.jar: magmator_fuel.json energy_produced=10000; MagmatorBlockEntity.postTick uses a 100 mB batch, so a 1000 mB bucket yields 100000 FE. Rechecked local bytecode; no local fuel-map override found.

## ftb/power/powah.md#47

英文: Output transfer runs from 80 FE/t for Starter up to 160,000 FE/t for Nitro. Lava gives 10,000 FE per bucket.

中文: 输出传输速率从初级的80 FE/t提升至下界级的160,000 FE/t.每桶熔岩提供100,000 FE.

依据: Powah-7.0.4-alpha.jar: magmator_fuel.json energy_produced=10000; MagmatorBlockEntity.postTick uses a 100 mB batch, so a 1000 mB bucket yields 100000 FE. Rechecked local bytecode; no local fuel-map override found.

## ftb/power/energized_power.md#37

英文: Lava is worth 10,000 FE per bucket (50,000), the same as every other lava generator in the pack.

中文: 每桶熔岩可产生10,000 FE(50,000),与奥瑞科技熔岩发电机一致;Powah岩浆发电机不在此列.

依据: Powah-7.0.4-alpha.jar: magmator_fuel.json energy_produced=10000; MagmatorBlockEntity.postTick uses a 100 mB batch, so a 1000 mB bucket yields 100000 FE. Rechecked local bytecode; no local fuel-map override found.

## ftbic/generators/geothermal_generator.md#15

英文:   Consumes **lava** from an internal 8,000 mB tank to produce **640 FE/t**. Twice the output of a Basic Generator, and entirely renewable if you have a nether portal tap or a lava lake nearby.

中文:   消耗内部8,000 mB储罐中的 **熔岩** ,产生 **320 FE/t** ,与本整合包的基础发电机相同.只要能从下界或附近熔岩湖持续抽取熔岩,就能稳定供电.

依据: ftbic-common.toml machines.geothermal_generator_output=40.0; energy.zap_to_fe_conversion_rate=8.0, full_fe_mode=true: output=320 FE/t, equal to basic generator. GeothermalGeneratorBlockEntity reads maxEnergyOutput.

## ftbic/generators/geothermal_generator.md#43

英文: * **Output:** 640 FE/t

中文: * **输出:** 320 FE/t

依据: ftbic-common.toml machines.geothermal_generator_output=40.0; energy.zap_to_fe_conversion_rate=8.0, full_fe_mode=true: output=320 FE/t, equal to basic generator. GeothermalGeneratorBlockEntity reads maxEnergyOutput.

## ftbic/generators/index.md#25

英文: | <ItemLink id="geothermal_generator" /> | LV | 640 FE/t | Needs lava in tank |

中文: | <ItemLink id="geothermal_generator" /> | LV | 320 FE/t | 需要储罐内有熔岩 |

依据: ftbic-common.toml machines.geothermal_generator_output=40.0; energy.zap_to_fe_conversion_rate=8.0, full_fe_mode=true: output=320 FE/t, equal to basic generator. GeothermalGeneratorBlockEntity reads maxEnergyOutput.

## ftbic/generators/wind_mill.md#15

英文:   A height-dependent generator that makes about **60 FE/t** at Y=64 and about **260 FE/t** at Y=320.

中文:   发电量取决于高度.在天气和遮挡修正前,配置输出从Y=64时的 **9.6 FE/t** 提升至Y=320时的 **104 FE/t** .

依据: ftbic-common.toml wind_mill_min_output=1.2, wind_mill_max_output=13, min_y=64, max_y=320; Zap-to-FE factor=8, so configured endpoint outputs=9.6 and 104 FE/t before weather/obstructions.

## ftbic/generators/index.md#26

英文: | <ItemLink id="wind_mill" /> | LV | About 60 to 260 FE/t | Height-dependent |

中文: | <ItemLink id="wind_mill" /> | LV | 约9.6至104 FE/t | 取决于高度 |

依据: ftbic-common.toml wind_mill_min_output=1.2, wind_mill_max_output=13, min_y=64, max_y=320; Zap-to-FE factor=8, so configured endpoint outputs=9.6 and 104 FE/t before weather/obstructions.

## ftbic/upgrades/index.md#12

英文:   Machines that support upgrades have 4 upgrade slots and accept **4 upgrades total**, combined across all slots and types. One slot may hold a stack of 4. Parallel Processing Upgrades have a separate limit of 3 per machine. Shift-click a stack into the machine UI, or sneak-right-click the machine while holding upgrades to install as many as it can accept, up to 4 at once. Extra upgrades stay in your hand or inventory.

中文:   支持升级的机器有4个升级槽, **每种升级合计最多4个** ,可集中堆叠在一个槽中.并行处理升级另有每台机器3个的限制.在机器界面中Shift点击一组升级,或手持升级潜行右击机器,可在容量允许时一次安装最多4个.多余升级保留在手中或物品栏.

依据: FTBIC UpgradeInventory.getSlotLimit(int,ItemStack) counts other slots containing the SAME item, and limits to 4 minus that count; parallel processing is separately capped at 3. It does not cap all types combined at 4.

## ftbic/upgrades/overclocker.md#26

英文: * Install up to 4 upgrades total across the machine's upgrade slots. All 4 can share one slot.

中文: * 全部升级槽合计最多安装4个超频升级,4个可以集中在同一槽;其他升级类型分别计算上限.

依据: FTBIC UpgradeInventory.getSlotLimit(int,ItemStack) counts other slots containing the SAME item, and limits to 4 minus that count; parallel processing is separately capped at 3. It does not cap all types combined at 4.

## ftbic/upgrades/energy_storage.md#25

英文: Stack up to **16** total (4 per slot × 4 slots) for an extra 5,120,000 FE of local buffer.

中文: 最多安装 **4** 个储能升级(可在一个槽中堆叠4个),额外提供1,280,000 FE本地缓存;不能将同类升级在4个槽中各放满.

依据: FTBIC UpgradeInventory.getSlotLimit(int,ItemStack) counts other slots containing the SAME item, and limits to 4 minus that count; parallel processing is separately capped at 3. It does not cap all types combined at 4. Each upgrade adds 320000 FE, so maximum extra capacity is 4*320000=1280000 FE.

