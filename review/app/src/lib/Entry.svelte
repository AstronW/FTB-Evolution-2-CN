<script>
	import { app, ORIGINS, statusOf, tokenMismatch, highlight, setMarks } from './store.svelte.js';

	let { e, group } = $props();

	let status = $derived(statusOf(e));
	let mark = $derived(app.marks[e.id]);
	let mismatch = $derived(tokenMismatch(e));
	let long = $derived(e.t === 'page' || e.t === 'code' || e.en.length > 600);
	let editing = $state(false);
	let note = $state('');

	function toggle(s) {
		if (s === 'flag' && status !== 'flag') {
			note = mark?.note ?? '';
			editing = true;
			return;
		}
		setMarks([e], status === s ? null : s, group);
	}

	function saveNote() {
		editing = false;
		setMarks([e], 'flag', group, note.trim());
	}
</script>

<div class="entry st-{status}" class:excluded={e.ex}>
	<div class="meta">
		<code class="key" title={e.id}>{e.k}</code>
		<span class="badge o-{e.o}">{ORIGINS[e.o]}</span>
		{#if e.eo === 'kubejs'}<span class="badge">整合包改写原文</span>{/if}
		{#if e.ex}<span class="badge">排除范围</span>{/if}
		{#if e.zh != null && e.zh === e.en}<span class="badge warn">与原文相同</span>{/if}
		{#if mismatch}<span class="badge bad">占位符/格式码不一致</span>{/if}
		{#if status === 'stale'}<span class="badge warn">标记后内容已变</span>{/if}
		<span class="spacer"></span>
		<button class="btn ok" class:on={status === 'ok'} onclick={() => toggle('ok')} title="标记为已审查">
			✓ 已审查
		</button>
		<button class="btn flag" class:on={status === 'flag'} onclick={() => toggle('flag')} title="标记为有疑问">
			⚑ 疑问
		</button>
	</div>
	<div class="pair" class:long>
		<div class="text en" lang="en">{@html highlight(e.en, app.filter.q)}</div>
		<div class="text zh" lang="zh-CN">
			{#if e.zh == null}<span class="none">(无译文)</span>{:else}{@html highlight(e.zh, app.filter.q)}{/if}
			{#if e.up}<div class="upstream">上游原译: {@html highlight(e.up, app.filter.q)}</div>{/if}
		</div>
	</div>
	{#if editing}
		<form class="note" onsubmit={(ev) => (ev.preventDefault(), saveNote())}>
			<input bind:value={note} placeholder="疑问说明 (可留空)" autofocus />
			<button class="btn" type="submit">保存</button>
			<button class="btn" type="button" onclick={() => (editing = false)}>取消</button>
		</form>
	{:else if status === 'flag' && mark?.note}
		<div class="note-text">⚑ {mark.note}</div>
	{/if}
</div>

<style>
	.entry {
		border-top: 1px solid var(--line);
		padding: 8px 12px 10px;
		border-left: 3px solid transparent;
	}
	.entry.st-ok {
		border-left-color: var(--ok);
		background: var(--ok-bg);
	}
	.entry.st-flag {
		border-left-color: var(--flag);
		background: var(--flag-bg);
	}
	.entry.st-stale {
		border-left-color: var(--warn);
	}
	.meta {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		align-items: center;
		margin-bottom: 6px;
	}
	.key {
		font-size: 12px;
		color: var(--muted);
		word-break: break-all;
	}
	.spacer {
		flex: 1;
	}
	.pair {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
	}
	.text {
		white-space: pre-wrap;
		word-break: break-word;
		line-height: 1.55;
		font-size: 14px;
	}
	.long .text {
		max-height: 60vh;
		overflow: auto;
		font-family: var(--mono);
		font-size: 12.5px;
		background: var(--code-bg);
		padding: 8px;
		border-radius: 6px;
	}
	.none {
		color: var(--bad);
		font-style: italic;
	}
	.upstream {
		margin-top: 6px;
		font-size: 12.5px;
		color: var(--muted);
		border-top: 1px dashed var(--line);
		padding-top: 4px;
	}
	.note {
		display: flex;
		gap: 6px;
		margin-top: 8px;
	}
	.note input {
		flex: 1;
	}
	.note-text {
		margin-top: 6px;
		font-size: 13px;
		color: var(--flag);
	}
	.excluded {
		opacity: 0.7;
	}
	@media (max-width: 760px) {
		.pair {
			grid-template-columns: 1fr;
		}
	}
</style>
