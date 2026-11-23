"""
EJERCICIO 2 -- Fuzzing guiado por cobertura (greybox, estilo AFL / libFuzzer)
============================================================================
Idea: en vez de generar desde cero, MUTAMOS entradas que ya tenemos (semillas).
Si una mutacion ejecuta codigo nuevo (nueva cobertura), la guardamos en el
corpus para seguir mutandola. Asi el fuzzer "aprende" el formato poco a poco.

Este fuzzer cabe en ~60 lineas. AFL++ hace lo mismo pero en C,
instrumentando el binario y a millones de ejecuciones por segundo.

TODO 1: completa mutate() con las tres mutaciones
        (cambiar, borrar e insertar un byte). Sin ellas, el fuzzer no muta nada!
TODO 2: anade semillas en seeds/ (ficheros con entradas validas).
        ¿Que pasa si no hay semillas? ¿Y si las hay?

Ejecuta:   python workshop.py ex2            (90 segundos por defecto)
"""
import os
import random
import sys
import time

from harness import CrashCollector, run_one

TARGET_FILE = "egc_parser.py"
SEED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seeds")


# ---------------------------------------------------------------- cobertura
def coverage_of(data: bytes) -> frozenset:
    """Ejecuta el objetivo y devuelve las lineas que se han ejecutado."""
    lines = set()

    def tracer(frame, event, arg):
        if not frame.f_code.co_filename.endswith(TARGET_FILE):
            return None
        if event == "line":
            lines.add(frame.f_lineno)
        return tracer

    sys.settrace(tracer)
    try:
        run_one(data)
    finally:
        sys.settrace(None)
    return frozenset(lines)


# ---------------------------------------------------------------- mutaciones
def mutate(data: bytes) -> bytes:
    data = bytearray(data)
    choice = random.randint(0, 2)

    if choice == 0:
        # TODO: cambiar un byte en una posicion aleatoria por otro aleatorio
        # Pista: random.randrange(len(data)) da una posicion, random.randrange(256) un byte
        pass

    elif choice == 1:
        # TODO: borrar un byte en una posicion aleatoria
        pass

    elif choice == 2:
        # TODO: insertar un byte aleatorio en una posicion aleatoria
        pass

    return bytes(data)


# ---------------------------------------------------------------- bucle
def load_seeds() -> list:
    seeds = []
    if os.path.isdir(SEED_DIR):
        for name in sorted(os.listdir(SEED_DIR)):
            with open(os.path.join(SEED_DIR, name), "rb") as f:
                seeds.append(f.read())
    return seeds or [b""]


def main(budget: float):
    crashes = CrashCollector("greybox")
    corpus = load_seeds()
    seen = set()
    for s in corpus:
        seen |= coverage_of(s)
    print(f"Corpus inicial: {len(corpus)} semillas, {len(seen)} lineas cubiertas")

    start, execs = time.time(), 0
    while time.time() - start < budget:
        child = mutate(random.choice(corpus))
        for _ in range(random.randint(0, 3)):   # a veces, varias mutaciones seguidas
            child = mutate(child)
        execs += 1
        cov = coverage_of(child)
        if crashes.check(child):
            continue
        if not cov <= seen:                       # ¡cobertura nueva!
            seen |= cov
            corpus.append(child)
            print(f"  [{time.time() - start:5.1f}s] +cobertura ({len(seen)} lineas): {child[:60]!r}")

    print(f"Corpus final: {len(corpus)} entradas")
    return crashes.report(execs, time.time() - start)


if __name__ == "__main__":
    try:
        main(float(sys.argv[1]) if len(sys.argv) > 1 else 90)
    except KeyboardInterrupt:
        print("\nInterrumpido.")
