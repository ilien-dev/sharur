<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="Sharur, an output style for Claude Code: against Concise on Opus 5.5, 21% lower cost on everyday coding tasks, 10% on large ones and 6% on a huge one, with the same hidden tests passed and the same facts kept." width="100%">
  </picture>
</p>

<p align="center"><b>English</b> · <a href="README.es.md">Español</a></p>

<h1 align="center">Sharur: cut Claude Code token usage with a one-paragraph output style</h1>

<p align="center">
  <b>An output style for Claude Code that answers in one or two lines, with no greeting or filler,<br>
  and one short line per item when the result is bigger. One short paragraph in one small file.</b>
</p>

<p align="center">
  <img alt="Claude Code output style" src="https://img.shields.io/badge/Claude%20Code-output%20style-0B7A70?style=flat-square&labelColor=0F1115">
  <a href="#what-you-save"><img alt="Opus 5.5: 21% lower cost than Concise on everyday tasks" src="https://img.shields.io/badge/Opus%205.5-%E2%88%9221%25%20cost%20on%20everyday%20tasks-0B7A70?style=flat-square&labelColor=0F1115"></a>
  <a href="BENCHMARKS.md"><img alt="Checked with hidden tests" src="https://img.shields.io/badge/checked%20with-hidden%20tests-0F1115?style=flat-square"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-0F1115?style=flat-square"></a>
</p>

<p align="center">
  <a href="#install"><b>Install</b></a> ·
  <a href="#what-you-save"><b>What you save</b></a> ·
  <a href="#before-and-after"><b>Before and after</b></a> ·
  <a href="#before-you-switch"><b>Before you switch</b></a> ·
  <a href="#how-it-differs-from-caveman"><b>vs caveman</b></a> ·
  <a href="BENCHMARKS.md"><b>Benchmarks</b></a>
</p>

---

Use it to reduce Claude Code token usage and cost, or when you want a terse "caveman mode" that still gives you the error and the fix.

## What you save

On everyday coding work Sharur costs 21% less than the built-in Concise style. That is the median of four medium tasks on Claude Opus 5.5: fixing failing tests, adding a CLI flag, reviewing three modules for bugs and tracing how an order total is computed (between 4% and 26% per task). Bigger jobs save less, and every result is in the table:

| Task | Tasks | Cost | Output tokens | Words to read |
|---|---|---|---|---|
| Short questions and small fixes | 4 | -37% | -35% | -61% |
| Long answers: an explanation, an audit | 2 | -21% | -23% | -38% |
| **Medium coding tasks** | **4** | **-21%** | **-35%** | **-54%** |
| Large features: returns, a move to integer cents | 2 | -10% | -13% | -47% |
| A huge task: an 11-item spec | 1 | -6% | 0% | -28% |
| Medium, large and huge, each size weighted equally | 7 | -12% | -16% | -43% |

Each task ran 3 times with each style, and each number is the median of the per-task changes. Cost is what the CLI reports, so it includes the style's own text, which is read on every request. Sharur was cheaper on all 13 tasks. Hidden tests checked the files every run left behind, and all of them passed with both styles. A grader found the same required facts in both styles' replies on the medium to huge tasks.

Questions save the most, but few sessions are mostly questions, so 37% is not the number to expect. The bigger the task, the smaller the saving: a long session spends most of its tokens on code, tool calls and the context read again on every turn, and an output style changes none of that. [JetBrains found the same](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/) for the caveman skill: 65% advertised, 8.5% on real agent tasks.

How this was measured, and how to rerun it, is in [BENCHMARKS.md](BENCHMARKS.md).

## The whole style

