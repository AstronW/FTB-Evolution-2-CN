---
navigation:
  parent: ae2wtlib/ae2wtlib-index.md
  title: "AE2WTLib无线终端"
  icon: ae2wtlib:wireless_universal_terminal
  position: 10
categories:
- ae2wtlib
item_ids:
  - ae2wtlib:wireless_pattern_encoding_terminal
  - ae2wtlib:wireless_pattern_access_terminal
---

<a name="wireless-terminals"></a>

# 无线终端

<ItemGrid>
  <ItemIcon id="ae2wtlib:wireless_universal_terminal" />
  <ItemIcon id="ae2:wireless_crafting_terminal" />
  <ItemIcon id="ae2wtlib:wireless_pattern_encoding_terminal" />
  <ItemIcon id="ae2wtlib:wireless_pattern_access_terminal" />
</ItemGrid>

除去<ItemLink id="ae2:energy_card" />外, 所有AE2WTLib无线终端也接受<ItemLink id="ae2wtlib:quantum_bridge_card" />, 还可组合为<ItemLink id="ae2wtlib:wireless_universal_terminal" />.

与AE2的<ItemLink id="ae2:wireless_terminal" />类似, 本模组的终端可通过键位打开, 也可放入饰品槽(如果有模组实现了Curios API的话).

无线终端也可像普通的<ItemLink id="ae2:wireless_terminal" />那样与<ItemLink id="ae2:wireless_access_point" />建立连接.

<a name="wireless-universal-terminal"></a>

## 无线通用终端

<ItemImage id="ae2wtlib:wireless_universal_terminal" scale="3" />

<ItemLink id="ae2wtlib:wireless_universal_terminal" />是多个无线终端组合而成的物品.

<a name="wireless-crafting-terminal"></a>

## 无线合成终端

<ItemImage id="ae2:wireless_crafting_terminal" scale="3" />

<ItemLink id="ae2:wireless_crafting_terminal" />是合成终端的无线版本.它相较于AE2原版来说有一些[额外功能](wireless_crafting_terminal.md).

<a name="wireless-pattern-encoding-terminal"></a>

## 无线样板编码终端

<ItemImage id="ae2wtlib:wireless_pattern_encoding_terminal" scale="3" />

<ItemLink id="ae2:pattern_encoding_terminal" />的无线版本.

<RecipeFor id="ae2wtlib:wireless_pattern_encoding_terminal" />

<a name="wireless-pattern-access-terminal"></a>

## 无线样板管理终端

<ItemImage id="ae2wtlib:wireless_pattern_access_terminal" scale="3" />

<ItemLink id="ae2:pattern_access_terminal" />的无线版本.

<RecipeFor id="ae2wtlib:wireless_pattern_access_terminal" />

<a name="addon-terminals"></a>

## 附属终端

来自其他附属的大多数无线终端均可装入<ItemLink id="ae2wtlib:wireless_universal_terminal" />.

<a name="terminals-that-dont-work-in-the-universal-terminal"></a>

## 不适用于通用终端的终端

<ItemLink id="ae2:wireless_terminal" />不可装入<ItemLink id="ae2wtlib:wireless_universal_terminal" />, 这是因为它的功能已被<ItemLink id="ae2:wireless_crafting_terminal" />完全覆盖.它也无法装入<ItemLink id="ae2wtlib:quantum_bridge_card" />.
