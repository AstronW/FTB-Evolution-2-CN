// Nutritional 1.2.3 constructs a literal prefix, bypassing its language key.
// KubeJS handles ItemTooltipEvent at LOW priority, after Nutritional.
ItemEvents.modifyTooltips(event => {
    event.modifyAll(builder => builder.dynamic('ftb_cn_nutrients'))
})
ItemEvents.dynamicTooltips('ftb_cn_nutrients', event => {
    // Follow the selected language; preserve English when Chinese is inactive.
    if (Text.translate('tooltip.nutritional.nutrients', ['']).getString() !== '营养: ') return
    for (let i = 0; i < event.lines.size(); i++) {
        const line = event.lines.get(i)
        if (!line.getString().startsWith('Nutrients: ')) continue
        const siblings = line.getSiblings()
        // Exact structure emitted by NutritionTooltip.onTooltip in the bound JAR.
        // Do not flatten children: nutrient colors and amount styles must survive.
        if (line.getContents().text() !== 'Nutrients: ') continue
        const translated = Text.of('营养: ').setStyle(line.getStyle())
        for (let j = 0; j < siblings.size(); j++) translated.append(siblings.get(j).copy())
        event.lines.set(i, translated)
    }
})
