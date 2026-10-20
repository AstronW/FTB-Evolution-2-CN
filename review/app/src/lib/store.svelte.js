// Shared review state: index, lazily loaded mod data, marks and filters.

export const ORIGINS = {
	project: '项目译文',
	pack: '整合包自带',
	mod: '模组自带',
	missing: '缺失'
};

export const TYPES = {
	lang: '语言键',
	manual: '手册',
	quest: '任务书',
	custom: '特色内容'
};

const TYPE_OF = { lang: 'lang', manual: 'manual', page: 'manual', quest: 'quest', custom: 'custom', code: 'custom' };

export const STATUSES = {
	all: '全部',
	todo: '未审查',
	ok: '已审查',
	flag: '有疑问',
	stale: '已过期'
};

export const app = $state({
	index: null,
	mods: {}, // id -> { sections } once loaded
	loading: {}, // id -> true while fetching
	marks: {},
	saving: 0,
	error: '',
	filter: {
		q: '',
		status: 'all',
		origins: { project: true, pack: true, mod: true, missing: true },
		types: { lang: true, manual: true, quest: true, custom: true },
		hideExcluded: true,
		sameOnly: false,
		tokenMismatch: false
	}
});

const TOKEN_RE = /%(?:\d+\$)?[sdfx%]|\{\d*\}|[&§][0-9a-fk-or]|<\/?[a-zA-Z][^>]*>|\$\([^)]*\)/g;

export function tokens(text) {
	return (text ?? '').match(TOKEN_RE) ?? [];
}

export function tokenMismatch(e) {
	if (e.zh == null || e.t === 'page' || e.t === 'code') return false;
	const a = tokens(e.en).filter((t) => !/^[&§]r$/.test(t)).sort().join('\u0000');
	const b = tokens(e.zh).filter((t) => !/^[&§]r$/.test(t)).sort().join('\u0000');
	return a !== b;
}

export function statusOf(e) {
	const m = app.marks[e.id];
	if (!m) return 'todo';
	return m.h === e.h ? m.s : 'stale';
}

export function matches(e) {
	const f = app.filter;
	if (!f.origins[e.o]) return false;
	if (!f.types[TYPE_OF[e.t]]) return false;
	if (f.hideExcluded && e.ex) return false;
	if (f.status !== 'all' && statusOf(e) !== f.status) return false;
	if (f.sameOnly && e.zh !== e.en) return false;
	if (f.tokenMismatch && !tokenMismatch(e)) return false;
	if (f.q) {
		const q = f.q.toLowerCase();
		if (
			!e.k.toLowerCase().includes(q) &&
			!e.en.toLowerCase().includes(q) &&
			!(e.zh ?? '').toLowerCase().includes(q)
		)
			return false;
	}
	return true;
}

export async function init() {
	const [index, marks] = await Promise.all([
		fetch('/data/index.json').then((r) => r.json()),
		fetch('/api/marks').then((r) => r.json())
	]);
	app.marks = marks.marks ?? {};
	app.index = index;
}

export async function loadMod(mod) {
	if (app.mods[mod.id] || app.loading[mod.id]) return;
	app.loading[mod.id] = true;
	try {
		const data = await fetch('/data/mods/' + mod.file).then((r) => r.json());
		app.mods[mod.id] = data;
	} catch (err) {
		app.error = `加载 ${mod.name} 失败: ${err}`;
	} finally {
		delete app.loading[mod.id];
	}
}

export async function loadAll() {
	const pending = app.index.mods.filter((m) => !app.mods[m.id]);
	for (let i = 0; i < pending.length; i += 8) {
		await Promise.all(pending.slice(i, i + 8).map(loadMod));
	}
}

/** @param {{id:string,h:string}[]} entries @param {string|null} s @param {string} group */
export async function setMarks(entries, s, group, note = '') {
	const updates = entries.map((e) => ({ id: e.id, h: e.h, s, g: group, note }));
	const at = new Date().toISOString();
	for (const u of updates) {
		if (s) app.marks[u.id] = { h: u.h, s, g: group, ...(note ? { note } : {}), at };
		else delete app.marks[u.id];
	}
	app.saving++;
	try {
		const r = await fetch('/api/marks', {
			method: 'POST',
			headers: { 'content-type': 'application/json' },
			body: JSON.stringify({ updates })
		});
		if (!r.ok) throw new Error(r.status + ' ' + r.statusText);
	} catch (err) {
		app.error = '保存失败: ' + err;
	} finally {
		app.saving--;
	}
}

/** Reviewed count for a mod, usable before its data is loaded. */
export function reviewedCount(mod) {
	const data = app.mods[mod.id];
	if (data) {
		let n = 0;
		for (const s of data.sections) for (const e of s.entries) if (app.marks[e.id]?.h === e.h) n++;
		return n;
	}
	let n = 0;
	for (const m of Object.values(app.marks)) if (m.g === mod.id) n++;
	return n;
}

export function escapeHtml(s) {
	return s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
}

/** Escape text and wrap placeholders / format codes / query hits in spans. */
export function highlight(text, q) {
	if (text == null) return '';
	let out = '';
	let last = 0;
	for (const m of text.matchAll(TOKEN_RE)) {
		out += hitMark(text.slice(last, m.index), q);
		out += `<span class="tok">${escapeHtml(m[0])}</span>`;
		last = m.index + m[0].length;
	}
	return out + hitMark(text.slice(last), q);
}

function hitMark(s, q) {
	if (!q) return escapeHtml(s);
	const lower = s.toLowerCase();
	const ql = q.toLowerCase();
	let out = '';
	let i = 0;
	for (;;) {
		const j = lower.indexOf(ql, i);
		if (j < 0) return out + escapeHtml(s.slice(i));
		out += escapeHtml(s.slice(i, j)) + '<mark>' + escapeHtml(s.slice(j, j + q.length)) + '</mark>';
		i = j + q.length;
	}
}
