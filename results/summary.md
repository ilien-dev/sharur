
Round 1: claude-opus-5-5, clean environment, prompts 1-6
| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |
|---|---|---|---|---|---|---|---|---|---|
| Concise | 12 | 111.8 | 667 | 302 | 2.50 | 0.079 | - | - | - |
| cavA | 12 | 107.5 | 583 | 312 | 2.42 | 0.067 | - | - | - |
| cavB | 12 | 71.0 | 542 | 196 | 2.17 | 0.067 | - | - | - |
| cavC | 12 | 30.8 | 393 | 76 | 2.33 | 0.063 | - | - | - |

Rounds 2-5: claude-fable-5-2, clean environment, prompts 1-6
| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |
|---|---|---|---|---|---|---|---|---|---|
| Concise | 12 | 97.3 | 579 | 248 | 2.33 | 0.154 | 100% | 100% | 4/4 |
| cavF | 12 | 34.3 | 455 | 84 | 2.17 | 0.115 | 100% | 100% | 4/4 |
| cavD | 12 | 28.5 | 408 | 76 | 2.00 | 0.114 | 100% | 100% | 4/4 |
| H4 | 12 | 22.0 | 404 | 49 | 2.25 | 0.114 | 100% | 67% | 4/4 |
| T5a | 12 | 23.6 | 397 | 65 | 2.08 | 0.113 | 97% | 83% | 4/4 |
| cavG | 12 | 23.1 | 383 | 69 | 2.00 | 0.111 | 97% | 100% | 4/4 |
| T4 | 12 | 23.8 | 379 | 65 | 2.00 | 0.112 | 97% | 92% | 4/4 |
| cavC | 12 | 28.7 | 378 | 77 | 1.83 | 0.111 | 100% | 92% | 4/4 |
| T3 | 12 | 20.6 | 378 | 53 | 1.92 | 0.112 | 97% | 100% | 4/4 |
| H1 | 12 | 13.4 | 373 | 35 | 2.17 | 0.111 | 84% | 100% | 4/4 |
| H3 | 12 | 11.9 | 372 | 21 | 1.92 | 0.110 | 88% | 100% | 4/4 |
| H2 | 12 | 17.6 | 371 | 34 | 2.17 | 0.111 | 97% | 92% | 4/4 |
| cavE | 12 | 22.8 | 369 | 63 | 1.83 | 0.111 | 97% | 83% | 4/4 |
| T5b | 24 | 23.2 | 352 | 68 | 1.67 | 0.109 | 98% | 83% | 8/8 |
| T1 | 24 | 21.8 | 344 | 62 | 1.75 | 0.109 | 100% | 96% | 8/8 |

Rounds 3-5: claude-fable-5-2, clean environment, 9 prompts (styles run on all 9)
| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |
|---|---|---|---|---|---|---|---|---|---|
| Concise | 18 | 87.7 | 645 | 248 | 2.94 | 0.161 | 98% | 100% | 6/6 |
| H4 | 18 | 23.2 | 498 | 49 | 2.89 | 0.127 | 100% | 78% | 6/6 |
| T5a | 18 | 22.6 | 473 | 65 | 2.72 | 0.126 | 94% | 83% | 6/6 |
| cavG | 18 | 22.5 | 459 | 69 | 2.67 | 0.126 | 96% | 100% | 6/6 |
| H3 | 18 | 16.6 | 455 | 21 | 2.50 | 0.123 | 92% | 100% | 6/6 |
| H1 | 18 | 14.3 | 447 | 35 | 2.72 | 0.123 | 84% | 94% | 6/6 |
| H2 | 18 | 20.4 | 444 | 34 | 2.67 | 0.122 | 94% | 94% | 6/6 |
| T4 | 18 | 22.8 | 401 | 65 | 2.28 | 0.120 | 92% | 89% | 6/6 |
| T3 | 18 | 19.4 | 396 | 53 | 2.17 | 0.120 | 96% | 100% | 6/6 |
| T5b | 36 | 21.7 | 344 | 68 | 1.78 | 0.116 | 97% | 89% | 12/12 |
| T1 | 36 | 20.1 | 338 | 62 | 1.83 | 0.116 | 100% | 97% | 12/12 |

Real environment (plugins, hooks, Spanish replies), claude-fable-5-2, prompts 1, 2, 6, 11
| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |
|---|---|---|---|---|---|---|---|---|---|
| Concise | 4 | 104.0 | 728 | 423 | 3.00 | 0.358 | 100% | 100% | 2/2 |
| T1 | 4 | 22.3 | 431 | 172 | 1.75 | 0.309 | 100% | 100% | 2/2 |

Same four prompts in the clean environment, for comparison
| style | runs | words/reply | output tokens/task | output tokens/question | tool calls/task | cost/task (USD) | info kept | clear | tasks ok |
|---|---|---|---|---|---|---|---|---|---|
| Concise | 8 | 116.1 | 774 | 320 | 3.63 | 0.160 | 100% | 100% | 4/4 |
| T1 | 16 | 21.9 | 326 | 61 | 1.88 | 0.111 | 100% | 100% | 8/8 |

runs: 344, total cost: $41.31
