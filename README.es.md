<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="Sharur, un output style para Claude Code: hasta 48% menos tokens de salida que Concise. Fable 5.2 −48%, Sonnet 5.5 −35%, Haiku 5.5 −33%, Opus 5.5 −29%." width="100%">
  </picture>
</p>

<p align="center"><a href="README.md">English</a> · <b>Español</b></p>

<h1 align="center">Sharur: gasta menos tokens en Claude Code con un output style de una línea</h1>

<p align="center">
  <b>Un output style para Claude Code que responde en una o dos líneas, sin saludos ni relleno,<br>
  así lees menos y pagas menos en cada tarea. Una línea de texto en un archivo pequeño.</b>
</p>

<p align="center">
  <img alt="Output style para Claude Code" src="https://img.shields.io/badge/Claude%20Code-output%20style-0B7A70?style=flat-square&labelColor=0F1115">
  <a href="#qué-ahorras"><img alt="Opus 5.5: 23% menos costo por tarea que Concise" src="https://img.shields.io/badge/Opus%205.5-%E2%88%9223%25%20costo-0B7A70?style=flat-square&labelColor=0F1115"></a>
  <a href="BENCHMARKS.md"><img alt="Probado en Opus, Sonnet, Haiku y Fable" src="https://img.shields.io/badge/probado%20en-Opus%20%C2%B7%20Sonnet%20%C2%B7%20Haiku%20%C2%B7%20Fable-0F1115?style=flat-square"></a>
  <a href="LICENSE"><img alt="Licencia: MIT" src="https://img.shields.io/badge/licencia-MIT-0F1115?style=flat-square"></a>
</p>

<p align="center">
  <a href="#instalación"><b>Instalación</b></a> ·
  <a href="#qué-ahorras"><b>Qué ahorras</b></a> ·
  <a href="#antes-y-después"><b>Antes y después</b></a> ·
  <a href="#antes-de-cambiarte"><b>Antes de cambiarte</b></a> ·
  <a href="#en-qué-se-diferencia-de-caveman"><b>vs caveman</b></a> ·
  <a href="BENCHMARKS.md"><b>Benchmarks (en inglés)</b></a>
</p>

---

Úsalo para reducir el consumo de tokens y el costo de Claude Code, o si quieres un "caveman mode" escueto que aun así te da el error y la solución.

## Qué ahorras

Comparado con el estilo Concise que trae Claude Code, con los mismos 9 prompts de prueba:

| Modelo | Palabras que lees | Tokens de salida | Costo por tarea |
|---|---|---|---|
| Opus 5.5 | -76% | -29% | -23% |
| Sonnet 5.5 | -63% | -35% | -23% |
| Haiku 5.5 | -65% | -33% | -18% |
| Fable 5.2 | -77% | -48% | -28% |

Donde más se nota es en las preguntas simples. En las tres que no usan herramientas, como "¿qué diferencia hay entre git rebase y git merge?", Opus 5.5 usó 357 tokens de salida con Concise y 63 con Sharur.

Cómo se midió y cómo repetirlo está en [BENCHMARKS.md](BENCHMARKS.md), en inglés.

## El estilo completo

```
Caveman. <=2 lines, <=25 words unless asked more. Exact: code, errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

A ti no te dirá mucho, pero el modelo lo sigue. Como es tan corto, ocupa menos que las instrucciones de Concise, así que cada petición lleva 379 tokens de entrada menos.

## Antes y después

Mismo prompt, mismo modelo (Opus 5.5), mismo proyecto pequeño en Python: "Add a multiply function to calc.py with a test, and run the tests." El archivo de tests tiene un bug que el prompt no menciona. Las respuestas están en inglés, tal como las dio el modelo.

Concise, 96 palabras:

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

Sharur, 27 palabras:

> Added `multiply` and its test, but tests fail first on an old bug: `subtract` returns `a + b` (`calc.py:6`). So the multiply test never ran. Fix `subtract`?

## Instalación

Pega esto en Claude Code:

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

O hazlo a mano:

```bash
mkdir -p ~/.claude/output-styles
curl -fsSL https://raw.githubusercontent.com/ilien-dev/sharur/main/sharur.md -o ~/.claude/output-styles/sharur.md
```

Después elige Sharur en `/config`, en Output style, y abre una sesión nueva. En Windows, `~` es `%USERPROFILE%`. Para usarlo en un solo proyecto, pon el archivo en `.claude/output-styles/` dentro de ese proyecto. Para volver atrás, elige otro estilo en `/config` y borra el archivo.

## Antes de cambiarte

Es muy corto, y a veces demasiado. De vez en cuando una respuesta deja fuera un detalle, como qué archivos tocó un renombrado: en Opus 5.5 el evaluador encontró el 90% de los datos obligatorios en las respuestas de Sharur y el 98% en las de Concise. El formato también cambia de una respuesta a otra. Después de abrir un PR, una vez puede darte el enlace y otra solo el número del PR. Si prefieres respuestas más completas, quédate con Concise.

## En qué se diferencia de caveman

[caveman](https://github.com/JuliusBrussee/caveman) ataca el mismo problema con todo un kit: un instalador, varias skills y sus propios comandos. Sharur es la línea de arriba y nada más, así que no hay nada que actualizar ni nada que se ejecute en tu máquina.

Sharur es la maza del dios sumerio Ninurta. El nombre significa "el que aplasta a miles".

## Licencia

MIT
