// Prints the confirmation-round tables in BENCHMARKS.md from results/runs-v2.json.
// usage: node bench/summarize-v2.cjs [results/runs-v2.json] [arm=Sharur]
// Per task: median over reps of cost, output tokens and words; mean of hidden-test score and of
// facts (each criterion by majority of three Sonnet grades). Groups: median of the per-task changes.
const fs = require('fs');
const path = require('path');
const runs = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, '..', 'results', 'runs-v2.json'), 'utf8'));
const arm = process.argv[3] || 'Sharur', base = 'Concise';
const SIZE = p => p <= 11 ? 'short' : p <= 13 ? 'long' : p <= 17 ? 'medium' : p <= 19 ? 'large' : 'huge';
const med = a => { a = [...a].sort((x, y) => x - y); const n = a.length; return n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2 };
const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : NaN;
const words = r => r.reply.split(/\s+/).filter(Boolean).length;
const facts = r => { const g = r.grades_sonnet; if (!g.length) return null; const n = g[0].criteria.length; let ok = 0; for (let i = 0; i < n; i++) if (g.filter(x => x.criteria[i]).length * 2 > g.length) ok++; return ok / n };
const score = r => r.hidden_tests ? r.hidden_tests.passed / r.hidden_tests.total : null;
const sign = (k, n) => { let c = 1, s = 0; const t = []; for (let i = 0; i <= n; i++) { t.push(c); c = c * (n - i) / (i + 1) } for (let i = 0; i <= Math.min(k, n - k); i++) s += t[i]; return Math.min(1, 2 * s / 2 ** n) };
const pick = (st, p) => runs.filter(r => r.style === st && r.prompt === p);
const prompts = [...new Set(runs.map(r => r.prompt))].sort((a, b) => a - b);
const pct = (a, b) => 100 * (a / b - 1);
const rows = prompts.map(p => {
  const B = pick(base, p), S = pick(arm, p);
  const m = (a, f) => med(a.map(f)), avg = (a, f) => mean(a.map(f).filter(x => x !== null));
  return { p, size: SIZE(p), cost: [m(B, r => r.cost_usd), m(S, r => r.cost_usd)], out: [m(B, r => r.output_tokens), m(S, r => r.output_tokens)],
    words: [m(B, words), m(S, words)], tests: [avg(B, score), avg(S, score)], facts: [avg(B, facts), avg(S, facts)] };
});
const f = x => isNaN(x) ? '-' : (100 * x).toFixed(0) + '%';
console.log(`| task | size | cost ${base} → ${arm} | output tokens | words | hidden tests | facts |`);
console.log('|---|---|---|---|---|---|---|');
for (const r of rows) console.log(`| p${r.p} | ${r.size} | ${r.cost[0].toFixed(3)} → ${r.cost[1].toFixed(3)} (${pct(r.cost[1], r.cost[0]).toFixed(0)}%) | ${r.out[0]} → ${r.out[1]} (${pct(r.out[1], r.out[0]).toFixed(0)}%) | ${r.words[0]} → ${r.words[1]} | ${f(r.tests[0])} → ${f(r.tests[1])} | ${f(r.facts[0])} → ${f(r.facts[1])} |`);
console.log('\n| group | tasks | cost | output tokens | words | cheaper on | sign test p | hidden tests | facts |');
console.log('|---|---|---|---|---|---|---|---|---|');
const groups = [['short', ['short']], ['long', ['long']], ['medium', ['medium']], ['large', ['large']], ['huge', ['huge']], ['medium + large + huge', ['medium', 'large', 'huge']], ['all', ['short', 'long', 'medium', 'large', 'huge']]];
for (const [name, sizes] of groups) {
  if (name === 'all') {
    // Headline: medium, large and huge with each size weighted equally, so 4 medium tasks do not outvote 3 bigger ones.
    const sz = ['medium', 'large', 'huge'], g = k => mean(sz.map(z => med(rows.filter(r => r.size === z).map(r => pct(r[k][1], r[k][0]))))).toFixed(1) + '%';
    console.log(`| medium + large + huge, each size weighted equally | 7 | ${g('cost')} | ${g('out')} | ${g('words')} | | | | |`);
  }
  const a = rows.filter(r => sizes.includes(r.size)); if (!a.length) continue;
  const d = k => med(a.map(r => pct(r[k][1], r[k][0]))).toFixed(1) + '%';
  const q = k => { const v = a.filter(r => !isNaN(r[k][0])); return v.length ? f(mean(v.map(r => r[k][0]))) + ' → ' + f(mean(v.map(r => r[k][1]))) : '-' };
  const neg = a.filter(r => r.cost[1] < r.cost[0]).length;
  console.log(`| ${name} | ${a.length} | ${d('cost')} | ${d('out')} | ${d('words')} | ${neg}/${a.length} | ${sign(neg, a.length).toFixed(3)} | ${q('tests')} | ${q('facts')} |`);
}
