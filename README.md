# BabyDuck-Compiler

Compilador para el lenguaje **Baby Duck**


## Requisitos

- Python 3.8 o mayor

PLY ya viene incluido en la carpeta `ply/`, así que no hay que instalar nada más.

## Cómo probarlo

```bash
python3 tests.py
```

Corre todos los programas de `tests/` e indica si cada uno pasó o falló como se esperaba.

## Estructura

- `lexer.py`: tokens y sus expresiones regulares (scanner)
- `parser.py`: reglas gramaticales (parser LALR(1))
- `tests.py`: pruebas del scanner y el parser
- `tests/`: programas de prueba, correctos y con errores
- `ply/`: librería PLY