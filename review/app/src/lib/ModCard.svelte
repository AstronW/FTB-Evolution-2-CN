<script>
	import Section from './Section.svelte';
	import { app, loadMod, matches, reviewedCount, ORIGINS } from './store.svelte.js';

	let { mod, open = $bindable() } = $props();

	let data = $derived(app.mods[mod.id]);
	let filtered = $derived(
		data ? data.sections.reduce((n, s) => n + s.entries.filter(matches).length, 0) : null
	);
	let done = $derived(reviewedCount(mod));
	let openSections = $state({});

	$effect(() => {
		if (open) loadMod(mod);
	});
</script>

{#if filtered !== 0}
	<article class="mod" id={'mod-' + mod.id}>
		<button class="head" onclick={() => (open = !open)} aria-expanded={open}>
			<span class="caret">{open ? '▾' : '▸'}</span>
			<span class="name">{mod.name}</span>
			{#if mod.zh}<span class="zh">{mod.zh}</span>{/if}
			<code class="id">{mod.id}</code>
			{#if mod.excluded}<span class="badge">排除范围</span>{/if}
			<span class="stats">
				{#each Object.keys(ORIGINS) as o}
					{#if mod.counts[o]}<span class="badge o-{o}" title={ORIGINS[o]}>{mod.counts[o]}</span>{/if}
				{/each}
				{#if filtered != null && filtered !== mod.counts.total}<span class="hit">筛选 {filtered}</span>{/if}
				<span class="progress" title="已审查 {done}/{mod.counts.total}">
					<span style="width: {(100 * done) / mod.counts.total}%"></span>
				</span>
				<span class="pct">{done}/{mod.counts.total}</span>
			</span>
		</button>
		{#if open}
			<div class="body">
				{#if !data}
					<p class="loading">加载中…</p>
				{:else}
					{#each data.sections as section (section.id)}
						<Section {section} group={mod.id} bind:open={openSections[section.id]} />
					{/each}
				{/if}
			</div>
		{/if}
	</article>
{/if}

<style>
	.mod {
		background: var(--card);
		border: 1px solid var(--line);
		border-radius: 8px;
		margin-bottom: 10px;
		overflow: clip;
		--sticky-top: calc(var(--bar-h) + 44px);
	}
	.head {
		all: unset;
		box-sizing: border-box;
		cursor: pointer;
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		align-items: center;
		width: 100%;
		padding: 10px 12px;
		position: sticky;
		top: var(--bar-h);
		z-index: 2;
		background: var(--card);
		min-height: 44px;
	}
	.head:hover {
		background: var(--hover);
	}
	.caret {
		width: 1em;
		color: var(--muted);
	}
	.name {
		font-weight: 650;
	}
	.zh {
		color: var(--muted);
	}
	.id {
		font-size: 11.5px;
		color: var(--muted);
	}
	.stats {
		margin-left: auto;
		display: flex;
		gap: 6px;
		align-items: center;
	}
	.hit {
		font-size: 12px;
		color: var(--accent);
	}
	.progress {
		display: inline-block;
		width: 80px;
		height: 6px;
		border-radius: 3px;
		background: var(--line);
		overflow: hidden;
	}
	.progress span {
		display: block;
		height: 100%;
		background: var(--ok);
	}
	.pct {
		font-size: 12px;
		color: var(--muted);
		min-width: 6em;
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	.loading {
		padding: 12px;
		color: var(--muted);
	}
</style>
