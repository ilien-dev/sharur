// Runs the hidden tests of a prompt against the files each run left behind.
// usage: node verify.ts  -> writes out/<id>.verify.json {passed, total} for every run of a prompt with verify/p<N>/
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const here = import.meta.dirname;
const out = path.join(here, 'out');
for (const f of fs.readdirSync(out).filter(f => f.endsWith('.jsonl'))) {
  const m = f.match(/^(.+)_p(\d+)_r(\d+)\.jsonl$/); if (!m) continue;
  const src = path.join(here, 'verify', `p${m[2]}`), run = path.join(here, 'runs', f.replace('.jsonl', ''));
  const target = path.join(out, f.replace('.jsonl', '.verify.json'));
  if (!fs.existsSync(src) || !fs.existsSync(run) || (fs.existsSync(target) && !process.argv.includes('--force'))) continue;
  const v = path.join(run, '_v'); fs.rmSync(v, { recursive: true, force: true });
  fs.cpSync(src, v, { recursive: true });
  if (!fs.existsSync(path.join(v, 'conftest.py'))) fs.copyFileSync(path.join(here, 'verify', 'common', 'conftest.py'), path.join(v, 'conftest.py'));
  const total = fs.readdirSync(v).filter(n => n.startsWith('test_'))
    .reduce((n, t) => n + (fs.readFileSync(path.join(v, t), 'utf8').match(/^def test_/gm) || []).length, 0);
  const r = spawnSync('python', ['-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--tb=no', '_v'], { cwd: run, encoding: 'utf8' });
  const passed = +((r.stdout || '').match(/(\d+) passed/)?.[1] ?? 0);
  fs.rmSync(v, { recursive: true, force: true });
  fs.writeFileSync(target, JSON.stringify({ passed, total }));
}
