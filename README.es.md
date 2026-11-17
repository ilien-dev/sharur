<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" alt="Sharur, un output style para Claude Code. Comparado con Concise en Opus 5.5, las tareas de programación de cada día cuestan 21% menos y sus respuestas tienen 54% menos palabras que leer; las tareas grandes cuestan 10% menos y una enorme 6% menos, con los mismos tests ocultos aprobados." width="100%">
  </picture>
</p>

<p align="center"><a href="README.md">English</a> · <b>Español</b></p>

<h1 align="center">Sharur: gasta menos tokens en Claude Code con un output style de un párrafo</h1>

<p align="center">
  <b>Un output style para Claude Code que responde en una o dos líneas, sin saludos ni relleno,<br>
  y una línea corta por punto cuando el resultado es más grande. Un párrafo corto en un archivo pequeño.</b>
</p>

<p align="center">
  <a href="#qué-ahorras"><img alt="Tareas de cada día: 21% menos costo que Concise" src="https://img.shields.io/badge/tareas%20diarias-%E2%88%9221%25%20costo-0B7A70?style=flat-square&labelColor=0F1115"></a>
  <a href="#qué-ahorras"><img alt="Tareas de cada día: 54% menos palabras que leer que con Concise" src="https://img.shields.io/badge/palabras%20que%20leer-%E2%88%9254%25-1F6FEB?style=flat-square&labelColor=0F1115"></a>
  <a href="BENCHMARKS.md"><img alt="Tests ocultos: todos aprobados" src="https://img.shields.io/badge/tests%20ocultos-todos%20aprobados-2DA44E?style=flat-square&labelColor=0F1115"></a>
  <img alt="Output style para Claude Code" src="https://img.shields.io/badge/Claude%20Code-output%20style-8250DF?style=flat-square&labelColor=0F1115">
  <a href="LICENSE"><img alt="Licencia: MIT" src="https://img.shields.io/badge/licencia-MIT-0F1115?style=flat-square"></a>
</p>

<p align="center">
  <a href="#instalación"><b>Instalación</b></a> ·
  <a href="#qué-ahorras"><b>Qué ahorras</b></a> ·
  <a href="#antes-y-después"><b>Antes y después</b></a> ·
  <a href="#cómo-se-compara"><b>vs caveman, rtk, ponytail</b></a> ·
  <a href="#antes-de-cambiarte"><b>Antes de cambiarte</b></a> ·
  <a href="BENCHMARKS.md"><b>Benchmarks (en inglés)</b></a>
</p>

---

> [!TIP]
> **En las tareas de programación de cada día, Sharur cuesta un 21% menos que el estilo Concise de Claude Code, y sus respuestas tienen un 54% menos de palabras que leer.** Todos los tests ocultos siguieron pasando. Medido en Claude Opus 5.5; el método y cada número están en [BENCHMARKS.md](BENCHMARKS.md).

Úsalo para gastar menos de tu plan de Claude en cada tarea y para leer cada respuesta más rápido: el resultado, el estado de los tests y lo que salió distinto, sin el párrafo de relleno alrededor.

## Qué ahorras

En el trabajo de programación de todos los días, Sharur cuesta un 21% menos que el estilo Concise que trae Claude Code. Es la mediana de cuatro tareas medianas en Claude Opus 5.5: arreglar tests que fallan, añadir una opción a un comando, revisar tres módulos en busca de bugs y rastrear cómo se calcula el total de un pedido (entre 4% y 26% según la tarea). Las tareas más grandes ahorran menos, y todos los resultados están en la tabla:

| Tarea | Tareas | Costo | Tokens de salida | Palabras que lees |
|---|---|---|---|---|
| Preguntas cortas y arreglos pequeños | 4 | -37% | -35% | -61% |
| Respuestas largas: una explicación, una auditoría | 2 | -21% | -23% | -38% |
| **Tareas medianas** | **4** | **-21%** | **-35%** | **-54%** |
| Funciones grandes: devoluciones, pasar a centavos enteros | 2 | -10% | -13% | -47% |
| Una tarea enorme: una especificación de 11 puntos | 1 | -6% | 0% | -28% |
| Medianas, grandes y enormes, con el mismo peso por tamaño | 7 | -12% | -16% | -43% |

