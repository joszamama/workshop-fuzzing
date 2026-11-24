"""
Ejecuta TUS fuzzers (ejercicios 1-3) con un presupuesto de tiempo corto, pensado para CI.
Sale con codigo 1 si se encuentra algun bug -> el pipeline se pone en rojo.

    python workshop.py ci [segundos_por_fuzzer]
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ex1_random, ex2_greybox, ex3_grammar, harness  # noqa: E402

budget = float(sys.argv[1]) if len(sys.argv) > 1 else 15
ex1_random.main(budget)
ex2_greybox.main(max(budget, 90))

# La gramatica (ejercicio 3) se lanza sin restricciones.
fan = os.path.join(HERE, "..", "grammars", "egc.fan")
with open(fan, encoding="utf-8") as f:
    lines = f.readlines()
no_constraints = [l for l in lines if not l.lstrip().startswith("where")]
with tempfile.NamedTemporaryFile("w", suffix=".fan", delete=False, encoding="utf-8") as tmp:
    tmp.writelines(no_constraints)
ex3_grammar.main(tmp.name, 300)
os.unlink(tmp.name)

# Si has hecho el reto para casa (lineas "where" en egc.fan), se lanza otra vez
# con ellas: las restricciones "enfocan" la generacion y dejan de explorar
# otras zonas, asi que hacen falta las dos pasadas.
if len(no_constraints) != len(lines):
    ex3_grammar.main(fan, 100)

total = len(harness.ALL_BUGS)
print(f"\nTOTAL de bugs distintos encontrados: {total}")
sys.exit(1 if total else 0)
