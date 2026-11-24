"""
Harness comun: ejecuta el objetivo con una entrada y clasifica el resultado.
No hace falta tocar este fichero.
"""
import hashlib
import os
import sys
import traceback

try:  # emojis y acentos en la consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "target"))
from egc_parser import ParseError, process  # noqa: E402

CRASH_DIR = os.path.join(os.path.dirname(__file__), "..", "crashes")
ALL_BUGS = set()  # firmas de todos los bugs vistos en esta ejecucion, sea cual sea el fuzzer


def classify(data: bytes):
    """Devuelve (resultado, firma_del_crash). resultado es uno de:
    'cabecera' (rechazada en la cabecera), 'rechazada' (rechazada mas adelante),
    'valida' (aceptada) o 'crash' (BUG)."""
    try:
        process(data)
    except ParseError as e:  # entrada invalida: comportamiento correcto
        return ("cabecera" if "cabecera" in str(e) else "rechazada"), None
    except Exception as e:  # cualquier otra cosa es un BUG
        tb = traceback.extract_tb(e.__traceback__)[-1]
        return "crash", f"{type(e).__name__} en {tb.name}() linea {tb.lineno}"
    return "valida", None


def run_one(data: bytes):
    """Devuelve None si todo va bien, o una 'firma' del crash si hay bug."""
    return classify(data)[1]


class CrashCollector:
    """Agrupa crashes por firma (tipo de excepcion + linea) y los guarda."""

    def __init__(self, fuzzer_name: str):
        self.fuzzer_name = fuzzer_name
        self.crashes = {}  # firma -> primera entrada que lo provoco
        self.stats = {"cabecera": 0, "rechazada": 0, "valida": 0, "crash": 0}

    def check(self, data: bytes) -> bool:
        result, sig = classify(data)
        self.stats[result] += 1
        if sig is None:
            return False
        ALL_BUGS.add(sig)
        if sig not in self.crashes:
            self.crashes[sig] = data
            print(f"\n  💥 NUEVO BUG: {sig}\n     entrada: {data[:80]!r}")
            os.makedirs(CRASH_DIR, exist_ok=True)
            name = hashlib.sha1(data).hexdigest()[:10]
            with open(os.path.join(CRASH_DIR, f"{self.fuzzer_name}-{name}"), "wb") as f:
                f.write(data)
        return True

    def report(self, execs: int, seconds: float):
        print(f"\n== {self.fuzzer_name}: {execs} ejecuciones en {seconds:.1f}s "
              f"({execs / max(seconds, 1e-9):.0f}/s) ==")
        total = max(sum(self.stats.values()), 1)
        pct = lambda k: f"{100 * self.stats[k] / total:.1f}%"
        print(f"   Rechazadas en la cabecera: {pct('cabecera'):>6}   "
              f"Rechazadas despues: {pct('rechazada'):>6}   "
              f"Validas: {pct('valida'):>6}   Crashes: {pct('crash'):>6}")
        if not self.crashes:
            print("   Ningun bug encontrado.")
        for sig, data in self.crashes.items():
            print(f"   - {sig}\n       {data[:80]!r}")
        return len(self.crashes)
