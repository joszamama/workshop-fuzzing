<start>    ::= <header> "\n" <commands>
<header>   ::= "EGC/1"
<commands> ::= <command> | <command> "\n" <commands>
<command>  ::= <calc> | <msg>

<calc>     ::= "CALC " <expr>
<expr>     ::= <number> | <expr> <op> <expr> | "(" <expr> ")"
<op>       ::= "+" | "-" | "*" | "/"
<number>   ::= <digit>+

<msg>      ::= "MSG " <length> ":" <payload>
<length>   ::= <digit>+
<payload>  ::= <char>*
<char>     ::= r"[a-zA-Z0-9 !?.]"

where forall <m> in <msg>: int(<m>.<length>) == len(str(<m>.<payload>))
where exists <m> in <msg>: int(<m>.<length>) > 32
