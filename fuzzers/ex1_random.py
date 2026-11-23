"""
EJERCICIO 1 -- Fuzzing aleatorio (blackbox)
===========================================
Idea: generar entradas completamente aleatorias y lanzarlas contra el programa.

TODO: completa random_input() para que devuelva bytes aleatorios
      de longitud aleatoria (por ejemplo entre 0 y 100).

Ejecuta:   python workshop.py ex1            (30 segundos por defecto)
           python workshop.py ex1 10         (10 segundos)

Preguntas:
  - ¿Cuantos bugs encuentra? ¿Que tipo de bugs son?
  - ¿Cuantas entradas pasan de la cabecera "EGC/1"? ¿Por que?
"""
import random
import sys
import time

from harness import CrashCollector


def random_input() -> bytes:
    # TODO: devuelve bytes aleatorios de longitud aleatoria.
    # Pista: random.randint(a, b), random.randbytes(n)
    return b"EGC/1\nCALC 1+1"


def main(budget: float):
    crashes = CrashCollector("random")
    start, execs = time.time(), 0
    while time.time() - start < budget:
        crashes.check(random_input())
        execs += 1
    return crashes.report(execs, time.time() - start)


if __name__ == "__main__":
    try:
        main(float(sys.argv[1]) if len(sys.argv) > 1 else 30)
    except KeyboardInterrupt:
        print("\nInterrumpido.")
