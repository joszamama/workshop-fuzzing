"""
EJERCICIOS 3 y 4 -- Fuzzing con gramaticas y restricciones (Fandango)
=====================================================================
Genera entradas con Fandango a partir de una gramatica (.fan) y las lanza
contra el programa.

Ejecuta:   python fuzzers/ex3_grammar.py                       (usa grammars/egc.fan)
           python fuzzers/ex3_grammar.py grammars/otra.fan -n 500
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

from harness import CrashCollector

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def main(fan_file: str, n: int):
    out = tempfile.mkdtemp(prefix="fandango-")
    fandango = shutil.which("fandango") or "fandango"
    print(f"Generando {n} entradas con Fandango desde {fan_file} ...")
    start = time.time()
    subprocess.run([fandango, "fuzz", "-f", fan_file, "-n", str(n), "-d", out],
                   check=True)
    crashes = CrashCollector("grammar")
    files = sorted(os.listdir(out))
    for name in files:
        with open(os.path.join(out, name), "rb") as f:
            crashes.check(f.read())
    print(f"(ejemplo de entrada generada: {open(os.path.join(out, files[0]), 'rb').read()[:80]!r})" if files else "")
    shutil.rmtree(out)
    return crashes.report(len(files), time.time() - start)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 300
    if "-n" in args:
        i = args.index("-n"); n = int(args[i + 1]); del args[i:i + 2]
    fan = args[0] if args else os.path.join(ROOT, "grammars", "egc.fan")
    main(fan, n)
