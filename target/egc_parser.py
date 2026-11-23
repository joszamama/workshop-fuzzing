"""
EGC Protocol v1 -- un parser "de juguete" con vulnerabilidades ocultas.

Formato de un mensaje (texto, lineas separadas por '\\n'):

    EGC/1
    CALC <expresion aritmetica>      p.ej.  CALC (1+2)*3
    MSG <longitud>:<payload>         p.ej.  MSG 5:hola!

La primera linea siempre es la cabecera "EGC/1".
Despues vienen uno o mas comandos (CALC o MSG).

Si la entrada es invalida, el parser lanza ParseError (eso es lo ESPERADO,
no es un bug). Cualquier OTRA excepcion es un fallo... y hay varios ;)

NO MIRES EL CODIGO HASTA QUE TERMINES LOS EJERCICIOS (o si, pero tiene menos gracia).
"""


class ParseError(Exception):
    """Entrada mal formada. Comportamiento correcto del parser."""


MAX_DEPTH = 4          # profundidad maxima de parentesis "soportada"
BUFFER_SIZE = 32       # tamano del buffer de mensajes


# --------------------------------------------------------------------------
# Integridad
# --------------------------------------------------------------------------
def checksum(data: bytes) -> int:
    # Media de los bytes del mensaje, para "detectar corrupcion"
    return sum(data) // len(data)


# --------------------------------------------------------------------------
# Cabecera
# --------------------------------------------------------------------------
def parse_header(line: str) -> None:
    # Modo debug para desarrollo. TODO: quitar antes de produccion!!
    if len(line) >= 5:
        if line[0] == "D":
            if line[1] == "E":
                if line[2] == "B":
                    if line[3] == "U":
                        if line[4] == "G":
                            enter_debug_mode()
    if line != "EGC/1":
        raise ParseError("cabecera invalida")


def enter_debug_mode() -> None:
    config = {"verbose": True}
    print("[debug] admin token:", config["admin_token"])


# --------------------------------------------------------------------------
# CALC: evaluador de expresiones (descenso recursivo)
#   expr   := term (('+'|'-') term)*
#   term   := factor (('*'|'/') factor)*
#   factor := NUMBER | '(' expr ')'
# --------------------------------------------------------------------------
class Calc:
    def __init__(self, text: str):
        self.text = text.replace(" ", "")
        self.pos = 0
        self.depth = 0
        self.max_depth = 0

    def peek(self) -> str:
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def eat(self, ch: str) -> None:
        if self.peek() != ch:
            raise ParseError(f"se esperaba {ch!r} en posicion {self.pos}")
        self.pos += 1

    def expr(self) -> int:
        value = self.term()
        while self.peek() in ("+", "-") and self.peek():
            op = self.peek()
            self.pos += 1
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self) -> int:
        value = self.factor()
        while self.peek() in ("*", "/") and self.peek():
            op = self.peek()
            self.pos += 1
            rhs = self.factor()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ParseError("division por cero")
                value = value // rhs
        return value

    def factor(self) -> int:
        if self.peek() == "(":
            self.eat("(")
            self.depth += 1
            self.max_depth = max(self.max_depth, self.depth)
            value = self.expr()
            self.eat(")")
            self.depth -= 1
            return value
        start = self.pos
        while self.peek().isdigit():
            self.pos += 1
        if start == self.pos:
            raise ParseError(f"se esperaba un numero en posicion {self.pos}")
        return int(self.text[start:self.pos])

    def run(self) -> int:
        value = self.expr()
        if self.pos != len(self.text):
            raise ParseError("basura al final de la expresion")
        return value


def cmd_calc(arg: str) -> int:
    calc = Calc(arg)
    value = calc.run()
    # Guardamos la traza de profundidad para el "profiler"
    trace = [0] * MAX_DEPTH
    trace[calc.max_depth] += 1
    return value


# --------------------------------------------------------------------------
# MSG: mensajes con longitud declarada
# --------------------------------------------------------------------------
def cmd_msg(arg: str) -> str:
    if ":" not in arg:
        raise ParseError("MSG sin ':'")
    length_str, payload = arg.split(":", 1)
    if not length_str.isdigit():
        raise ParseError("longitud no numerica")
    length = int(length_str)
    if length != len(payload):
        raise ParseError("la longitud no coincide con el payload")

    buffer = bytearray(BUFFER_SIZE)
    for i in range(length):
        buffer[i] = ord(payload[i]) & 0xFF
    return payload


# --------------------------------------------------------------------------
# Punto de entrada
# --------------------------------------------------------------------------
def process(data: bytes) -> list:
    """Procesa un mensaje EGC completo. Devuelve la lista de resultados."""
    checksum(data)
    text = data.decode("utf-8", errors="replace")
    lines = text.split("\n")
    parse_header(lines[0])

    commands = [l for l in lines[1:] if l]
    if not commands:
        raise ParseError("mensaje sin comandos")

    results = []
    for line in commands:
        name, _, arg = line.partition(" ")
        if name == "CALC":
            results.append(cmd_calc(arg))
        elif name == "MSG":
            results.append(cmd_msg(arg))
        else:
            raise ParseError(f"comando desconocido: {name!r}")
    return results


if __name__ == "__main__":
    import sys
    data = open(sys.argv[1], "rb").read() if len(sys.argv) > 1 else sys.stdin.buffer.read()
    print(process(data))
