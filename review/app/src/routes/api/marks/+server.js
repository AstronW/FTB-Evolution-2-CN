import { json } from '@sveltejs/kit';
import fs from 'node:fs';
import path from 'node:path';

// Review marks live next to the exporter, outside the generated data, so a
// re-export never discards them. A mark records the hash of the EN/ZH pair it
// was made against; the client treats a changed hash as stale.
// Run from review/app (npm run dev / preview); REVIEW_MARKS overrides the path.
const FILE = path.resolve(process.env.REVIEW_MARKS ?? '../marks.json');

function load() {
	try {
		return JSON.parse(fs.readFileSync(FILE, 'utf8'));
	} catch {
		return { version: 1, marks: {} };
	}
}

function save(data) {
	const tmp = FILE + '.tmp';
	fs.writeFileSync(tmp, JSON.stringify(data, null, 1) + '\n');
	fs.renameSync(tmp, FILE);
}

export function GET() {
	return json(load());
}

/** Body: { updates: [{ id, h, g, s: 'ok' | 'flag', note? } | { id, s: null }] } */
export async function POST({ request }) {
	const { updates } = await request.json();
	const data = load();
	const at = new Date().toISOString();
	for (const u of updates ?? []) {
		if (typeof u.id !== 'string') continue;
		if (!u.s) delete data.marks[u.id];
		else data.marks[u.id] = { h: u.h, s: u.s, ...(u.g ? { g: u.g } : {}), ...(u.note ? { note: u.note } : {}), at };
	}
	save(data);
	return json({ ok: true, count: Object.keys(data.marks).length });
}
