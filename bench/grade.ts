// usage: node grade.ts  -> grades every out/*.jsonl lacking out/*.grade.json
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { events } from './types.ts';

const here = import.meta.dirname;
const dir = path.join(here, 'out');
const rub: Record<string, string[]> = JSON.parse(fs.readFileSync(path.join(here, 'rubrics.json'), 'utf8'));
const prompts = fs.readFileSync(path.join(here, 'prompts.txt'), 'utf8').split('\n');
const gdir = path.join(here, 'grader'); fs.mkdirSync(gdir, { recursive: true });
const jobs: { g: string; q: string }[] = [];
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.jsonl'))) {
  const m = f.match(/^(.+)_p(\d+)_r(\d+)\.jsonl$/); if (!m || !rub[m[2]]) continue;
  const g = path.join(dir, f.replace('.jsonl', '.grade.json')); if (fs.existsSync(g)) continue;
  let text = '';
  for (const j of events(fs.readFileSync(path.join(dir, f), 'utf8')))
    if (j.type === 'assistant') for (const c of j.message.content) if (c.type === 'text') text += c.text + '\n';
  const q = `A developer asked a coding assistant: "${prompts[+m[2] - 1]}"
The assistant did the work and replied with ONLY this text:
<reply>
${text.trim()}
</reply>

For each criterion decide if the reply clearly conveys it (true/false):
${rub[m[2]].map((c, i) => `${i + 1}. ${c}`).join('\n')}

Also: "clear" = can a developer understand the reply without guessing at garbled words or ambiguous shorthand (true/false).
Output ONLY JSON: {"criteria":[true,...],"clear":true}`;
  jobs.push({ g, q });
}
let i = 0;
function next(): void {
  if (i >= jobs.length) return; const { g, q } = jobs[i++];
  const p = spawn('claude -p --model haiku --setting-sources project --no-session-persistence --system-prompt "You are a strict grader. Output only JSON."', { shell: true, cwd: gdir });
  let o = ''; p.stdout.on('data', (d: Buffer) => o += d);
  p.on('close', () => { const m = o.match(/\{[\s\S]*\}/); if (m) try { JSON.parse(m[0]); fs.writeFileSync(g, m[0]) } catch { } next() });
  p.stdin.end(q);
}
for (let k = 0; k < 10; k++) next();
