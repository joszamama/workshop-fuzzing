"""
Ejecuta todos los fuzzers con un presupuesto de tiempo corto (pensado para CI).
Sale con codigo 1 si se encuentra algun bug -> el pipeline se pone en rojo.

    python solutions/ci_fuzz.py [segundos_por_fuzzer]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ex1_random, ex2_greybox, ex3_grammar  # noqa: E402
import harness  # noqa: E402  (esta en fuzzers/; los modulos de arriba lo ponen en el path)

budget = float(sys.argv[1]) if len(sys.argv) > 1 else 15
ex1_random.main(budget)
ex2_greybox.main(max(budget, 90))
ex3_grammar.main(os.path.join(HERE, "egc_ex3.fan"), 300)  # ejercicio 3: solo la gramatica
ex3_grammar.main(os.path.join(HERE, "egc.fan"), 100)      # reto para casa: con restricciones
total = len(harness.ALL_BUGS)
print(f"\nTOTAL de bugs distintos encontrados: {total}")
sys.exit(1 if total else 0)
