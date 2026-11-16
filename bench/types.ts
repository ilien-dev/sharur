// Shapes of the `claude -p --output-format stream-json` events the scripts read, and of results/runs.json.

export type Content =
  | { type: 'text'; text: string }
  | { type: 'tool_use'; name: string; input: { description?: string; command?: string } };

export interface AssistantEvent { type: 'assistant'; message: { content: Content[] } }

export interface ResultEvent {
  type: 'result';
  usage: { output_tokens: number; input_tokens: number; cache_creation_input_tokens: number; cache_read_input_tokens: number };
  total_cost_usd: number;
  is_error?: boolean;
  modelUsage?: Record<string, unknown>;
}

export type StreamEvent = AssistantEvent | ResultEvent | { type: 'system' | 'user' | 'rate_limit_event' };

export interface Grade { criteria: boolean[]; clear: boolean }

export interface Run {
  round: string | null;
  env: 'full' | 'clean';
  model: string | null;
  style: string;
  prompt: number;
  rep: number;
  words: number;
  chars: number;
  output_tokens: number;
  input_tokens: number;
  tool_calls: number;
  tools: string[];
  cost_usd: number;
  is_error: boolean;
  grade: Grade | null;
  task_ok: boolean | null;
  reply: string;
}

// Parses one stream-json log, skipping blank and malformed lines.
export function* events(text: string): Generator<StreamEvent> {
  for (const l of text.split('\n')) {
    if (!l.trim()) continue;
    try { yield JSON.parse(l) as StreamEvent } catch { continue }
  }
}
