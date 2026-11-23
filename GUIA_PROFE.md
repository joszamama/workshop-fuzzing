# Guía del profe (solo en la rama `solutions`)

Formato de cada ejercicio: **ellos intentan → tú lo resuelves en directo → pregunta al aula → siguiente.**
Quien no haya terminado copia de tu pantalla: las soluciones son muy cortas.

Antes de empezar: ten **dos terminales** abiertas, una en `main` (para el live coding, igual que ellos)
y otra en esta rama (por si algo falla). Pon un temporizador visible.

| Bloque | Ellos | Tú en directo | Total |
|---|---|---|---|
| Arranque: `python workshop.py check` | 3' | — | 3' |
| Ej. 1 Aleatorio | 4' | 3' | 7' |
| Ej. 2 Greybox | 8' | 5' | 13' |
| Ej. 3 Gramáticas | 6' | 4' | 10' |
| Ej. 4 Restricciones | 8' | 5' | 13' |
| Ej. 5 CI/CD | 5' | 5' | 10' |
| **Total** | | | **~56'** |

Si vas mal de tiempo, recorta primero el "ellos" del Ej. 4 y hazlo directamente en directo.

---

## Ej. 1: Fuzzing aleatorio

**En directo** (`fuzzers/ex1_random.py`):
```python
return random.randbytes(random.randint(0, 100))
```
`python workshop.py ex1 10`, y después `python workshop.py repro crashes/random-...`

**Qué señalar:**
- Encuentra el `ZeroDivisionError` (entrada vacía) en menos de 1 s: los bugs "superficiales" son baratos.
- **"Rechazadas en la cabecera: 99%"**. Pregunta al aula: *¿cuánto tardaría en generar `EGC/1` por azar?* (256⁵ ≈ 10¹² intentos).
- ⭐ Quien hizo el fuzzer "con trampa": pasa la cabecera, pero sigue sin generar comandos válidos.

## Ej. 2: Greybox

**En directo** (`mutate()`):
```python
if choice == 0:
    if data:
        data[random.randrange(len(data))] = random.randrange(256)
elif choice == 1:
    if data:
        del data[random.randrange(len(data))]
elif choice == 2:
    data.insert(random.randint(0, len(data)), random.randrange(256))
```
`python workshop.py ex2 30`

**Qué señalar:**
- Lee en voz alta las líneas `+cobertura`: **`D…`, `DE…`, `DEB…`, `DEBU…`, 💥**. El fuzzer "aprende" el backdoor letra a letra, porque cada `if` superado es cobertura nueva.
- Un backdoor de debug olvidado es un bug real (CWE-489).
- Pregunta: *¿por qué no encuentra el bug de los paréntesis?* La cobertura no distingue la profundidad de anidamiento, y además las mutaciones de bytes rompen la sintaxis.
- ⭐ Sin semillas: no pasa nunca de la cabecera. Las semillas importan (OSS-Fuzz pide un corpus).

## Ej. 3: Gramáticas

**En directo** (`grammars/egc.fan`):
```
<factor>   ::= <number> | "(" <expr> ")"
```
`python workshop.py ex3`

**Qué señalar:**
- **"Válidas: ~85%"** frente al 0% del aleatorio. La gramática "habla el idioma" del programa.
- Pregunta: *¿y los MSG?* La gramática genera `MSG 7880796871807:XEq...`, sintácticamente correcto pero con una longitud que no cuadra. La gramática no entiende la **semántica**.
- ⭐ El bug de `"²"`: en Python, `"²".isdigit()` da `True` pero `int("²")` falla. La gramática solo genera lo que tú le dices: si no imaginas Unicode, no lo prueba.

## Ej. 4: Restricciones

**En directo**, en dos pasos (ejecuta entre uno y otro):
```
where forall <m> in <msg>: int(<m>.<length>) == len(str(<m>.<payload>))
```
→ todos los MSG son válidos... y no hay bug nuevo. Pregunta: *¿por qué?* Los payloads son cortos.
```
where exists <m> in <msg>: int(<m>.<length>) > 32
```
→ 💥 overflow del buffer (`BUFFER_SIZE = 32`). Tarda ~30 s.

**Qué señalar:**
- `forall` frente a `exists`: un `forall` se cumple aunque no haya ningún MSG (es la trampa en la que caen casi todos).
- Las restricciones expresan lo que el programa **espera**; el bug vive justo en el borde de lo que espera.
- Estos patrones (campo de longitud + payload, checksums) están en casi todos los formatos binarios reales: PNG, ZIP, TLS...

## Ej. 5: CI/CD

**En directo:**
1. Haz push de tu `main` con los 4 ejercicios resueltos a **un fork tuyo de prueba** (prepáralo antes de clase).
2. Enseña la pestaña Actions en rojo, el log con los 4 bugs y descarga el artifact `crashes`.
3. Arregla un bug en directo, por ejemplo el de `checksum`:
   ```python
   if not data:
       raise ParseError("mensaje vacio")
   ```
   Haz push y enseña que el informe baja de 4 bugs a 3.

**Qué señalar:**
- Pregunta: *el pipeline estaba en verde al principio, ¿significaba que no había bugs?* No: solo que los fuzzers no buscaban. **El verde es tan bueno como tus tests.**
- ¿Cuánto tiempo dar al fuzzing en CI? Unos minutos por push, horas cada noche (⭐ `schedule`). Así funcionan ClusterFuzzLite y OSS-Fuzz.
- Para lanzar el CI de esta rama: Actions → Fuzzing → Run workflow → `solutions`.

---

## Resumen para la discusión final

| Técnica | Encuentra | No encuentra porque... |
|---|---|---|
| Aleatorio | Entrada vacía | No pasa de la cabecera |
| Greybox | Backdoor `DEBUG` | La cobertura no ve la profundidad; muta bytes, no estructura |
| Gramática | Paréntesis anidados | No entiende relaciones entre campos |
| Gramática + restricciones | Overflow de `MSG` | Solo prueba lo que modelas (el bug de `²`) |
