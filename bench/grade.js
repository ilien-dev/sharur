// usage: node grade.js  -> grades every out/*.jsonl lacking out/*.grade.json
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const dir = path.join(__dirname, 'out'), rub = JSON.parse(fs.readFileSync(path.join(__dirname, 'rubrics.json')));
const prompts = fs.readFileSync(path.join(__dirname, 'prompts.txt'), 'utf8').split('\n');
const gdir = path.join(__dirname, 'grader'); fs.mkdirSync(gdir, { recursive: true });
const jobs = [];
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.jsonl'))) {
  const m = f.match(/^(.+)_p(\d+)_r(\d+)\.jsonl$/); if (!m || !rub[m[2]]) continue;
  const g = path.join(dir, f.replace('.jsonl', '.grade.json')); if (fs.existsSync(g)) continue;
  let text = '';
  for (const l of fs.readFileSync(path.join(dir, f), 'utf8').split('\n')) {
    if (!l.trim()) continue; let j; try { j = JSON.parse(l) } catch { continue }
    if (j.type === 'assistant') for (const c of j.message.content) if (c.type === 'text') text += c.text + '\n';
  }
  const q = `A developer asked a coding assistant: "${prompts[m[2] - 1]}"
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
function next() {
  if (i >= jobs.length) return; const { g, q } = jobs[i++];
  const p = spawn('claude -p --model haiku --setting-sources project --no-session-persistence --system-prompt "You are a strict grader. Output only JSON."', { shell: true, cwd: gdir });
  let o = ''; p.stdout.on('data', d => o += d);
  p.on('close', () => { const m = o.match(/\{[\s\S]*\}/); if (m) try { JSON.parse(m[0]); fs.writeFileSync(g, m[0]) } catch { } next() });
  p.stdin.end(q);
}
for (let k = 0; k < 10; k++) next();
