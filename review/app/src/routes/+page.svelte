<script>
	import { onMount, tick } from 'svelte';
	import ModCard from '$lib/ModCard.svelte';
	import { app, init, loadAll, reviewedCount, ORIGINS, TYPES, STATUSES } from '$lib/store.svelte.js';
	import '$lib/app.css';

	let openMods = $state({});
	let modQuery = $state('');
	let allLoaded = $state(false);
	let loadingAll = $state(false);
	let qInput = $state('');
	let sidebar = $state(false);

	let bar;
	onMount(() => {
		init().catch((err) => (app.error = '初始化失败: ' + err));
		// sticky mod/section headers sit just below the (possibly wrapping) top bar
		const ro = new ResizeObserver(() =>
			document.documentElement.style.setProperty('--bar-h', bar.offsetHeight + 'px')
		);
		ro.observe(bar);
		return () => ro.disconnect();
	});

	// Debounce the free-text query so typing stays responsive on large data.
	let timer;
	$effect(() => {
		const v = qInput;
		clearTimeout(timer);
		timer = setTimeout(() => (app.filter.q = v.trim()), 250);
	});

	let filterActive = $derived.by(() => {
		const f = app.filter;
		return (
			f.q !== '' ||
			f.status !== 'all' ||
			f.sameOnly ||
			f.tokenMismatch ||
			Object.values(f.origins).some((v) => !v) ||
			Object.values(f.types).some((v) => !v)
		);
	});

	$effect(() => {
		if (filterActive && app.index && !allLoaded && !loadingAll) {
			loadingAll = true;
			loadAll().then(() => {
				allLoaded = true;
				loadingAll = false;
			});
		}
	});

	let mods = $derived.by(() => {
		if (!app.index) return [];
		return app.index.mods.filter((m) => !(app.filter.hideExcluded && m.excluded));
	});

	let sideMods = $derived.by(() => {
		const q = modQuery.trim().toLowerCase();
		return q
			? mods.filter((m) => (m.name + ' ' + m.zh + ' ' + m.id).toLowerCase().includes(q))
			: mods;
	});

	let totals = $derived.by(() => {
		let total = 0;
		for (const m of mods) total += m.counts.total;
		const c = { ok: 0, flag: 0 };
		for (const v of Object.values(app.marks)) if (v.s in c) c[v.s]++;
		return { total, ...c };
	});

	async function jump(mod) {
		openMods[mod.id] = true;
		sidebar = false;
		await tick();
		document.getElementById('mod-' + mod.id)?.scrollIntoView({ block: 'start' });
	}

	function setAll(open) {
		for (const m of mods) openMods[m.id] = open;
	}

	function resetFilters() {
		qInput = '';
		Object.assign(app.filter, { q: '', status: 'all', sameOnly: false, tokenMismatch: false });
		for (const k in app.filter.origins) app.filter.origins[k] = true;
		for (const k in app.filter.types) app.filter.types[k] = true;
	}
</script>

