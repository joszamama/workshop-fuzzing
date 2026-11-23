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
