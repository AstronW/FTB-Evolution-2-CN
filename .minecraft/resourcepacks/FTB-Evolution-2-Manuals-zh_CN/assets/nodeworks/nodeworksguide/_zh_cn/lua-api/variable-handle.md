---
navigation:
  parent: lua-api/index.md
  title: VariableHandle
  icon: variable
categories:
  - api_types
description: reference to a <ItemLink id="variable" /> in a network
---

# <a name="VariableHandle" /> <a name="variablehandle" /> VariableHandle

`VariableHandle`引用网络中的<ItemLink id="variable" />,
由[`network:get(name)`](network.md#get)返回, 与获取卡片
的方法相同. 句柄跟踪变量声明的类型. 各类型
除下列共用核心API外, 还具有专用辅助方法.

<BlockImage scale="6" id="variable" />

> **注意:** 所有修改均为原子操作. 另一个脚本对同一变量调用`:set`或`:cas`
> 时, 绝不会在操作中途交错执行.

## <a name="Properties" /> <a name="properties" /> 属性

- **`.name`**
  - 变量别名, 与终端侧栏显示的名称相同

## <a name="core-methods" /> 核心方法

### <a name="get-/-set" /> <a name="get-set" /> get / set

获取和设置变量当前值.

<LuaCode>
```lua
local myNumericVar = network:get("myNumericVar")
print(myNumericVar:get())
myNumericVar:set(1)
print(myNumericVar:get())
-- "0"
-- "1"
```
</LuaCode>

### <a name="cas" /> cas

比较并交换. 只有当前值等于预期值时, 才设置为`new`,
预期值由`expected`指定. 否则保持原值, 成功时返回`true`,
已被其他操作更改时返回`false`.

准备写入的新值 **依赖当前值** , 且多个脚本可能
访问同一变量时, 请使用此方法. `:set`会直接覆盖
原值, 两个脚本竞争时可能相互覆盖操作结果.
`:cas`则只在变量仍为你所预期的值时写入.

<LuaCode>
```lua
-- 认领任务槽: 只有第一个读到""的脚本成功
if slot:cas("", "worker_A") then
  print("i got the job")
else
  print("someone else already claimed it")
end
```
</LuaCode>

数值可能在操作中途变化时, 常用的读取-修改-写入循环如下:

<LuaCode>
```lua
-- 仅在>0时递减, 发生竞争则重试
while true do
  local current = counter:get()
  if current <= 0 then
    break -- 已无剩余可取
  end
  if counter:cas(current, current - 1) then
    break -- 已成功取得
  end
  -- 另一个脚本在: get和: cas之间改变了值, 再试一次
end
```
</LuaCode>

> **注意:** 简单算术可用[`increment / decrement`](variable-handle.md#increment--decrement), 它们本身已是
> 原子操作, 且更简单. 状态变化不只是"+/- n"时再用`:cas`.

### <a name="type" /> type

返回表示此`VariableHandle`类型的字符串.

- **`NumberVariableHandle`**
  - `"number"`
- **`BoolVariableHandle`**
  - `"bool"`
- **`StringVariableHandle`**
  - `"string"`

<LuaCode>
```lua
local numberVar = network:get("numberVar")
local boolVar = network:get("boolVar")
local stringVar = network:get("stringVar")
print(numberVar:type())
print(boolVar:type())
print(stringVar:type())
-- "number"
-- "bool"
-- "string"
```
</LuaCode>

## <a name="BoolVariableHandle" /> <a name="boolvariablehandle" /> BoolVariableHandle

此[`VariableHandle`](./variable-handle.md)引用一个<ItemLink id="variable" />, 其声明类型如下:
`bool`. 增加仅适用于布尔变量的方法.

### <a name="toggle" /> toggle

翻转当前值, `true`变为`false`, `false`变为`true`,
并返回新值.

<LuaCode>
```lua
local lights = network:get("lights")
print(lights:get())
lights:toggle()
print(lights:get())
-- "false"
-- "true"
```
</LuaCode>

> **注意:** 可通过红石按钮触发此方法, 实现"按下即切换", 例如使用
> [`RedstoneCard:onChange`](./card-handle.md#onchange)

### <a name="trylock-/-unlock" /> <a name="trylock-unlock" /> tryLock / unlock

布尔变量也可充当互斥锁. `:tryLock()`以原子方式将
变量从`false`改为`true`, 成功时返回`true`. 若变量
已为`true`, 即其他脚本持有锁, 则 **不阻塞** 地返回`false`.
`:unlock()`将它改回`false`.

<LuaCode>
```lua
local mutex = network:get("job_mutex") -- 布尔变量
if mutex:tryLock() then
  -- 执行任务
  mutex:unlock()
end
```
</LuaCode>

> **重要:** 锁已被持有时, `:tryLock`不会等待, 而是立即返回`false`. 脚本应稍后重试, 例如使用[`scheduler:delay`](scheduler.md#delay), 或在无法取得锁时跳过操作.
>
> 成功的`:tryLock`必须配对`:unlock`. 如上例用`pcall`包裹临界区, 防止代码出错后锁无法释放.

## <a name="NumberVariableHandle" /> <a name="numbervariablehandle" /> NumberVariableHandle

此[`VariableHandle`](./variable-handle.md)引用一个<ItemLink id="variable" />, 其声明类型如下:
`number`. 增加仅适用于数字变量的方法.

### <a name="increment--decrement" /> <a name="increment-/-decrement" /> <a name="increment-decrement" /> increment / decrement

对变量当前值进行加法或减法. 两者均接受一个数量, 并返回
新值.

<LuaCode>
```lua
local counter = network:get("counter")
counter:set(0)
counter:increment(1) -- +1 -> 1
counter:increment(5) -- +5 -> 6
counter:decrement(2) -- -2 -> 4
```
</LuaCode>

### <a name="min-/-max" /> <a name="min-max" /> min / max

- `:min(n)`将变量设为当前值与`n`中较小的一个.
- `:max(n)`则设为较大的一个.

二者均返回新值.

<LuaCode>
```lua
local best = network:get("best_score")
best:set(42)
best:max(50) -- 42与50比较->50, 新最高值
best:max(35) -- 50与35比较->50, 保持不变
best:min(10) -- 50与10比较->10, 限制上界
```
</LuaCode>

## <a name="StringVariableHandle" /> <a name="stringvariablehandle" /> StringVariableHandle

此[`VariableHandle`](./variable-handle.md)引用一个<ItemLink id="variable" />, 其声明类型如下:
`string`. 增加仅适用于字符串变量的方法.

### <a name="append-/-length-/-clear" /> <a name="append-length-clear" /> append / length / clear

- `:append(str)`将`str`追加到当前值末尾, 返回新
字符串.
- `:length()`返回当前值字符数.
- `:clear()`清空变量, 即设为`""`.

<LuaCode>
```lua
local log = network:get("log")
log:clear()
log:append("start ")
log:append("middle ")
log:append("end")
print(log:get())
print(log:length())
-- "start middle end"
-- 16
```
</LuaCode>
