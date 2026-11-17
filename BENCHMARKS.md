# Sharur benchmarks

How Sharur was measured, every result, and how to run the benchmark yourself. The short version is in the [README](README.md).

This file covers two versions of the style. The current one (v2) is measured first. The one-line version it replaced (v1) is kept at the end, together with why it was replaced.

## Current style

```
Telegraphic: drop filler, keep grammar. <=2 lines, <=25 words. Bigger result: one short line per item, every item asked, no recap. No text before work is done. Say what was wrong, not a label for it. Exact: errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

## Results

Claude Opus 5.5, Claude Code 2.1.326, no plugins or hooks. 13 tasks, 3 runs per task and style, 117 runs in all, USD 25 spent. For each task the per-run numbers were reduced to a median, and Sharur was compared with Concise on the same task. `node bench/summarize-v2.cjs` prints these tables from `results/runs-v2.json`.

| group | tasks | cost | output tokens | words | Sharur cheaper on | sign test p | hidden tests | facts |
|---|---|---|---|---|---|---|---|---|
| short questions and small fixes | 4 | -37.1% | -34.8% | -60.9% | 4/4 | 0.125 | - | 100% → 100% |
| long answers | 2 | -20.7% | -23.0% | -37.9% | 2/2 | 0.500 | - | 100% → 97% |
| **medium coding tasks** | **4** | **-21.4%** | **-34.6%** | **-53.7%** | **4/4** | **0.125** | **100% → 100%** | **100% → 100%** |
| large features | 2 | -9.8% | -12.9% | -46.5% | 2/2 | 0.500 | 100% → 100% | 100% → 100% |
| huge spec | 1 | -6.0% | -0.2% | -28.3% | 1/1 | 1.000 | 100% → 100% | 100% → 100% |
| medium + large + huge, median of the 7 tasks | 7 | -14.5% | -29.4% | -48.1% | 7/7 | 0.016 | 100% → 100% | 100% → 100% |
| medium + large + huge, each size weighted equally | 7 | -12.4% | -15.9% | -42.8% | | | | |
| all | 13 | -20.2% | -29.4% | -52.3% | 13/13 | <0.001 | 100% → 100% | 99.6% → 100%, rounded |

The README leads with the medium row, -21%, because tasks of that size are most of a working day: fix the failing tests, add a flag, review a module, trace a bug. It shows every other row next to it. Large and huge tasks still came out cheaper, by 10% and 6%. Weighting medium, large and huge equally gives -12%; that row keeps the four medium tasks from outvoting the three bigger ones, where a plain median of the 7 lands at -14.5%. Questions save the most and are the least representative of agent work, so they are shown and not used as a headline. The large and huge rows show where it is heading: the bigger the task, the closer the saving gets to the single digits JetBrains measured.

Per task:

| task | size | cost Concise → Sharur | output tokens | words | hidden tests | facts |
|---|---|---|---|---|---|---|
| p1 | short | 0.080 → 0.038 (-53%) | 359 → 189 (-47%) | 175 → 69 | - | 100% → 100% |
| p4 | short | 0.135 → 0.103 (-23%) | 1117 → 1012 (-9%) | 89 → 36 | - | 100% → 100% |
| p7 | short | 0.117 → 0.058 (-51%) | 2998 → 1177 (-61%) | 1143 → 443 | - | 100% → 100% |
| p11 | short | 0.119 → 0.102 (-15%) | 1203 → 936 (-22%) | 105 → 34 | - | 100% → 100% |
| p12 | long | 0.146 → 0.126 (-14%) | 1806 → 1697 (-6%) | 116 → 78 | - | 100% → 94% |
| p13 | long | 0.118 → 0.086 (-28%) | 1636 → 981 (-40%) | 435 → 248 | - | 100% → 100% |
| p14 | medium | 0.149 → 0.115 (-23%) | 1132 → 799 (-29%) | 129 → 57 | 100% → 100% | 100% → 100% |
| p15 | medium | 0.181 → 0.173 (-4%) | 2349 → 1606 (-32%) | 151 → 72 | 100% → 100% | 100% → 100% |
| p16 | medium | 0.130 → 0.097 (-26%) | 1563 → 977 (-37%) | 265 → 119 | - | 100% → 100% |
| p17 | medium | 0.143 → 0.114 (-20%) | 1753 → 1062 (-39%) | 380 → 203 | - | 100% → 100% |
| p18 | large | 0.465 → 0.441 (-5%) | 9160 → 8004 (-13%) | 308 → 170 | 100% → 100% | 100% → 100% |
| p19 | large | 0.808 → 0.691 (-14%) | 17251 → 14992 (-13%) | 484 → 251 | 100% → 100% | 100% → 100% |
| p20 | huge | 0.577 → 0.542 (-6%) | 13211 → 13187 (0%) | 315 → 226 | 100% → 100% | 100% → 100% |

Cost is the `total_cost_usd` the CLI reports. It already includes the input side: the style's own text, read on every request, and the whole context read again on every turn. A saving in this column is a saving on the bill, not on one slice of it.

The style text is smaller than Concise's. On a question with no tools, the first request carried 24,581 input tokens with Sharur and 24,912 with Concise, 331 fewer (measured on Fable 5.2; the text is the same on every model).

## The tasks

Prompts 1 to 13 run in `bench/fixture`, three short Python files. Prompts 14 to 20 run in `bench/fixture2`, a 9-file order-book package with a CLI, a JSON data file and 19 pytest tests, three of which fail on planted bugs. The prompts are in `bench/prompts.txt`.

| task | prompt, shortened |
|---|---|
| p1 | What's the difference between git rebase and git merge? |
| p4 | Add a multiply function with a test, and run the tests. |
| p7 | Explain in detail how Python's GIL works and why it exists. |
| p11 | Rename `average` to `mean` everywhere. |
| p12 | Six changes at once: fix two files, add two functions, rename, convert the tests to pytest. |
| p13 | Audit all three files without changing anything, with a fix for each problem. |
| p14 | The tests fail. Find the causes and fix them. |
| p15 | Add a `--json` flag to `report`, with a test. |
| p16 | Review three modules for bugs without changing anything. |
| p17 | Trace how an order total with a coupon is computed. |
| p18 | Add product returns: a method, refunds in the totals and reports, a CLI command, storage with backward compatibility, tests, README. |
| p19 | Move all money from floats to integer cents without changing the CLI output. |
| p20 | Do the 11 items in `SPEC.md`: three bug fixes, seven features and the tests and README for them. |

## How quality was checked

- **Hidden tests.** p14, p15 and p18 to p20 have tests the model never sees, in `bench/verify/`. `node bench/verify.ts` copies them into the directory each run left behind and runs pytest. Every run of both styles passed every hidden test.
- **Facts.** `bench/rubrics.json` lists two to six facts a useful reply must contain, such as "states the test run outcome". Claude Sonnet 5.5 graded each reply three times with no knowledge of the style, and each fact counts as present when at least two of the three grades say so.
- **Clarity.** The same grader answered whether a developer could understand the reply without guessing at garbled words or shorthand. Concise and Sharur were both graded clear on 100% of the medium to huge runs.

The grader was changed during this work. Haiku 5.5 graded the earlier rounds, and on reading its misses most were wrong: it marked "the 10-unit check ran first, so 50+ units got only 5%" as not naming the bulk discount bug, and a list of three named failing tests as not specific. With Haiku, Sharur appeared to lose about 5 points of facts; with Sonnet it lost none, while the same Sonnet grader still took 11 points off the v1-like candidate `L3`, so it is not simply lenient. All numbers in this section use Sonnet. Two rubric lines that Haiku read too literally were reworded before the Sonnet grading and apply to both styles in the same way.

## What was learned from JetBrains

JetBrains tested [caveman](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/) (65% advertised, 8.5% measured) and [rtk](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/) (60 to 90% advertised, cost up 7.6%) on 86 real agent tasks. Their method, scaled down, is what this round follows:

- **Tasks with real work in them.** Most output tokens in an agent session are code and tool calls, which an output style leaves alone. A benchmark made of questions measures chat, not agent work. So 7 of the 13 tasks here edit a multi-file project, and the headline leaves the questions out.
- **Paired comparison per task, medians, no arm totals.** Two runs of the same task can differ by 40%: on Fable 5.2, Concise cost USD 0.97 on p19 in one run and 1.37 in the next. Totals let one outlier decide the result.
- **Never trust k=1.** Their first 10-task run showed -30% and shrank to -8.5% at scale. Here every number has 3 runs per task, and the tuning rounds are not the reported ones (see below).
- **Measure the bill, not the tool's own count.** Cost includes the style's input tokens and every cached re-read.
- **Check the work, not just the words.** Hidden tests decide whether a shorter style made the model sloppier.

Their caveman result also sets the expectation: an output style can only compress the text between tool calls, and on large tasks that text is a small part of what the model writes. Here it was 10% of the visible output on the medium to huge tasks (16% with Concise).

## How the text was chosen

The v1 style ended its length limit with "unless asked more". On long answers the model read that as permission to drop the limit and the terse register with it: on Fable 5.2 the GIL explanation (p7) came out at 448 words, against 651 for Concise. On a six-step task (p12) the opposite happened: it kept to 25 words and dropped half the facts.

Candidates were tuned on Fable 5.2, 2 runs per task, on the long and project tasks. Each line of the final text answers a failure seen in those rounds:

| candidate | change | what it showed |
|---|---|---|
| L1 | "past that only if needed, and still caveman" | Long answers shorter, but the six-step task still lost facts. |
| L3 | "Bigger result: one fragment per item, every item asked, no recap" | Fixed the six-step task. On project tasks the grader flagged invented labels ("last-unit reserve") and notes left over from the middle of the work. |
| S1 | L3 + "No text before work is done. Name things in full." | Fewer stray notes; the labels remained. |
| S2 | "Telegraphic: drop filler, keep grammar" + "Say what was wrong, not a label for it" | Clarity fixed. Chosen. |
| S3, S4 | "After a task: result, tests, deviations only" | Cut facts on the six-step task. Dropped. |

The confirmation round then ran only Concise, L3 and S2, on Opus 5.5 (Fable 5.2 had hit its usage limit), with 3 runs per task and a model none of the candidates had been tuned on. The tasks were not all new: p7 and p12 to p18 were also used while tuning on Fable 5.2. For S2, only the model and the two biggest tasks, p19 and p20, are fully held out. L3, which uses fewer words, saved almost nothing on the medium to huge tasks (-2.3% cost) and lost 11 points of facts; S2 is the result above.

The Fable 5.2 tuning runs agree in direction (S2 against Concise: -30% cost on 5 medium and large tasks, the same facts), but they were used to pick the text, so they are biased in its favour and are not reported as results.

## Hooks and scripts

An output style is a Markdown file. Its frontmatter takes `name`, `description`, `keep-coding-instructions` and, in plugins, `force-for-plugin`; it cannot run scripts or ship hooks. A plugin could bundle the style with hooks, so the ceiling of each hook was worked out from these runs before testing any:

- **Stop hook.** It can block the reply and send the model back for another turn, but it cannot rewrite the text the user sees. Each extra turn reads the whole context again. That is a cost added to every task to remove at most part of the 10% of output that is reply text.
- **PreToolUse hook with `updatedInput`.** It can shorten a tool call's `description`, but only after the model has generated it, so the output tokens are already billed. Descriptions were 0.7% of the visible output.
- **UserPromptSubmit `additionalContext`.** It adds input tokens to every prompt. Claude Code already repeats a reminder of the active output style on its own.
- **Compressing tool output in PostToolUse.** This is what rtk does, and JetBrains measured it at +7.6% cost.

None of these could beat the run-to-run noise, which is 20 to 40% of a task's cost, so none was run, and Sharur stays a text file.

## Limits

- One model in the confirmation round. Opus 5.5 is the only model measured with this text at 3 runs per task. Sonnet 5.5 and Haiku 5.5 were measured only with v1.
- Partly reused tasks. 8 of the 13 tasks were also used to tune the text on Fable 5.2; only p19 and p20 are new to it on both counts.
- 13 tasks. JetBrains used 86. A sign test over 7 tasks reaches p = 0.016 only because Sharur was cheaper on all of them; the size of the saving per group rests on 1 to 4 tasks.
- One huge task. Its -6% is a single task with 3 runs per style.
- The test projects are small. Nothing here shows how the style behaves in a large codebase, where tool output and code would take an even larger share of the bill.
- The grader is a language model. Haiku and Sonnet disagreed by about 5 points of facts on the same replies.
- "Destructive confirms" was not exercised; the headless permission mode allows the edits.
- The word count includes every text block of a run, not just the final reply.

## Run it yourself

You need Claude Code, Node 22.18 or newer (it runs the TypeScript scripts directly, no build step), Python with pytest, and bash. A run of the confirmation round costs about USD 25 at Opus 5.5 prices.

```bash
cd bench
MODEL=claude-opus-5-5 PFX=O_ PROMPTS="1 4 7 11 12 13 14 15 16 17 18 19 20" bash matrix.sh 3 Concise S2
node verify.ts                       # hidden tests against each run's files
GRADER=sonnet ONLY=O_ node grade.ts  # three grades per reply
GTAG=grade-sonnet node analyze.cjs O_ Concise S2
```

`one.sh` copies `fixture/` for prompts 1 to 13 and `fixture2/` for 14 and up, adds `tasks/p<N>/` (the `SPEC.md` of p20), and drops a run whose result is an error or a usage-limit message so it is never graded. `mkstyle.sh NAME "text"` adds a candidate to `fixture/.claude/output-styles/`. Raw session logs go to `bench/out/` and are not published, because their first event lists the plugins and paths of the machine that ran them; `results/runs-v2.json` keeps the reply text, token counts, tool names, hidden-test scores and grades.

---

## v1: the one-line style

The rest of this file is the benchmark of the previous version. Its numbers come from 9 prompts on the three-file project, mostly questions and short tasks, which is why they are larger than the numbers above.

```
Caveman. <=2 lines, <=25 words unless asked more. Exact: code, errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

