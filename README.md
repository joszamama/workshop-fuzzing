# Hackea tu software: descubre vulnerabilidades antes de que lleguen a producción

Taller de fuzzing y CI/CD · ETSII, Universidad de Sevilla.

Tienes delante **EGC/1**, un protocolo de juguete y su parser ([target/egc_parser.py](target/egc_parser.py)).
Tiene **varios bugs ocultos**. Tu misión: encontrarlos **sin leer el código**, solo con fuzzers.
Cada técnica de fuzzing desbloquea bugs que la anterior no puede encontrar.

## Instalación (2 minutos)

Solo necesitas **Python 3.11 o superior**. Todo es Python puro y funciona en Linux, macOS y Windows.

```bash
git clone <url-de-este-repo> && cd workshop-fuzzing
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

¿Sin Python en tu portátil? Botón **Code → Codespaces → Create codespace** (gratis con tu cuenta de GitHub).

## El protocolo EGC/1

```
EGC/1
CALC (1+2)*3
MSG 4:hola
```

- Línea 1: cabecera, siempre `EGC/1`.
- Después, uno o más comandos: `CALC <expresión>` o `MSG <longitud>:<payload>`.
- Si la entrada es inválida, el parser lanza `ParseError`, que es lo **correcto**. Cualquier **otra** excepción es un **bug**.

Las entradas que provocan crash se guardan en `crashes/`. Para reproducir una:

```bash
python target/egc_parser.py crashes/<fichero>
```

## Ejercicios

| # | Técnica | Fichero | Tiempo |
|---|---------|---------|--------|
| 1 | Fuzzing aleatorio (blackbox) | [fuzzers/ex1_random.py](fuzzers/ex1_random.py) | ~5 min |
| 2 | Fuzzing guiado por cobertura (greybox) | [fuzzers/ex2_greybox.py](fuzzers/ex2_greybox.py) | ~12 min |
| 3 | Fuzzing con gramáticas (Fandango) | [grammars/egc.fan](grammars/egc.fan) | ~12 min |
| 4 | Gramáticas + restricciones (Fandango) | [grammars/egc.fan](grammars/egc.fan) | ~12 min |
| 5 | CI/CD: fuzzing en cada push (GitHub Actions) | [.github/workflows/fuzz.yml](.github/workflows/fuzz.yml) | ~10 min |

Cada fichero tiene marcados los `TODO` y unas preguntas para pensar.

```bash
python fuzzers/ex1_random.py        # ej. 1
python fuzzers/ex2_greybox.py       # ej. 2
python fuzzers/ex3_grammar.py       # ej. 3 y 4 (usa grammars/egc.fan)
```

### Ejercicio 5: CI/CD

1. Haz **fork** de este repo y activa *Actions* en tu fork.
2. Haz un push: el workflow ejecuta **tus** fuzzers ([fuzzers/ci_fuzz.py](fuzzers/ci_fuzz.py)). Con los ejercicios sin hacer sale **verde**... ¿significa eso que el código no tiene bugs? 🤔
   Completa los ejercicios, haz push otra vez y verás el pipeline **en rojo**. Descarga el artifact `crashes`.
3. Arregla un bug en `target/egc_parser.py`, haz push y comprueba que ese bug desaparece del informe.
4. ¿Consigues un pipeline **verde**?

## ¿Vas sobrado? Extras ⭐

- **⭐ El bug secreto.** Hay al menos un bug que no está "previsto". El greybox suele encontrarlo. ¿Por qué ocurre? Pista: Unicode.
- **⭐ Diccionario.** Mejora `mutate()` para que a veces inserte palabras clave (`"CALC "`, `"MSG "`, `"DEBUG"`…). ¿Cuánto más rápido encuentra los bugs? AFL++ lo llama *dictionaries*.
- **⭐ Sin semillas.** Borra `seeds/` y lanza el greybox. ¿Llega a pasar de la cabecera? ¿Por qué?
- **⭐⭐ Oráculo diferencial.** Compara el resultado de `CALC` con `eval()` de Python sobre la misma expresión. ¿Coinciden siempre? (Pista: ¿qué hace `/` en cada uno?)
- **⭐⭐ Atheris.** Usa [Atheris](https://github.com/google/atheris), el fuzzer de Google para Python, sobre `process()`. Funciona mejor en Linux o Codespaces.
- **⭐⭐⭐ Arréglalo todo.** Corrige todos los bugs y consigue que el CI pase en verde 5 veces seguidas.

Las soluciones están en la rama [`solutions`](../../tree/solutions). Sin trampas 😉

---
Más para casa: [HOMEWORK.md](HOMEWORK.md)
