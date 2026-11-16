// Turns raw `claude -p --output-format stream-json` logs into results/runs.json.
// Raw logs are not published: their init event lists the local machine's paths and plugins.
// usage: node export.js <outDir>[:round] ... > runs.json
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const runs = [];
for (const arg of process.argv.slice(2)) {
  const [d, round] = arg.split(':'); const dir = path.resolve(__dirname, d);
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.jsonl'))) {
    const m = f.match(/^(full-)?(.+)_p(\d+)_r(\d+)\.jsonl$/); if (!m) continue;
    let reply = '', tools = [], res = null;
    for (const l of fs.readFileSync(path.join(dir, f), 'utf8').split('\n')) {
      if (!l.trim()) continue; let j; try { j = JSON.parse(l) } catch { continue }
      if (j.type === 'assistant') for (const c of j.message.content) { if (c.type === 'text') reply += c.text + '\n'; if (c.type === 'tool_use') tools.push(c.name) }
      if (j.type === 'result') res = j;
    }
    if (!res) continue;
    reply = reply.trim();
    const r = {
      round: round || null, env: m[1] ? 'full' : 'clean', model: Object.keys(res.modelUsage || {})[0] || null,
      style: m[2], prompt: +m[3], rep: +m[4],
      words: reply.split(/\s+/).filter(Boolean).length, chars: reply.length,
      output_tokens: res.usage.output_tokens,
      input_tokens: res.usage.input_tokens + res.usage.cache_creation_input_tokens + res.usage.cache_read_input_tokens,
      tool_calls: tools.length, tools, cost_usd: +res.total_cost_usd.toFixed(4), is_error: !!res.is_error,
      grade: null, task_ok: null, reply,
    };
    const g = path.join(dir, f.replace('.jsonl', '.grade.json'));
    if (fs.existsSync(g)) r.grade = JSON.parse(fs.readFileSync(g));
    // Objective checks on the files the run left behind (only where the run directory still exists).
    const rd = path.join(__dirname, 'runs', f.replace('.jsonl', ''));
    if (round !== '1' && fs.existsSync(rd)) {
      const rf = n => { try { return fs.readFileSync(path.join(rd, n), 'utf8') } catch { return '' } };
      const sh = c => { try { return execSync(c, { cwd: rd, stdio: ['ignore', 'pipe', 'ignore'] }).toString() } catch (e) { return (e.stdout || '').toString() } };
      if (r.prompt === 2) r.task_ok = sh('python test_calc.py').includes('ok');
      if (r.prompt === 4) r.task_ok = /def multiply/.test(rf('calc.py')) && /multiply/.test(rf('test_calc.py'));
      if (r.prompt === 11) { const a = rf('calc.py') + rf('test_calc.py'); r.task_ok = /def mean/.test(a) && !/average/.test(a) }
    }
    runs.push(r);
  }
}
runs.sort((a, b) => (a.round + a.env + a.style).localeCompare(b.round + b.env + b.style) || a.prompt - b.prompt || a.rep - b.rep);
process.stdout.write(JSON.stringify(runs, null, 1));