```
Telegraphic: drop filler, keep grammar. <=2 lines, <=25 words. Bigger result: one short line per item, every item asked, no recap. No text before work is done. Say what was wrong, not a label for it. Exact: errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

It is also smaller than the instructions Concise ships with, so every request carries about 330 fewer input tokens.

## Before and after

Same prompt, same model (Opus 5.5), same small Python project: "Add a multiply function to calc.py with a test, and run the tests." The test file has a bug the prompt doesn't mention.

Concise, 89 words, 1,619 output tokens:

> I added `multiply` and its test, but the test run fails because of a bug that was already in `subtract`.
>
> ```
>   File "test_calc.py", line 4, in <module>
>     assert subtract(5, 3) == 2
> AssertionError
> ```
>
> `subtract` returns `a + b` instead of `a - b` (`calc.py:6`). The test file stops at the first failed check, so the new `multiply` check never ran there. I ran it separately and it passes.
>
> I didn't change `subtract` because you didn't ask me to. It's a one-character fix — want me to make it?

Sharur, 37 words, 1,012 output tokens:

> Added `multiply` to `calc.py` and a test, but the tests fail first at `assert subtract(5, 3) == 2`, so the multiply test never ran. `subtract` returns `a + b`; should I change it to `a - b`?

On a bigger result it writes one line per item. Sharur after "The tests fail. Find the causes and fix them." on a 9-file project:

> All 19 tests pass now. The three causes:
> - `shop/inventory.py`: `reserve` refused an order for the last units because it checked `>=` instead of `>`.
> - `shop/pricing.py` `bulk_discount`: the 10-unit check ran first, so 50+ units got 5% instead of 10%.
> - `shop/pricing.py` `order_totals`: tax was charged before the coupon was taken off; it's now charged after.

## Install

Paste this into Claude Code:

```
Install the Sharur output style for Claude Code.

1. Create the file ~/.claude/output-styles/sharur.md (create the folder if it is missing) with exactly this content:

---
name: Sharur
description: Telegraphic replies of 1-2 lines, one short line per item on bigger results, exact errors, as few tool calls as possible.
keep-coding-instructions: true
---

Telegraphic: drop filler, keep grammar. <=2 lines, <=25 words. Bigger result: one short line per item, every item asked, no recap. No text before work is done. Say what was wrong, not a label for it. Exact: errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.

2. In ~/.claude/settings.json set "outputStyle" to "Sharur". Keep every other key as it is. Create the file if it does not exist.

3. Tell me to start a new session, because the output style is read when a session starts.
```

Or do it by hand:

```bash
mkdir -p ~/.claude/output-styles
curl -fsSL https://raw.githubusercontent.com/ilien-dev/sharur/main/sharur.md -o ~/.claude/output-styles/sharur.md
```

Then pick Sharur in `/config` under Output style and start a new session. On Windows, `~` is `%USERPROFILE%`. To use it in one project only, put the file in `.claude/output-styles/` inside that project. To go back, pick another style in `/config` and delete the file.

## Before you switch

- On big tasks the saving is small: 6 to 10% of the cost in these tests. The larger numbers come from questions and short tasks.
- This version of the style was measured on Opus 5.5 only, 3 runs per task. The earlier one-line version was also tested on Sonnet 5.5, Haiku 5.5 and Fable 5.2; this one has not been. Fable 5.2 runs made while tuning it looked similar, but those runs were used to choose the text, so they prove nothing.
- "Fewest tool calls" changes how the model works, not only how it talks. It never cost a hidden test here, but it is the first part to delete if you see the model skip a step it should have taken.
- The reports are written for someone who knows the task. If you need a full write-up of a change, ask for one or stay on Concise.

## Why there are no hooks

Claude Code hooks can't rewrite a reply. A Stop hook can only block it and send the model back for another turn, which reads the whole context again. A PreToolUse hook can shorten a tool call's input, but only after the model has written, and been billed for, those tokens. In these runs the reply text was 10% of what the model wrote on medium to huge tasks, and tool `description` fields were under 1%, so a hook has little to save and the extra turn costs more than that. A proxy that compresses tool output, rtk, [raised the median cost by 7.6%](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/) in JetBrains' tests. Sharur stays a text file.

## How it differs from caveman

[caveman](https://github.com/JuliusBrussee/caveman) goes after the same problem with a whole toolkit: an installer, several skills and its own commands. Sharur is the text above and nothing else, so there is nothing to update and nothing that runs on your machine.

Sharur is the mace of the Sumerian god Ninurta. The name means "smasher of thousands".

## License

MIT