<div class="layout">
	<header class="bar" bind:this={bar}>
		<button class="btn menu" onclick={() => (sidebar = !sidebar)} aria-label="模组列表">☰</button>
		<h1>FTB Evolution 2 汉化审查</h1>
		{#if app.index}<span class="ver">整合包 {app.index.pack}</span>{/if}
		<input class="search" type="search" placeholder="搜索键名 / 英文 / 中文" bind:value={qInput} />
		<span class="summary">
			共 {totals.total.toLocaleString()} 条 · 已审 <b class="c-ok">{totals.ok.toLocaleString()}</b> · 疑问
			<b class="c-flag">{totals.flag}</b>
			{#if app.saving}<span class="saving">保存中…</span>{/if}
		</span>
	</header>

	<div class="filters">
		<label>
			状态
			<select bind:value={app.filter.status}>
				{#each Object.entries(STATUSES) as [k, v]}<option value={k}>{v}</option>{/each}
			</select>
		</label>
		<fieldset>
			<legend>来源</legend>
			{#each Object.entries(ORIGINS) as [k, v]}
				<label class="chk"><input type="checkbox" bind:checked={app.filter.origins[k]} />{v}</label>
			{/each}
		</fieldset>
		<fieldset>
			<legend>类型</legend>
			{#each Object.entries(TYPES) as [k, v]}
				<label class="chk"><input type="checkbox" bind:checked={app.filter.types[k]} />{v}</label>
			{/each}
		</fieldset>
		<fieldset>
			<legend>其他</legend>
			<label class="chk"><input type="checkbox" bind:checked={app.filter.hideExcluded} />隐藏排除范围</label>
			<label class="chk"><input type="checkbox" bind:checked={app.filter.sameOnly} />仅与原文相同</label>
			<label class="chk"><input type="checkbox" bind:checked={app.filter.tokenMismatch} />仅占位符不一致</label>
		</fieldset>
		<span class="grow"></span>
		{#if loadingAll}<span class="muted">正在加载全部数据以筛选…</span>{/if}
		<button class="btn small" onclick={resetFilters}>重置筛选</button>
		<button class="btn small" onclick={() => setAll(true)}>全部展开</button>
		<button class="btn small" onclick={() => setAll(false)}>全部折叠</button>
	</div>

	{#if app.error}
		<div class="error" role="alert">
			{app.error} <button class="btn small" onclick={() => (app.error = '')}>关闭</button>
		</div>
	{/if}

	<div class="main">
		<aside class="side" class:show={sidebar}>
			<input type="search" placeholder="筛选模组" bind:value={modQuery} />
			<ul>
				{#each sideMods as m (m.id)}
					{@const done = reviewedCount(m)}
					<li>
						<button onclick={() => jump(m)} class:full={done === m.counts.total}>
							<span class="n" title={m.zh ? `${m.zh} (${m.name})` : m.name}>
								{#if m.zh}{m.zh} <span class="en">{m.name}</span>{:else}{m.name}{/if}
							</span>
							<span class="c">{done}/{m.counts.total}</span>
						</button>
					</li>
				{/each}
			</ul>
		</aside>

		<main class="list">
			{#if !app.index}
				<p class="muted">加载索引…</p>
			{:else}
				{#each mods as mod (mod.id)}
					<ModCard {mod} bind:open={openMods[mod.id]} />
				{/each}
				{#if filterActive && allLoaded}
					<p class="muted end">筛选结束</p>
				{/if}
			{/if}
		</main>
	</div>
</div>

<style>
	.layout {
		min-height: 100vh;
	}
	.bar {
		position: sticky;
		top: 0;
		z-index: 10;
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		align-items: center;
		padding: 10px 16px;
		background: var(--bar);
		border-bottom: 1px solid var(--line);
	}
	h1 {
		font-size: 17px;
		margin: 0;
	}
	.ver {
		color: var(--muted);
		font-size: 13px;
	}
	.search {
		flex: 1;
		min-width: 200px;
		max-width: 520px;
	}
	.summary {
		font-size: 13px;
		color: var(--muted);
		margin-left: auto;
	}
	.c-ok {
		color: var(--ok);
	}
	.c-flag {
		color: var(--flag);
	}
	.saving {
		margin-left: 6px;
		color: var(--accent);
	}
	.menu {
		display: none;
	}
	.filters {
		display: flex;
		flex-wrap: wrap;
		gap: 10px 16px;
		align-items: center;
		padding: 8px 16px;
		border-bottom: 1px solid var(--line);
		font-size: 13px;
	}
	fieldset {
		border: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 4px 10px;
		align-items: center;
	}
	legend {
		float: left;
		white-space: nowrap;
		color: var(--muted);
		margin-right: 4px;
	}
	.chk {
		display: inline-flex;
		gap: 4px;
		align-items: center;
		white-space: nowrap;
	}
	.grow {
		flex: 1;
	}
	.muted {
		color: var(--muted);
	}
	.error {
		margin: 8px 16px;
		padding: 8px 12px;
		border-radius: 6px;
		background: var(--flag-bg);
		color: var(--bad);
	}
	.main {
		display: grid;
		grid-template-columns: 260px 1fr;
		gap: 16px;
		padding: 12px 16px;
	}
	.side {
		position: sticky;
		top: calc(var(--bar-h) + 12px);
		align-self: start;
		max-height: calc(100vh - var(--bar-h) - 24px);
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.side ul {
		list-style: none;
		margin: 0;
		padding: 0;
		overflow: auto;
	}
	.side li button {
		all: unset;
		box-sizing: border-box;
		cursor: pointer;
		display: flex;
		gap: 6px;
		width: 100%;
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 13px;
	}
	.side li button:hover {
		background: var(--hover);
	}
	.side li button.full .n {
		color: var(--ok);
	}
	.side .n {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.side .n .en {
		color: var(--muted);
		font-size: 11.5px;
	}
	.side .c {
		color: var(--muted);
		font-variant-numeric: tabular-nums;
		font-size: 12px;
	}
	.list {
		min-width: 0;
	}
	.end {
		text-align: center;
	}
	@media (max-width: 900px) {
		.main {
			grid-template-columns: 1fr;
		}
		.menu {
			display: inline-block;
		}
		.side {
			display: none;
		}
		.side.show {
			display: flex;
			position: fixed;
			inset: 56px 0 0 0;
			max-height: none;
			z-index: 20;
			background: var(--bg);
			padding: 12px 16px;
		}
	}
</style>