### One reply, side by side

Same prompt, same model (Claude Fable 5.2), same test project: "Add a multiply function to calc.py with a test, and run the tests." The test file has a bug the prompt does not mention.

Concise (101 words, 1,517 output tokens, 6 tool calls):

> `multiply` is added and its assertions pass, but the test file as a whole fails on an existing bug in `subtract`, which I left alone:
>
> ```
> File "...\test_calc.py", line 4, in <module>
>     assert subtract(5, 3) == 2
> AssertionError
> ```
>
> `subtract` at `calc.py:6` returns `a + b` instead of `a - b`. Because the test file is a plain script that stops at the first failed assertion, the new `multiply` assertions never run there; I checked them separately and they pass.
>
> Changing line 6 to `a - b` should make the whole file pass — say the word and I'll apply it.

v1 (27 words, 675 output tokens, 4 tool calls):

> Multiply added, its test pass. Suite fail on old bug: `assert subtract(5, 3) == 2` → `AssertionError`; `subtract` returns `a + b`. Not fixed — want fix?

### Results

All numbers below are means per run, taken from `results/runs.json`. `node bench/summarize.ts` prints every table in this section from that data. Facts and clarity here were graded by Haiku, once per reply.

Claude Fable 5.2, 9 prompts, no plugins or hooks:

| | Concise (18 runs) | v1 (36 runs) | change |
|---|---|---|---|
| Words per reply | 87.7 | 20.1 | -77% |
| Output tokens per task | 645 | 338 | -48% |
| Output tokens per question (no tools) | 248 | 62 | -75% |
| Tool calls per task | 2.94 | 1.83 | -38% |
| Cost per task (USD) | 0.161 | 0.116 | -28% |
| Required facts present in the reply | 98% | 100% | |
| Replies graded clear | 100% | 97% | |
| Tasks done correctly | 6/6 | 12/12 | |

The same 9 prompts, 2 runs per prompt and style, on Claude Code 2.1.325. Change against Concise:

| | Fable 5.2 | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|---|
| Words per reply | -77% | -76% | -63% | -65% |
| Output tokens per task | -48% | -29% | -35% | -33% |
| Output tokens per question (no tools) | -75% | -82% | -70% | -57% |
| Tool calls per task | -38% | +2% | -32% | -18% |
| Cost per task | -28% | -23% | -23% | -18% |
| Required facts present (Concise → v1) | 98% → 100% | 98% → 90% | 100% → 96% | 98% → 92% |
| Tasks done correctly (Concise, v1) | 6/6, 12/12 | 6/6, 6/6 | 6/6, 6/6 | 6/6, 6/6 |

