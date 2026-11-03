from pathlib import Path

from lexer import nuevo_lexer, errores
from parser import nuevo_parser

parser = nuevo_parser()


def analizar(codigo):
    lex = nuevo_lexer()
    lex.input(codigo)
    for _ in lex:
        pass
    if errores:
        raise Exception("\n".join(errores))
    parser.parse(codigo, lexer=nuevo_lexer())


def test(nombre_test, archivo, debe_pasar):
    codigo = Path("tests", archivo).read_text(encoding="utf-8")
    print(f"\n{'=' * 50}")
    print(f"TEST: {nombre_test} ({archivo})")
    print(f"{'=' * 50}")
    print(f"Código:\n{codigo}")
    print("Resultado:")

    try:
        analizar(codigo)
        print("✓ Análisis léxico y sintáctico correcto")
        if debe_pasar:
            print("La prueba pasa sin errores como se esperaba")
            return True
        print("La prueba debía fallar pero pasó")
        return False
    except Exception as e:
        print(f"✗ {e}")
        if not debe_pasar:
            print("La prueba tiene errores como se esperaba")
            return True
        print("La prueba debía pasar pero falló")
        return False


cases = [
    ("Programa correcto", "correcto.baby", True),
    ("Expresiones aritméticas", "expresiones.baby", True),
    ("Programa con funciones", "funciones.baby", True),
    ("Errores léxicos", "error_lexico.baby", False),
    ("Errores sintácticos", "error_sintactico.baby", False),
]


def runtests():

    passed = sum(test(nombre, archivo, debe_pasar) for nombre, archivo, debe_pasar in cases)

    print(f"Pruebas: {passed}/{len(cases)} dieron el resultado esperado")



if __name__ == "__main__":
    runtests()
