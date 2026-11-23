# Hackea tu software: descubre vulnerabilidades antes de que lleguen a producción

Taller de fuzzing y CI/CD · ETSII, Universidad de Sevilla.

Tienes delante **EGC/1**, un protocolo de juguete y su parser ([target/egc_parser.py](target/egc_parser.py)).
Tiene **varios bugs ocultos**. Tu misión: encontrarlos **sin leer el código**, solo con fuzzers.
Cada técnica de fuzzing desbloquea bugs que la anterior no puede encontrar.

## 🏁 Antes de clase (5 minutos, en casa)

1. **Haz fork** de este repo: botón **Fork** (arriba a la derecha) → **Create fork**.
2. En **tu fork**, ve a la pestaña **Actions** y pulsa **"I understand my workflows, go ahead and enable them"**.
   (GitHub desactiva Actions en los forks. Sin este paso, el ejercicio 5 no funciona.)
3. Descarga **tu fork** en tu portátil:
   - Con git: `git clone https://github.com/TU-USUARIO/workshop-fuzzing.git`
   - Sin git: botón verde **Code → Download ZIP** y descomprímelo.
4. Necesitas **Python 3.11 o superior** ([python.org/downloads](https://www.python.org/downloads/)).
   En Windows, marca **"Add python.exe to PATH"** al instalarlo.
5. Abre una terminal **dentro de la carpeta del repo** y ejecuta:

```bash
python workshop.py setup
```

Si al final ves `Todo listo!`, ya está. **No hace falta activar ningún entorno virtual**:
`workshop.py` se encarga de todo.

> 💡 En Windows, si `python` no funciona, usa `py` (`py workshop.py setup`). En macOS/Linux puede que sea `python3`.

### ¿Algo falla? Plan B: Codespaces

En **tu fork**: **Code → Codespaces → Create codespace on main**. Se abre VS Code en el navegador
con todo instalado. Es gratis con tu cuenta de GitHub (no pide tarjeta).

### Comandos

| Comando | Qué hace |
|---|---|
| `python workshop.py check` | Comprueba que todo funciona |
| `python workshop.py ex1` | Ejercicio 1: fuzzing aleatorio |
| `python workshop.py ex2` | Ejercicio 2: fuzzing guiado por cobertura |
| `python workshop.py ex3` | Ejercicios 3 y 4: gramáticas (lee `grammars/egc.fan`) |
| `python workshop.py ci` | Lo mismo que ejecuta GitHub Actions |
| `python workshop.py repro crashes/<fichero>` | Reproduce un crash |

Los ejercicios 1 y 2 no necesitan nada instalado: funcionan aunque el Wi-Fi se caiga.

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
`python workshop.py repro crashes/<fichero>`.

## Ejercicios

| # | Técnica | Fichero | Tiempo |
|---|---------|---------|--------|
| 1 | Fuzzing aleatorio (blackbox) | [fuzzers/ex1_random.py](fuzzers/ex1_random.py) | ~5 min |
| 2 | Fuzzing guiado por cobertura (greybox) | [fuzzers/ex2_greybox.py](fuzzers/ex2_greybox.py) | ~12 min |
| 3 | Fuzzing con gramáticas (Fandango) | [grammars/egc.fan](grammars/egc.fan) | ~12 min |
| 4 | Gramáticas + restricciones (Fandango) | [grammars/egc.fan](grammars/egc.fan) | ~12 min |
| 5 | CI/CD: fuzzing en cada push (GitHub Actions) | [.github/workflows/fuzz.yml](.github/workflows/fuzz.yml) | ~10 min |

Cada fichero tiene marcados los `TODO` y unas preguntas para pensar. Edítalo y lánzalo con `python workshop.py exN`.

### Ejercicio 5: CI/CD

1. Comprueba que activaste *Actions* en tu fork (paso 2 de "Antes de clase").
2. Sube tus cambios a tu fork:
   - Si clonaste con git: `git add -A && git commit -m "mis fuzzers" && git push`
   - Si no (ZIP, o `git push` te pide contraseña): abre tu fork en GitHub y pulsa la tecla **`.`**.
     Se abre un editor en el navegador. Pega ahí tus cambios y haz commit desde el panel de la izquierda.

3. El workflow ejecuta **tus** fuzzers ([fuzzers/ci_fuzz.py](fuzzers/ci_fuzz.py)). Con los ejercicios sin hacer sale **verde**... ¿significa eso que el código no tiene bugs? 🤔
   Completa los ejercicios, haz push otra vez y verás el pipeline **en rojo**. Descarga el artifact `crashes`.
4. Arregla un bug en `target/egc_parser.py`, haz push y comprueba que ese bug desaparece del informe.
5. ¿Consigues un pipeline **verde**?

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
