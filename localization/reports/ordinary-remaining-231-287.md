# 剩余普通文本收尾 (第 231-287 批)

56 个命名空间共 1148 个语言键, 其中 888 条中文, 260 条为审校后保留的非正文值.

| 批次 | 命名空间 | 键 | 中文 | 保留 |
|---|---|---:|---:|---:|
| 231 | reliquary | 156 | 151 | 5 |
| 232 | rgp_client | 132 | 132 | 0 |
| 233 | apothic_enchanting | 127 | 8 | 119 |
| 234 | neovitae | 86 | 72 | 14 |
| 235 | irons_lib | 72 | 71 | 1 |
| 236 | iska_lib | 66 | 66 | 0 |
| 237 | crystalix | 64 | 61 | 3 |
| 238 | wakes | 59 | 59 | 0 |
| 239 | aci | 57 | 8 | 49 |
| 240 | sky_aesthetics | 36 | 35 | 1 |
| 241 | limacore | 24 | 24 | 0 |
| 242 | modernfix | 22 | 22 | 0 |
| 243 | animusnv | 21 | 19 | 2 |
| 244 | libtooltips | 21 | 17 | 4 |
| 245 | modonomicon | 21 | 17 | 4 |
| 246 | armor_cosmetic | 13 | 13 | 0 |
| 247 | collective | 13 | 13 | 0 |
| 248 | contex | 11 | 11 | 0 |
| 249 | pylons | 11 | 11 | 0 |
| 250 | forgeendertech | 10 | 0 | 10 |
| 251 | mysticalagradditions | 9 | 9 | 0 |
| 252 | mss | 7 | 2 | 5 |
| 253 | lollipop | 8 | 0 | 8 |
| 254 | bblcore | 8 | 8 | 0 |
| 255 | creativecore | 6 | 3 | 3 |
| 256 | balm | 6 | 2 | 4 |
| 257 | framework | 6 | 6 | 0 |
| 258 | ftblibrary | 6 | 3 | 3 |
| 259 | bmaddon | 4 | 0 | 4 |
| 260 | cloth-config2 | 4 | 1 | 3 |
| 261 | crashutilities | 4 | 3 | 1 |
| 262 | eccentrictome | 4 | 4 | 0 |
| 263 | shogi | 4 | 4 | 0 |
| 264 | tesseract_api | 4 | 3 | 1 |
| 265 | titanium | 4 | 3 | 1 |
| 267 | yungsapi | 3 | 3 | 0 |
| 268 | aquarius_libs | 3 | 3 | 0 |
| 269 | baguettelib | 3 | 3 | 0 |
| 270 | evilcraft | 3 | 0 | 3 |
| 271 | evilcraftcompat | 3 | 3 | 0 |
| 272 | imfast | 3 | 3 | 0 |
| 273 | pipezlagfix | 3 | 3 | 0 |
| 274 | cucumber | 2 | 2 | 0 |
| 275 | adrenaline | 2 | 2 | 0 |
| 276 | mint_lib | 2 | 2 | 0 |
| 277 | patchouli | 2 | 0 | 2 |
| 278 | plonk | 2 | 0 | 2 |
| 279 | polylib | 2 | 0 | 2 |
| 280 | witchery_forbidden_magic | 2 | 2 | 0 |
| 281 | euphoria_patcher | 1 | 0 | 1 |
| 282 | placebo | 1 | 0 | 1 |
| 283 | cable_facades | 1 | 0 | 1 |
| 284 | cyclopscore | 1 | 0 | 1 |
| 285 | guideme | 1 | 0 | 1 |
| 286 | supermartijn642corelib | 1 | 1 | 0 |
| 287 | volumetrics | 1 | 0 | 1 |

## 处理原则

1. 术语优先取任务书与上游官方中文: NeoVitae 的 炼金炉/狱火锻炉/命血台桌/生命宝珠, Apothic Enchanting 的 位阶/量子化/阿卡那, 神秘农业的 熔融究极精华.
2. 标识符不译: ACI 的表达式函数名与关键字, ForgeEnderTech 的配置键名, EvilCraft 的罗马数字等级, 以及 true/false/hide 这类值关键字.
3. 纯格式串与模组名单独登记, 不产出伪中文: Lollipop, BM Addon, Plonk, PolyLib 以及 Euphoria Patches 等 6 个只有模组名的批次.
4. 以空格开头的拼接后缀 (Aquarius Libs 的三条状态文案) 保留前导空格, 否则与玩家名拼接时会粘连.

## 未纳入与本轮补做

- `sdrp` 的 3 个键来自 JAR 与 `kubejs/assets/sdrp/lang/en_us.json` 合并, 源文重复导致抽取脚本拒绝建批. 本轮直接在 `kubejs/assets/sdrp/lang/zh_cn.json` 覆盖: `Main Menu` → 主菜单, `In ` → `在 ` (保留尾随空格), 整合包名 `FTB Evolution 2` 保留.
- `ftb` 命名空间的 8 条为模组名 (Configured / DeepNull / Just Zoom / FTB Evolution 2) 与格式串 (`%s: %s`, `Y:%s`, `%s II`), 已在自定义阶段原样写入, 不再建批.

补做后, 普通文本暂无中文候选降至 9 条, 全部为上述模组名与格式串, 按设计保留英文.

游戏内验收未做.

## 结论

普通文本 (非手册) 的汉化在本轮结束: 9 条剩余均为不译项. 此后剩余工作量只有手册语言键 1,733 条与 19 条独立分组名, 属手册阶段.
