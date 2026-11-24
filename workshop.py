"""
Punto de entrada unico del taller. NO hace falta activar ningun entorno virtual.

    python workshop.py setup        instala todo (solo la primera vez)
    python workshop.py check        comprueba que todo funciona
    python workshop.py ex1          ejercicio 1: fuzzing aleatorio
    python workshop.py ex2          ejercicio 2: fuzzing guiado por cobertura
    python workshop.py ex3          ejercicio 3: gramaticas (Fandango)
    python workshop.py ci           ejercicio 4: lo mismo que ejecuta GitHub Actions
    python workshop.py repro FICH   reproduce un crash guardado en crashes/

En Windows, si "python" no funciona, prueba con "py" (p.ej. py workshop.py setup).
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, ".venv")
IS_WIN = os.name == "nt"
VENV_PY = os.path.join(VENV, "Scripts", "python.exe") if IS_WIN else os.path.join(VENV, "bin", "python")
MIN_PY = (3, 11)

COMMANDS = {
    "ex1": os.path.join("fuzzers", "ex1_random.py"),
    "ex2": os.path.join("fuzzers", "ex2_greybox.py"),
    "ex3": os.path.join("fuzzers", "ex3_grammar.py"),
    "ex4": os.path.join("fuzzers", "ci_fuzz.py"),   # el ejercicio 4 es el CI: igual que "ci"
    "ci": os.path.join("fuzzers", "ci_fuzz.py"),
    "repro": os.path.join("target", "egc_parser.py"),
}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
except Exception:
    pass


def ok(msg):
    print("  [OK]   " + msg)


def fail(msg):
    print("  [FALLO] " + msg)


def in_venv():
    return os.path.realpath(sys.prefix) == os.path.realpath(VENV)


def check_python_version():
    if sys.version_info < MIN_PY:
        print("Tu Python es %d.%d, pero el taller necesita %d.%d o superior."
              % (sys.version_info[0], sys.version_info[1], MIN_PY[0], MIN_PY[1]))
        print("Instala Python 3.12 desde https://www.python.org/downloads/")
        print("(o usa Codespaces: en tu fork, Code -> Codespaces -> Create codespace)")
        sys.exit(1)


def setup():
    check_python_version()
    if not os.path.exists(VENV_PY):
        print("Creando entorno virtual en .venv ...")
        r = subprocess.run([sys.executable, "-m", "venv", VENV])
        if r.returncode != 0 or not os.path.exists(VENV_PY):
            print("\nNo se pudo crear el entorno virtual.")
            print("En Ubuntu/Debian: sudo apt install python3-venv   y vuelve a probar.")
            sys.exit(1)
    print("Instalando dependencias (puede tardar un minuto) ...")
    r = subprocess.run([VENV_PY, "-m", "pip", "install", "--disable-pip-version-check",
                        "-q", "-r", os.path.join(ROOT, "requirements.txt")])
    if r.returncode != 0:
        print("\nFallo la instalacion. ¿Tienes conexion a internet?")
        print("Los ejercicios 1 y 2 funcionan igualmente (no necesitan nada instalado).")
        sys.exit(1)
    print()
    sys.exit(subprocess.run([VENV_PY, os.path.join(ROOT, "workshop.py"), "check"]).returncode)


def check():
    print("Comprobando el entorno:\n")
    good = True
    if sys.version_info >= MIN_PY:
        ok("Python %d.%d" % sys.version_info[:2])
    else:
        fail("Python %d.%d (se necesita 3.11+)" % sys.version_info[:2]); good = False

    sys.path.insert(0, os.path.join(ROOT, "target"))
    try:
        from egc_parser import process
        assert process(b"EGC/1\nCALC 1+2\nMSG 4:hola") == [3, "hola"]
        ok("Programa objetivo (target/egc_parser.py)")
    except Exception as e:
        fail("Programa objetivo: %r" % e); good = False

    try:
        import fandango  # noqa: F401
        ok("Fandango instalado")
        sys.path.insert(0, os.path.join(ROOT, "fuzzers"))
        from ex3_grammar import generate
        inputs = generate(os.path.join(ROOT, "grammars", "egc.fan"), 3, quiet=True)
        assert inputs and all(i.startswith(b"EGC/1") for i in inputs)
        ok("Fandango genera entradas desde grammars/egc.fan")
    except Exception as e:
        fail("Fandango: %s" % e)
        print("         -> ejecuta:  python workshop.py setup")
        print("         (los ejercicios 1 y 2 funcionan sin Fandango)")
        good = False

    print()
    print("Todo listo! Empieza con:  python workshop.py ex1" if good
          else "Hay problemas. Avisa al profe o usa Codespaces.")
    return 0 if good else 1


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, rest = args[0], args[1:]

    if cmd == "setup":
        return setup()

    # Si existe .venv y no estamos dentro, nos re-ejecutamos con su Python.
    if os.path.exists(VENV_PY) and not in_venv():
        return subprocess.run([VENV_PY, os.path.abspath(__file__)] + args).returncode

    check_python_version()
    if cmd == "check":
        return check()
    if cmd not in COMMANDS:
        print("Comando desconocido: %r\n" % cmd)
        print(__doc__)
        return 1
    if cmd == "repro" and not rest:
        print("Uso: python workshop.py repro crashes/<fichero>")
        return 1
    try:
        return subprocess.run([sys.executable, os.path.join(ROOT, COMMANDS[cmd])] + rest).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
