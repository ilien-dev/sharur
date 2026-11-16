// Prints each run's tool calls in order, with their description or command, and its text replies.
// usage: node tools.ts <run id> ...
import fs from 'node:fs';
import path from 'node:path';
import { events } from './types.ts';

for (const id of process.argv.slice(2)) {
  const s: string[] = [];
  for (const j of events(fs.readFileSync(path.join(import.meta.dirname, 'out', id + '.jsonl'), 'utf8')))
    if (j.type === 'assistant') for (const c of j.message.content) {
      if (c.type === 'tool_use') s.push(c.name + (c.input.description ? `("${c.input.description}")` : c.input.command ? `<${c.input.command.slice(0, 40)}>` : ''));
      if (c.type === 'text') s.push('TEXT:' + c.text.trim());
    }
  console.log(`=== ${id}\n${s.join('\n')}\n`);
}
