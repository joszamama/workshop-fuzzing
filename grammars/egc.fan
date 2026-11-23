# Gramatica del protocolo EGC/1 para Fandango.
# Documentacion: https://fandango-fuzzer.github.io/

<start>    ::= <header> "\n" <commands>
<header>   ::= "EGC/1"
<commands> ::= <command> | <command> "\n" <commands>
<command>  ::= <calc> | <msg>

# ---- CALC <expresion> ----------------------------------------------------
<calc>     ::= "CALC " <expr>
<expr>     ::= <term> | <term> ("+" | "-") <expr>
<term>     ::= <factor> | <factor> ("*" | "/") <term>
# EJERCICIO 3 (TODO): un factor tambien puede ser una expresion entre parentesis.
#                     Anade esa alternativa a la regla <factor>.
<factor>   ::= <number>
<number>   ::= <digit>+

# ---- MSG <longitud>:<payload> --------------------------------------------
<msg>      ::= "MSG " <length> ":" <payload>
<length>   ::= <digit>+
<payload>  ::= <char>*
<char>     ::= r"[a-zA-Z0-9 !?.]"

# ⭐ EJERCICIO 3, SI VAS RAPIDO: la gramatica solo genera lo que tu le dices.
#    Cambia <number> para que a veces use digitos "raros", p.ej.:
#        <number> ::= (<digit> | "²")+
#    ¿Encuentras un bug nuevo? ¿Por que ocurre? (Pista: "²".isdigit() en Python)

# EJERCICIO 4 (TODO): restricciones semanticas.
# La gramatica genera MSG con longitudes aleatorias que casi nunca coinciden
# con el payload, asi que el parser las rechaza. Escribe restricciones con
# `where ...` para que:
#   1) la longitud declarada coincida con la longitud real del payload
#   2) (y luego...) ¿que pasa con mensajes largos?
# Pistas de sintaxis:
#   where forall <m> in <msg>: int(<m>.<length>) == ...
#   where exists <m> in <msg>: ...
#   str(<m>.<payload>)  -> el payload como string
#
# ⭐ EJERCICIO 4, SI VAS RAPIDO: arregla el bug que acabas de encontrar en
#    target/egc_parser.py (funcion cmd_msg) y vuelve a lanzar el ejercicio.
#    ¿Desaparece el bug? Asi se usa el fuzzing en la vida real: encontrar,
#    arreglar y comprobar que no vuelve (test de regresion).
