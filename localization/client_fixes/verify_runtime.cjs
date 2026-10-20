const fs = require('node:fs'), vm = require('node:vm'), assert = require('node:assert/strict')
const root = __dirname
const names = JSON.parse(fs.readFileSync(root + '/mod-names.json'))
assert.equal(names.mysticalagriculture?.translation, '神秘农业', 'Existing Chinese mod name must be connected')
assert.equal(names.ae2?.translation, '应用能源2', 'Existing Chinese mod name must be connected')
const userNames = JSON.parse(fs.readFileSync(root + '/user-name-decisions.json')).names
for (const [id, zh] of Object.entries(userNames)) {
    if (id !== 'authme') assert.equal(names[id]?.translation, zh)
}
assert.equal(names.authme, undefined, 'Auth Me keeps its original English metadata')
const renamed = {}
vm.runInNewContext(fs.readFileSync(root + '/mod_names.js','utf8'), {Platform: {isLoaded: id => !!names[id], getInfo: id => ({setName: zh => renamed[id] = zh})}})
for (const [id, row] of Object.entries(names)) assert.equal(renamed[id], row.translation)
function list(a) {return {size: () => a.length, get: i => a[i], set: (i,v) => a[i] = v}}
function text(value, style = 'green', children = []) {return {
    getString() {return value + children.map(c => c.getString()).join('')},
    getContents: () => ({text: () => value}), getStyle: () => style,
    getSiblings: () => list(children),
    setStyle(s) {style = s; return this}, append(c) {children.push(c); return this},
    copy: () => text(value, style, children.map(c => c.copy()))
}}
let handler, active = true, dynamic
vm.runInNewContext(fs.readFileSync(root + '/nutrients.js','utf8'), {
    Text: {of: s => text(s), translate: () => text(active ? '营养: ' : 'Nutrients: ')},
    ItemEvents: {
        modifyTooltips: cb => cb({modifyAll: cb => cb({dynamic: id => dynamic = id})}),
        dynamicTooltips: (id, cb) => {assert.equal(id, dynamic); handler = cb}
    }
})
const child = text('水果, 谷物', 'green'), amount = text(' (1.00)', 'aqua')
const unchanged = text('Unrelated line', 'gray')
const rows = [unchanged, text('Nutrients: ', 'dark_green', [child, amount])]
handler({lines: list(rows)})
assert.equal(rows[0], unchanged)
assert.equal(rows[1].getString(), '营养: 水果, 谷物 (1.00)')
assert.equal(rows[1].getStyle(), 'dark_green')
assert.equal(rows[1].getSiblings().get(1).getStyle(), 'aqua')
active = false
const english = text('Nutrients: ', 'green', [child]); const other = [english]
handler({lines: list(other)}); assert.equal(other[0], english)
console.log('PASS: mod-name mapping; nutrition label, language gate, sibling colors and amount preserved (mock API; no game launch)')
