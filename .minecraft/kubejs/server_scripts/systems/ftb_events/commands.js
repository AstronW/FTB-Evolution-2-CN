// priority: 99
const $Permissions = Java.loadClass("net.minecraft.server.permissions.Permissions");

const canManageEvents = (src) => {
  try {
    return src.permissions().hasPermission($Permissions.COMMANDS_ADMIN);
  } catch (e) {
    console.warn("[ftb_events] permission check unavailable: " + e);
    return false;
  }
};

const localizedEventName = (name) => {
  const keys = {
    "Frog and Squids": "ftb.custom.events.name.frog",
    "Treasure Goblin": "ftb.custom.events.name.treasure_goblin",
    "Fairy Event": "ftb.custom.events.name.fairy",
    "Apotheosis Boss Event": "ftb.custom.events.name.apotheosis",
    "Wandering Trader": "ftb.custom.events.name.trader",
    "Creeper": "ftb.custom.events.name.creeper",
    "Gunslinger Duel": "ftb.custom.events.name.gunslinger",
    "Phantom Bomber Event": "ftb.custom.events.name.phantom",
    "Goat": "ftb.custom.events.name.goat",
    "Allay Trade Event": "ftb.custom.events.name.allay"
};
  return keys[String(name)] ? Text.translate(keys[String(name)]) : Text.of(String(name));
};

const toggleEventForPlayer = (eventObj, ctx) => {
  let source = ctx.getSource();
  let player = source.getPlayerOrException();

  if (eventObj.disableStage && !EventLib.hasStage(player, eventObj.disableStage)) {
    source.sendSuccess(Text.translate("ftb.event_system.commands.disablefail").red(), false);
    return 0;
  }

  let disabled = checks.player.getDisabledEvents(player);
  let index = disabled.indexOf(eventObj.name);
  if (index !== -1) {
    disabled.splice(index, 1);
    player.persistentData.disabledEvents = disabled;
    source.sendSuccess(Text.translate("ftb.event_system.commands.toggle.on", [localizedEventName(eventObj.displayName)]).green(), false);
  } else {
    disabled.push(eventObj.name);
    player.persistentData.disabledEvents = disabled;
    source.sendSuccess(Text.translate("ftb.event_system.commands.toggle.off", [localizedEventName(eventObj.displayName)]).green(), false);
  }
  return 1;
};

const forceEvent = (ctx, target, eventObj) => {
  let source = ctx.getSource();
  target = target ?? source.getPlayerOrException();

  let chosenEvent = eventObj ?? checks.event.getRandomEvent(ftbEvents);
  if (!chosenEvent) return 0;

  let locationInfo = null;
  if (chosenEvent.size >= 0) {
    locationInfo = checks.event.findSpawnLocation(chosenEvent, target, 500);
    if (!locationInfo) {
      source.sendSuccess(Text.translate("ftb.event_system.spawn.not_found", [localizedEventName(chosenEvent.displayName)]).red(), false);
      return 0;
    }
  }

  chosenEvent.execute(ctx, target, locationInfo);
  Statistics().addSuccess(chosenEvent.displayName);
  source.sendSuccess(
    Text.translate("ftb.event_system.commands.force.success", [localizedEventName(chosenEvent.displayName), target.username]).green(),
    false
  );
  return 1;
};

ServerEvents.commandRegistry((event) => {
  let { commands: Commands, arguments: Arguments } = event;

  let forceBranch = (eventObj, literal) =>
    Commands.literal(literal)
      .executes((ctx) => forceEvent(ctx, null, eventObj))
      .then(
        Commands.argument("target", Arguments.PLAYER.create(event)).executes((ctx) =>
          forceEvent(ctx, Arguments.PLAYER.getResult(ctx, "target"), eventObj)
        )
      );

  let settingsArgs = {
    timerDelay: Arguments.INTEGER,
    debug: Arguments.BOOLEAN,
    maxAttempts: Arguments.INTEGER,
    timeCooldown: Arguments.INTEGER,
  };

  event.register(
    Commands.literal("events")
      .then(Commands.literal("force").requires(canManageEvents).then(forceBranch(null, "ftb:random")))
      .then(
        Commands.literal("statistics")
          .requires(canManageEvents)
          .executes((ctx) => {
            let source = ctx.getSource();
            let data = Statistics().data();
            let lines = [Text.translate("ftb.custom.events.total", [String(Statistics().totalEvents())]), "=============================="];
            Object.keys(data.failure).forEach((key) => lines.push(Text.translate("ftb.custom.events.failed", [localizedEventName(key), String(data.failure[key])])));
            lines.push("==============================");
            Object.keys(data.success).forEach((key) => lines.push(Text.translate("ftb.custom.events.succeeded", [localizedEventName(key), String(data.success[key])])));
            source.sendSuccess(lines.reduce((message, line, index) => {
              if (index) message.append("\n");
              return message.append(line);
            }, Text.of("")), false);
            return 1;
          })
          .then(
            Commands.literal("reset")
              .requires(canManageEvents)
              .executes((ctx) => {
                Statistics().reset();
                ctx.getSource().sendSuccess(Text.translate("ftb.event_system.commands.statistics.reset").green(), false);
                return 1;
              })
          )
      )
      .then(
        Commands.literal("settings")
          .requires(canManageEvents)
          .then(
            Commands.literal("list").executes((ctx) => {
              let source = ctx.getSource();
              let settings = eventSettingsOf(source.getServer());
              let lines = Object.keys(defaultEventSettings).map((key) => {
                if (key === "debug") return key + ": " + settings.getBooleanOr(key, defaultEventSettings[key]);
                return key + ": " + settings.getIntOr(key, defaultEventSettings[key]);
              });
              source.sendSuccess(Text.of(lines.join("\n")), false);
              return 1;
            })
          )
      )
  );

  Object.keys(settingsArgs).forEach((key) => {
    event.register(
      Commands.literal("events").then(
        Commands.literal("settings").then(
          Commands.literal("set")
            .requires(canManageEvents)
            .then(
              Commands.literal(key).then(
                Commands.argument(key, settingsArgs[key].create(event)).executes((ctx) => {
                  let source = ctx.getSource();
                  let settings = eventSettingsOf(source.getServer());
                  let value = settingsArgs[key].getResult(ctx, key);
                  if (key === "debug") {
                    value = String(value) === "true";
                    settings.putBoolean(key, value);
                  } else {
                    value = parseInt(String(value), 10);
                    settings.putInt(key, value);
                  }
                  source.sendSuccess(Text.translate("ftb.event_system.commands.settings.set", [key, value]).green(), false);
                  return 1;
                })
              )
            )
        )
      )
    );
  });

  ftbEvents.forEach((ftbEvent) => {
    event.register(
      Commands.literal("events")
        .then(
          Commands.literal("toggle").then(
            Commands.literal(ftbEvent.name).executes((ctx) => toggleEventForPlayer(ftbEvent, ctx))
          )
        )
        .then(Commands.literal("force").requires(canManageEvents).then(forceBranch(ftbEvent, ftbEvent.name)))
    );
  });

  ftbEventsInactive.forEach((ftbEvent) => {
    event.register(
      Commands.literal("events").then(
        Commands.literal("force").requires(canManageEvents).then(forceBranch(ftbEvent, ftbEvent.name))
      )
    );
    if (!ftbEvent.toggleable) return;
    event.register(
      Commands.literal("events").then(
        Commands.literal("toggle").then(
          Commands.literal(ftbEvent.name).executes((ctx) => toggleEventForPlayer(ftbEvent, ctx))
        )
      )
    );
  });
});
