import sys
from pathlib import Path

from lexer import nuevo_lexer, errores
from parser import nuevo_parser
import parser as parser_baby   # para leer el generador (gen) después de compilar

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
            print()
            parser_baby.gen.imprimir()               # fila de cuádruplos
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
    ("Variable doblemente declarada", "error_variable_doble.baby", False),
    ("Variable no declarada", "error_variable_no_declarada.baby", False),
    ("Función doblemente declarada", "error_funcion_doble.baby", False),
    ("Cuádruplos de expresiones y estatutos lineales", "cuadruplos.baby", True),
    ("Precedencia y paréntesis", "precedencia.baby", True),
    ("Asignar float a int", "error_tipo_asignacion.baby", False),
    ("Imprimir una comparación", "error_imprimir_comparacion.baby", False),
    ("If, if-else e if anidado", "if_else.baby", True),
    ("While con if adentro", "ciclo.baby", True),
]


def runtests():

    passed = 0
    for nombre, archivo, debe_pasar in cases:
        if test(nombre, archivo, debe_pasar):
            passed += 1

    print(f"Pruebas: {passed}/{len(cases)} dieron el resultado esperado")


def correr_uno(archivo):
    # acepta "precedencia", "precedencia.baby" o "tests/precedencia.baby"
    archivo = Path(archivo).name
    if not archivo.endswith(".baby"):
        archivo += ".baby"
    if not Path("tests", archivo).exists():
        print(f"No existe el archivo tests/{archivo}")
        return
    for nombre, archivo_caso, debe_pasar in cases:
        if archivo_caso == archivo:
            test(nombre, archivo, debe_pasar)
            return
    # si no está en la lista de casos, se asume que debe pasar
    test(archivo, archivo, True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # python3 tests.py precedencia    -> corre solo esa prueba (o varias)
        for archivo in sys.argv[1:]:
            correr_uno(archivo)
    else:
        # python3 tests.py                -> corre todas las pruebas
        runtests()