Cada tarea se corrió 3 veces con cada estilo, y cada número es la mediana de los cambios por tarea. El costo es el que reporta la CLI, así que incluye el texto del propio estilo, que se lee en cada petición. Sharur salió más barato en las 13 tareas. Unos tests ocultos revisaron los archivos que dejó cada corrida, y todas los pasaron con los dos estilos. En las tareas medianas a enormes, un evaluador encontró los mismos datos obligatorios en las respuestas de ambos estilos.

La columna de palabras es el tiempo que pasas leyendo. En las tareas medianas, Concise escribió una mediana de 129 a 380 palabras por tarea y Sharur de 57 a 203, con los mismos datos.

Las preguntas son lo que más ahorra, pero pocas sesiones son sobre todo preguntas, así que no esperes un 37%. Cuanto más grande la tarea, menor el ahorro: una sesión larga gasta casi todos sus tokens en código, en llamadas a herramientas y en volver a leer el contexto en cada turno, y un output style no cambia nada de eso. [JetBrains encontró lo mismo](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/) con la skill caveman: anunciaba 65% y midió 8.5% en tareas reales de agente.

> [!NOTE]
> **Por qué la tarea enorme marca 0% en tokens de salida y aun así 6% menos de costo.** Ahí casi todo lo que escribe el modelo es código: unos 13,000 tokens de salida por corrida, de los que el texto de la respuesta es cerca del 3%. La respuesta de Sharur tuvo 28% menos palabras, unos 120 tokens, que se pierden en la variación entre corridas (de 9,700 a 17,400 tokens de salida con Concise). El costo bajó por otra razón: casi todo es el contexto que se vuelve a leer en cada llamada, y Sharur hizo 10 llamadas en cada corrida donde Concise hizo de 10 a 14. Con una sola tarea y 3 corridas, ese 6% queda dentro del ruido.

Cómo se midió y cómo repetirlo está en [BENCHMARKS.md](BENCHMARKS.md), en inglés.

## El estilo completo

```
Telegraphic: drop filler, keep grammar. <=2 lines, <=25 words. Bigger result: one short line per item, every item asked, no recap. No text before work is done. Say what was wrong, not a label for it. Exact: errors, destructive confirms. Fewest tool calls. Tool description fields <=3 words.
```

Además ocupa menos que las instrucciones de Concise, así que cada petición lleva unos 330 tokens de entrada menos.

## Antes y después

Mismo prompt, mismo modelo (Opus 5.5), mismo proyecto pequeño en Python: "Add a multiply function to calc.py with a test, and run the tests." El archivo de tests tiene un bug que el prompt no menciona. Las respuestas están en inglés, tal como las dio el modelo.

Concise, 89 palabras, 1,619 tokens de salida:

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

Sharur, 37 palabras, 1,012 tokens de salida:

> Added `multiply` to `calc.py` and a test, but the tests fail first at `assert subtract(5, 3) == 2`, so the multiply test never ran. `subtract` returns `a + b`; should I change it to `a - b`?

Cuando el resultado es más grande, escribe una línea por punto. Esto respondió Sharur a "The tests fail. Find the causes and fix them." en un proyecto de 9 archivos:

> All 19 tests pass now. The three causes:
> - `shop/inventory.py`: `reserve` refused an order for the last units because it checked `>=` instead of `>`.
> - `shop/pricing.py` `bulk_discount`: the 10-unit check ran first, so 50+ units got 5% instead of 10%.
> - `shop/pricing.py` `order_totals`: tax was charged before the coupon was taken off; it's now charged after.

## Instalación

Pega esto en Claude Code:

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

O hazlo a mano:

```bash
mkdir -p ~/.claude/output-styles
curl -fsSL https://raw.githubusercontent.com/ilien-dev/sharur/main/sharur.md -o ~/.claude/output-styles/sharur.md
```

Después elige Sharur en `/config`, en Output style.

> [!IMPORTANT]
> Abre una sesión nueva después de instalarlo: Claude Code lee el output style al empezar la sesión.

En Windows, `~` es `%USERPROFILE%`. Para usarlo en un solo proyecto, pon el archivo en `.claude/output-styles/` dentro de ese proyecto. Para volver atrás, elige otro estilo en `/config` y borra el archivo.

## Cómo se compara

Los tres ahorradores de tokens más populares para Claude Code pasaron por la misma prueba independiente de JetBrains: de 80 a 86 tareas reales de agente, corridas en pares y el costo tomado de la factura.