v1 came out of five rounds with 16 candidate texts, 344 runs in all. The 16 texts are in `bench/fixture/.claude/output-styles/`, next to `canary.md`, a one-line style used to check that custom styles load in headless mode. v1 is `T1`.

### Where the ceiling was

A reply shorter than about 25 words started to lose facts. These candidates differ from v1 only in the limit (18 runs each, same 9 prompts):

| candidate | limit | words per reply | required facts present | graded clear |
|---|---|---|---|---|
| cavG | 2 lines, 25 words | 22.5 | 96% | 100% |
| H2 | 12 words | 20.4 | 94% | 94% |
| H1 | 1 line, 15 words | 14.3 | 84% | 94% |
| H3 | 8 words | 16.6 | 92% | 100% |
| H4 | 15 words, symbols and abbreviations | 23.2 | 100% | 78% |

Softer wording did little. In the first round, on Claude Opus 5.5, a style that said "Terse. No preamble, recap, filler, hedging, pleasantries" with no number averaged 107.5 words per reply against 111.8 for Concise. Adding "<=2 lines" brought that to 30.8.

Most output tokens in a coding task are tool calls, so a limit on reply text stops paying off early. `cavG` is v1 without its last two sentences, and it used 459 output tokens per task. "Fewest tool calls" brought that down to 344 (`T5b`). The limit on tool description fields did nothing by itself (473, `T5a`), and with both the result was 338.

### Why v1 was replaced

Its 9 prompts were mostly questions and short tasks, where an output style saves the most. On the larger tasks added for v2, v1 kept its replies short but lost facts on reports of multi-step work, and "unless asked more" switched the limit off on long answers instead of scaling it. Its -28% on Fable 5.2 also came from the same runs that chose it, the selection bias the v2 confirmation round avoids.
