"""
Ejecuta TUS fuzzers (ejercicios 1-4) con un presupuesto de tiempo corto, pensado para CI.
Sale con codigo 1 si se encuentra algun bug -> el pipeline se pone en rojo.

    python workshop.py ci [segundos_por_fuzzer]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ex1_random, ex2_greybox, ex3_grammar  # noqa: E402

budget = float(sys.argv[1]) if len(sys.argv) > 1 else 15
found = 0
found += ex1_random.main(budget)
found += ex2_greybox.main(max(budget, 90))
# La gramatica se ejecuta dos veces: sin restricciones (ej. 3) y con ellas (ej. 4),
# porque las restricciones "enfocan" la generacion y dejan de explorar otras zonas.
import tempfile  # noqa: E402
fan = os.path.join(HERE, "..", "grammars", "egc.fan")
with open(fan, encoding="utf-8") as f:
    no_constraints = [l for l in f if not l.lstrip().startswith("where")]
with tempfile.NamedTemporaryFile("w", suffix=".fan", delete=False, encoding="utf-8") as tmp:
    tmp.writelines(no_constraints)
found += ex3_grammar.main(tmp.name, 300)
os.unlink(tmp.name)
found += ex3_grammar.main(fan, 100)
print(f"\nTOTAL de bugs distintos encontrados: {found}")
sys.exit(1 if found else 0)