| | Qué cambia | Qué instalas | Anuncia | Lo que midió JetBrains |
|---|---|---|---|---|
| [caveman](https://github.com/JuliusBrussee/caveman), 121 mil estrellas | Cómo habla el agente, más un proxy, un selector de modelo y un servicio en la nube | Un plugin, o un instalador (Node.js 22) que añade una CLI y hooks | 65% menos tokens de salida | [8.5% menos tokens de salida](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/); cerca de 10% menos de costo por tarea, que una sola corrida atípica borró en los totales |
| [rtk](https://github.com/rtk-ai/rtk), 87 mil estrellas | Reduce la salida de los comandos antes de que el modelo la lea | Un binario de Rust y un hook | De 60 a 90% menos tokens | [Mediana del costo 7.6% más alta](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/) con esfuerzo bajo, sin cambio con esfuerzo alto |
| [ponytail](https://github.com/DietrichGebert/ponytail), 193 mil estrellas | Hace que el agente escriba menos código | Un plugin con un hook que corre al iniciar la sesión | 54% menos código, 20% menos costo | [15% menos código, 10.3% menos costo](https://blog.jetbrains.com/ai/2026/07/ponytail-skill-claude-tested/) |
| **Sharur** | **Cómo habla el agente** | **Un archivo Markdown** | **21% menos costo en tareas medianas** | JetBrains todavía no lo ha probado |

Lo que eso significa para ti:

- **No se ejecuta nada en tu máquina.** Ni binario, ni hook, ni proxy, ni cuenta, ni telemetría; la CLI de caveman envía estadísticas de uso por defecto, según su propio README. Para quitar Sharur, borras un archivo.
- **El límite es un número que el modelo puede seguir.** El README de caveman mide su propia voz un 3% más corta que la instrucción simple "Answer concisely." (10 intentos). Las respuestas de Sharur en tareas medianas tuvieron un 54% menos de palabras que Concise, el estilo corto que trae Claude Code.
- **Cada número sale de la factura y de tests ocultos.** El costo es el que reporta la CLI, incluido el texto del propio estilo, y los archivos que dejó cada corrida se probaron.
- **Funciona junto a ponytail.** ponytail recorta el código que escribe el agente y Sharur lo que dice, así que no se pisan. No se han medido juntos.

Dos cosas, para ser justos. Sharur solo cubre Claude Code, mientras que caveman funciona con más de 30 agentes. Y los números de Sharur salen de su propio benchmark de 13 tareas, no de las 86 de JetBrains, así que la última fila no se compara en igualdad de condiciones con las tres de arriba.

## Antes de cambiarte

> [!WARNING]
> - En tareas grandes el ahorro es pequeño: entre 6 y 10% del costo en estas pruebas. Los números grandes vienen de las preguntas y las tareas cortas.
> - Esta versión del estilo solo se midió en Opus 5.5, con 3 corridas por tarea. La versión anterior, de una línea, también se probó en Sonnet 5.5, Haiku 5.5 y Fable 5.2; esta no. Las corridas en Fable 5.2 que se hicieron al ajustarla dieron algo parecido, pero sirvieron para elegir el texto, así que no prueban nada.
> - "Fewest tool calls" cambia cómo trabaja el modelo, no solo cómo habla. Aquí nunca costó un test oculto, pero es lo primero que conviene borrar si ves que el modelo se salta un paso que debía dar.
> - Los informes están escritos para quien ya conoce la tarea. Si necesitas una descripción completa de un cambio, pídela o quédate con Concise.

## Por qué no hay hooks

Los hooks de Claude Code no pueden reescribir una respuesta. Un hook Stop solo puede bloquearla y mandar al modelo a otro turno, que vuelve a leer todo el contexto. Un hook PreToolUse puede recortar la entrada de una herramienta, pero cuando el modelo ya escribió esos tokens y ya se cobraron. En estas corridas el texto de la respuesta fue el 10% de lo que escribió el modelo en las tareas medianas a enormes, y los campos `description` de las herramientas menos del 1%: un hook tiene poco que ahorrar, y el turno extra cuesta más que eso. Un proxy que comprime la salida de las herramientas, rtk, [subió la mediana del costo un 7.6%](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/) en las pruebas de JetBrains. Sharur se queda en un archivo de texto.

Sharur es la maza del dios sumerio Ninurta. El nombre significa "el que aplasta a miles".

## Licencia

MIT
