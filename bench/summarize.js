// Prints the README tables from results/runs.json.
// usage: node bench/summarize.js [results/runs.json]
const fs = require('fs'), path = require('path');
const runs = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, '..', 'results', 'runs.json')));
const QA = [1, 5, 6];
const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : NaN;
function table(title, rows, prompts) {
  const by = {};
  for (const r of rows) if (prompts.includes(r.prompt)) (by[r.style] ??= []).push(r);
  console.log(`\n${title}`);
  console.log('| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |');
  console.log('|---|---|---|---|---|---|---|---|---|---|');
  for (const [k, a] of Object.entries(by).sort((x, y) => mean(y[1].map(r => r.output_tokens)) - mean(x[1].map(r => r.output_tokens)))) {
    const g = a.filter(r => r.grade), crit = g.flatMap(r => r.grade.criteria), t = a.filter(r => r.task_ok !== null);
    const pct = x => Number.isNaN(x) ? '-' : (100 * x).toFixed(0) + '%';
    console.log(`| ${k} | ${a.length} | ${mean(a.map(r => r.words)).toFixed(1)} | ${mean(a.map(r => r.output_tokens)).toFixed(0)} | ${mean(a.filter(r => QA.includes(r.prompt)).map(r => r.output_tokens)).toFixed(0)} | ${mean(a.map(r => r.tool_calls)).toFixed(2)} | ${mean(a.map(r => r.cost_usd)).toFixed(3)} | ${pct(mean(crit.map(Number)))} | ${pct(mean(g.map(r => +r.grade.clear)))} | ${t.length ? t.filter(r => r.task_ok).length + '/' + t.length : '-'} |`);
  }
}
const sel = (round, env) => runs.filter(r => r.round === round && r.env === env);
table('Round 1: claude-opus-5-5, clean environment, prompts 1-6', sel('1', 'clean'), [1, 2, 3, 4, 5, 6]);
table('Rounds 2-5: claude-fable-5-2, clean environment, prompts 1-6', sel('2', 'clean'), [1, 2, 3, 4, 5, 6]);
table('Rounds 3-5: claude-fable-5-2, clean environment, 9 prompts (styles run on all 9)', sel('2', 'clean').filter(r => !['cavC', 'cavD', 'cavE', 'cavF'].includes(r.style)), [1, 2, 3, 4, 5, 6, 9, 10, 11]);
table('Real environment (plugins, hooks, Spanish replies), claude-fable-5-2, prompts 1, 2, 6, 11', sel('2', 'full'), [1, 2, 6, 11]);
table('Same four prompts in the clean environment, for comparison', sel('2', 'clean').filter(r => ['Concise', 'T1'].includes(r.style)), [1, 2, 6, 11]);
console.log(`\nruns: ${runs.length}, total cost: $${runs.reduce((s, r) => s + r.cost_usd, 0).toFixed(2)}`);
