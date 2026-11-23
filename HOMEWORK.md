# Para seguir aprendiendo

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
