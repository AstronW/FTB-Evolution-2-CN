<script>
	import Entry from './Entry.svelte';
	import { app, matches, statusOf, setMarks } from './store.svelte.js';

	let { section, group, open = $bindable() } = $props();

	const PAGE = 100;
	let limit = $state(PAGE);
	let visible = $derived(section.entries.filter(matches));
	let done = $derived(section.entries.filter((e) => app.marks[e.id]?.h === e.h).length);

	$effect(() => {
		// reset paging when the filter changes
		app.filter.q;
		app.filter.status;
		limit = PAGE;
	});

	function markVisible() {
		const todo = visible.filter((e) => statusOf(e) !== 'ok' && statusOf(e) !== 'flag');
		if (todo.length && confirm(`将本节当前筛选下的 ${todo.length} 条标记为已审查?`)) setMarks(todo, 'ok', group);
	}
</script>

{#if visible.length}
	<section class="sec">
		<button class="head" onclick={() => (open = !open)} aria-expanded={open}>
			<span class="caret">{open ? '▾' : '▸'}</span>
			<span class="title">{section.title}</span>
			<span class="count">{visible.length} 条 · 已审 {done}/{section.entries.length}</span>
		</button>
		{#if open}
			<div class="tools">
				<button class="btn small" onclick={markVisible}>本节筛选结果全部标为已审查</button>
			</div>
			{#each visible.slice(0, limit) as e (e.id)}
				<Entry {e} {group} />
			{/each}
			{#if visible.length > limit}
				<button class="more" onclick={() => (limit += PAGE * 3)}>
					显示更多 (剩余 {visible.length - limit})
				</button>
			{/if}
		{/if}
	</section>
{/if}

<style>
	.sec {
		border-top: 1px solid var(--line);
	}
	.head {
		all: unset;
		box-sizing: border-box;
		cursor: pointer;
		display: flex;
		gap: 8px;
		align-items: baseline;
		width: 100%;
		padding: 8px 12px;
		background: var(--sec-bg);
		position: sticky;
		top: var(--sticky-top, 0);
		z-index: 1;
	}
	.head:hover {
		background: var(--hover);
	}
	.caret {
		width: 1em;
		color: var(--muted);
	}
	.title {
		font-weight: 600;
		font-size: 14px;
		word-break: break-all;
	}
	.count {
		margin-left: auto;
		font-size: 12px;
		color: var(--muted);
		white-space: nowrap;
	}
	.tools {
		padding: 6px 12px;
		display: flex;
		justify-content: flex-end;
	}
	@media (max-width: 760px) {
		.head {
			position: static;
		}
	}
	.more {
		all: unset;
		cursor: pointer;
		display: block;
		width: 100%;
		text-align: center;
		padding: 10px;
		color: var(--accent);
		border-top: 1px solid var(--line);
	}
</style>
