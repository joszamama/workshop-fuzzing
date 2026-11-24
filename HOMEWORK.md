# Para seguir aprendiendo

## Lo primero: el cuarto bug
En clase encontraste tres bugs. Queda uno, y ya viste la pista: con la gramática del ejercicio 3, el programa
**rechaza la mayoría de las entradas**. ¿Por qué, si la gramática dice cómo son?

1. Mira los `MSG` que salen en tu terminal (`python workshop.py ex3`). ¿Qué dice el número? ¿Y el texto?
2. Abre [grammars/egc.fan](grammars/egc.fan) y ve al final, a **RETO PARA CASA**. Ahí hay dos líneas `where` por completar:
   son **restricciones**, condiciones en Python que las entradas generadas tienen que cumplir.
3. Completa el paso 1, ejecuta `python workshop.py ex3`, y después el paso 2.
4. Haz push: el CI lanza la gramática con y sin restricciones, y el informe pasa de tres bugs a cuatro.

La solución está en la rama [`solutions`](../../tree/solutions) (`solutions/egc.fan`). Si lo encuentras, o te atascas, escríbeme.

## Lecturas
- **[The Fuzzing Book](https://www.fuzzingbook.org/)** (Zeller et al.). Gratis, interactivo y en Python. Es la mejor entrada al tema.
- **[Fandango](https://fandango-fuzzer.github.io/)**: documentación y tutorial de fuzzing con gramáticas y restricciones.
- **[AFL++ docs](https://aflplus.plus/docs/)**: el fuzzer greybox de referencia en la industria.

## Retos con este mismo repo
- **⭐ Arréglalo todo.** Corrige todos los bugs de `target/egc_parser.py` y consigue que el CI pase en verde 5 veces seguidas.
- **⭐⭐ Oráculo diferencial.** No todos los bugs son crashes. Compara el resultado de `CALC` con `eval()` de Python sobre la misma expresión. ¿Coinciden siempre? (Pista: ¿qué hace `/` en cada uno?)
- **⭐⭐ Atheris.** Usa [Atheris](https://github.com/google/atheris), el fuzzer de Google para Python, sobre `process()`. Compáralo con nuestro greybox. Funciona mejor en Linux o Codespaces.

## Retos con software real
1. **Haz fuzzing de algo real.** Escoge una librería Python que parsee algo (JSON, YAML, Markdown, fechas…) y escribe un harness con Atheris. ¿Encuentras excepciones no documentadas?
2. **AFL++ en C.** Compila un programa C pequeño con `afl-cc` y fuzzéalo. Compara la velocidad con nuestro greybox en Python.
3. **Escribe una gramática** de un formato que conozcas (CSV, URLs, un subconjunto de SQL) y úsala con Fandango contra un parser real.
4. **Fuzzing en tu proyecto.** Añade un workflow de fuzzing a tu proyecto de EGC o a tu TFG. Mira [ClusterFuzzLite](https://google.github.io/clusterfuzzlite/).
5. **OSS-Fuzz.** Explora [OSS-Fuzz](https://google.github.io/oss-fuzz/): miles de bugs encontrados en proyectos open source. Elige uno y lee su harness.
