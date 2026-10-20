// Verify the changed message paths without starting Minecraft.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const path = require('path');
const root = path.resolve(__dirname, '../..');
const language = {};
for (const ns of ['ftb', 'ftb_custom']) Object.assign(language, JSON.parse(fs.readFileSync(path.join(root, `.minecraft/kubejs/assets/${ns}/lang/zh_cn.json`))));
class Message {
  constructor(value) { this.value = value; }
  append(value) { this.value += value instanceof Message ? value.value : String(value); return this; }
  green() { return this; }
  red() { return this; }
}
const Text = {
  of: value => new Message(String(value)),
  translate: (key, args = []) => {
    assert.ok(key in language, `Missing language key: ${key}`);
    let i = 0;
    return new Message(language[key].replace(/%s/g, () => {
      const value = args[i++]; return value instanceof Message ? value.value : String(value);
    }));
  }
};
class Branch {
  constructor(name) { this.name = name; this.children = []; }
  then(child) { this.children.push(child); return this; }
  requires() { return this; }
  executes(handler) { this.handler = handler; return this; }
}
let registryCallback;
const output = [];
const statNames = [];
const player = { persistentData: { disabledEvents: [] }, username: 'Tester' };
const eventObj = { name: 'ftb:goat', displayName: 'Goat', size: -1, execute() {} };
const source = { getPlayerOrException: () => player, sendSuccess: m => output.push(m.value), getServer: () => ({}) };
const commandContext = { getSource: () => source };
const scope = {
  Text, console, Java: { loadClass: () => ({}) },
  ServerEvents: { commandRegistry: callback => { registryCallback = callback; } },
  defaultEventSettings: {}, ftbEvents: [eventObj], ftbEventsInactive: [],
  Statistics: () => ({ data: () => ({ failure: { Goat: 1 }, success: { Creeper: 2 } }), totalEvents: () => 3, addSuccess: name => statNames.push(name) }),
  checks: { player: { getDisabledEvents: () => player.persistentData.disabledEvents } }
};
vm.createContext(scope);
vm.runInContext(fs.readFileSync(path.join(root, '.minecraft/kubejs/server_scripts/systems/ftb_events/commands.js'), 'utf8'), scope);
const registered = [];
const argument = { create: () => ({}), getResult: () => null };
registryCallback({ commands: { literal: name => new Branch(name), argument: name => new Branch(name) }, arguments: { INTEGER: argument, BOOLEAN: argument, PLAYER: argument }, register: branch => registered.push(branch) });
const statistics = registered[0].children.find(branch => branch.name === 'statistics');
statistics.handler(commandContext);
assert.match(output.pop(), /事件触发总数: 3\n=+\n山羊 事件失败总数: 1\n=+\n苦力怕 事件成功总数: 2/);
scope.commandContext = commandContext; scope.eventObj = eventObj;
vm.runInContext('toggleEventForPlayer(eventObj, commandContext)', scope);
assert.equal(player.persistentData.disabledEvents[0], 'ftb:goat');
assert.equal(output.pop(), '已关闭 山羊 事件');
vm.runInContext('toggleEventForPlayer(eventObj, commandContext)', scope);
assert.equal(player.persistentData.disabledEvents.length, 0);
assert.equal(output.pop(), '已开启 山羊 事件');
vm.runInContext('forceEvent(commandContext, null, eventObj)', scope);
assert.deepEqual(statNames, ['Goat']);
assert.equal(output.pop(), '已强制触发 山羊 事件, 目标为 Tester');
scope.SpawnPyramid = {
  data: () => ({ getStringOr: () => 'pending', getIntOr: () => 2, getBooleanOr: () => true }),
  storedOrigin: () => ({ x: 10, y: 20, z: 30 }), verify: () => true
};
vm.runInContext(fs.readFileSync(path.join(root, '.minecraft/kubejs/server_scripts/systems/spawn_pyramid/commands.js'), 'utf8'), scope);
vm.runInContext('spawnPyramidStatus(commandContext)', scope);
assert.equal(output.pop(), '状态: pending\n尝试次数: 2\n原点: 10 20 30\n已认领: true\n验证通过: true');
console.log('Passed: localized statistics, toggles, force-event response, unchanged event IDs/statistics keys, and spawn status. Minecraft runtime not tested.');

// Exercise actual current shop interaction handler, preserving stage gates and commands.
let shopHandler;
let shopCanceled = 0;
const shopMessages = [];
const shopCommands = [];
const shopPlayer = {
  username: 'Tester', mainHandItem: {}, offHandItem: {},
  stages: { has: () => false }
};
const shopEvent = {
  player: shopPlayer, target: { persistentData: { getStringOr: () => 'ftb:broker_mid' } },
  hand: 'MAIN_HAND', server: { runCommandSilent: value => shopCommands.push(value) },
  cancel: () => { shopCanceled++; }
};
shopPlayer.tell = message => shopMessages.push(message.value);
Message.prototype.color = function () { return this; };
Message.prototype.gray = function () { return this; };
const shopScope = {
  Text, console,
  Java: { loadClass: () => ({ get: () => ({ getProgress: () => ({ isPresent: () => false }) }) }) },
  Ingredient: { of: () => ({ test: () => false }) },
  keeperDefs: { broker_mid: { id: 'ftb:broker_mid', name: 'ftb.shopkeeper.broker_mid', color: 'gold', stage: 'ftb:broker_mid_wares' } },
  ItemEvents: { entityInteracted: handler => { shopHandler = handler; } }
};
vm.createContext(shopScope);
vm.runInContext(fs.readFileSync(path.join(root, '.minecraft/kubejs/server_scripts/systems/echoes/echo_shop_villagers.js'), 'utf8'), shopScope);
shopHandler(shopEvent);
assert.equal(shopCanceled, 1);
assert.equal(shopCommands.length, 0);
assert.match(shopMessages.pop(), /^经纪人代理: .*完成FTB天际号任务/);
shopPlayer.stages.has = () => true;
shopHandler(shopEvent);
assert.equal(shopCanceled, 2);
assert.equal(shopCommands.pop(), 'execute as Tester run ftbechoes open ftb:broker_mid');
shopEvent.hand = 'OFF_HAND';
shopHandler(shopEvent);
assert.equal(shopCanceled, 2);
console.log('Passed: current shop locked/unlocked/off-hand branches, localized keeper message, and unchanged open command.');
