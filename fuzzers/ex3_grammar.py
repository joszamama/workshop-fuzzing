"""
EJERCICIOS 3 y 4 -- Fuzzing con gramaticas y restricciones (Fandango)
=====================================================================
Genera entradas con Fandango a partir de una gramatica (.fan) y las lanza
contra el programa. Lo que tienes que editar es grammars/egc.fan.

Ejecuta:   python workshop.py ex3                          (usa grammars/egc.fan)
           python workshop.py ex3 -n 500                   (genera 500 entradas)
           python workshop.py ex3 grammars/otra.fan
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

from harness import CrashCollector

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Lanzamos Fandango con el MISMO Python que ejecuta este script,
# asi no depende de que el comando "fandango" este en el PATH.
FANDANGO = [sys.executable, "-c",
            "import sys; from fandango.cli import main; sys.exit(main(*sys.argv[1:]))"]


def lint(fan_file: str) -> str:
    """Pistas para errores tipicos que Fandango no localiza bien."""
    hints = []
    with open(fan_file, encoding="utf-8") as f:
        for no, line in enumerate(f, 1):
            code = line.split("#", 1)[0] if not line.lstrip().startswith("where") else line
            if code.count('"') % 2:
                hints.append(f"  linea {no}: comillas \" sin cerrar ->  {line.rstrip()}")
            elif code.count("<") != code.count(">") and "where" not in code:
                hints.append(f"  linea {no}: < y > no cuadran ->  {line.rstrip()}")
    return ("\nPosibles errores:\n" + "\n".join(hints) + "\n") if hints else ""


def generate(fan_file: str, n: int, quiet: bool = False) -> list:
    try:
        import fandango  # noqa: F401
    except ImportError:
        raise SystemExit("\nFandango no esta instalado. Ejecuta:  python workshop.py setup\n")
    if not os.path.exists(fan_file):
        raise SystemExit(f"\nNo encuentro la gramatica: {fan_file}\n")

    out = tempfile.mkdtemp(prefix="fandango-")
    try:
        r = subprocess.run(FANDANGO + ["fuzz", "-f", fan_file, "-n", str(n), "-d", out],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise SystemExit("\nFandango ha dado un error (¿algo mal escrito en la gramatica?):\n\n"
                             + (r.stderr or r.stdout).strip()[-2000:] + "\n"
                             + lint(fan_file))
        inputs = []
        for name in sorted(os.listdir(out)):
            with open(os.path.join(out, name), "rb") as f:
                inputs.append(f.read())
        return inputs
    finally:
        shutil.rmtree(out, ignore_errors=True)


def main(fan_file: str, n: int):
    print(f"Generando {n} entradas con Fandango desde {os.path.relpath(fan_file)} ...")
    start = time.time()
    inputs = generate(fan_file, n)
    crashes = CrashCollector("grammar")
    for data in inputs:
        crashes.check(data)
    if inputs:
        print("Ejemplos de entradas generadas:")
        for data in inputs[:3]:
            print(f"   {data[:80]!r}")
    return crashes.report(len(inputs), time.time() - start)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 300
    if "-n" in args:
        i = args.index("-n"); n = int(args[i + 1]); del args[i:i + 2]
    fan = args[0] if args else os.path.join(ROOT, "grammars", "egc.fan")
    try:
        main(fan, n)
    except KeyboardInterrupt:
        print("\nInterrumpido.")
