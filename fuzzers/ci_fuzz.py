"""
Ejecuta TUS fuzzers (ejercicios 1-4) con un presupuesto de tiempo corto, pensado para CI.
Sale con codigo 1 si se encuentra algun bug -> el pipeline se pone en rojo.

    python fuzzers/ci_fuzz.py [segundos_por_fuzzer]
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
found += ex3_grammar.main(os.path.join(HERE, "..", "grammars", "egc.fan"), 300)
print(f"\nTOTAL de bugs distintos encontrados: {found}")
sys.exit(1 if found else 0)
