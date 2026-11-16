<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="Sharur, an output style for Claude Code: up to 48% fewer output tokens than Concise. Fable 5.2 −48%, Sonnet 5.5 −35%, Haiku 5.5 −33%, Opus 5.5 −29%." width="100%">
  </picture>
</p>

<p align="center"><b>English</b> · <a href="README.es.md">Español</a></p>

<h1 align="center">Sharur: cut Claude Code token usage with a one-line output style</h1>

<p align="center">
  <b>An output style for Claude Code that answers in one or two lines, with no greeting or filler,<br>
  so you read less and pay less on every task. One line of text in one small file.</b>
</p>

<p align="center">
  <img alt="Claude Code output style" src="https://img.shields.io/badge/Claude%20Code-output%20style-0B7A70?style=flat-square&labelColor=0F1115">
  <a href="#what-you-save"><img alt="Opus 5.5: 23% lower cost per task than Concise" src="https://img.shields.io/badge/Opus%205.5-%E2%88%9223%25%20cost-0B7A70?style=flat-square&labelColor=0F1115"></a>
  <a href="BENCHMARKS.md"><img alt="Benchmarked on Opus, Sonnet, Haiku and Fable" src="https://img.shields.io/badge/benchmarked-Opus%20%C2%B7%20Sonnet%20%C2%B7%20Haiku%20%C2%B7%20Fable-0F1115?style=flat-square"></a>
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

Against the built-in Concise style, on the same 9 test prompts:

| Model | Words to read | Output tokens | Cost per task |
|---|---|---|---|
| Opus 5.5 | -76% | -29% | -23% |
| Sonnet 5.5 | -63% | -35% | -23% |
| Haiku 5.5 | -65% | -33% | -18% |
| Fable 5.2 | -77% | -48% | -28% |

The gap is widest on plain questions. On the three that need no tools, like "what is the difference between git rebase and merge", Opus 5.5 used 357 output tokens with Concise and 63 with Sharur.

How this was measured, and how to rerun it, is in [BENCHMARKS.md](BENCHMARKS.md).

## The whole style

```
Caveman. <=2 lines, <=25 words unless asked more. Exact: code, errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

It won't mean much to you, but the model follows it. Because it is so short, it is also smaller than the instructions Concise ships with, so every request carries 379 fewer input tokens.

## Before and after

Same prompt, same model (Opus 5.5), same small Python project: "Add a multiply function to calc.py with a test, and run the tests." The test file has a bug the prompt doesn't mention.

Concise, 96 words:

> I added `multiply` to `calc.py` with a test in `test_calc.py`, but the test run fails because of a bug that was already there in `subtract`:
>
> ```
> File "test_calc.py", line 4, in <module>
>     assert subtract(5, 3) == 2
> AssertionError
> ```
>
> `subtract` returns `a + b` instead of `a - b` (`calc.py:6`). The script stops at that first failed assertion, so the new `multiply` test never runs. I checked `multiply(4, 3) == 12` on its own and it passes.
>
> I didn't change `subtract` because you didn't ask me to. Want me to fix it and rerun the tests?

Sharur, 27 words:

> Added `multiply` and its test, but tests fail first on an old bug: `subtract` returns `a + b` (`calc.py:6`). So the multiply test never ran. Fix `subtract`?

## Install

Paste this into Claude Code:

```
Install the Sharur output style for Claude Code.

1. Create the file ~/.claude/output-styles/sharur.md (create the folder if it is missing) with exactly this content:

---
name: Sharur
description: Caveman replies of 1-2 lines, exact code and errors, as few tool calls as possible.
keep-coding-instructions: true
---

Caveman. <=2 lines, <=25 words unless asked more. Exact: code, errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.

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

It is very short, and sometimes too short. Now and then a reply leaves out a detail, such as which files a rename touched: on Opus 5.5 the grader found 90% of the required facts in Sharur's replies and 98% in Concise's. The format also changes from one reply to the next. After opening a PR it may give you the link one time and only the PR number the next. If you want fuller answers, stay on Concise.

## How it differs from caveman

[caveman](https://github.com/JuliusBrussee/caveman) goes after the same problem with a whole toolkit: an installer, several skills and its own commands. Sharur is the one line above and nothing else, so there is nothing to update and nothing that runs on your machine.

Sharur is the mace of the Sumerian god Ninurta. The name means "smasher of thousands".

## License

MIT
