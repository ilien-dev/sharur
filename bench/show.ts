// Prints the reply text of runs, tool calls as [name].
// usage: node show.ts <run id> ...
import fs from 'node:fs';
import path from 'node:path';
import { events } from './types.ts';

const dir = path.join(import.meta.dirname, 'out');
for (const id of process.argv.slice(2)) {
  let text = '';
  for (const j of events(fs.readFileSync(path.join(dir, id + '.jsonl'), 'utf8')))
    if (j.type === 'assistant') for (const c of j.message.content) { if (c.type === 'text') text += c.text + '\n'; if (c.type === 'tool_use') text += `[${c.name}]\n` }
  console.log(`=== ${id}\n${text.trim()}\n`);
}
