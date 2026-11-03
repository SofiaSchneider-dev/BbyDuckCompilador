
import ply.lex as lex

# Palabras reservadas
reservadas = {
    'program': 'PROGRAM', 
    'main': 'MAIN', 
    'end': 'END', 
    'var': 'VAR',
    'int': 'INT', 
    'float': 'FLOAT',
    'void': 'VOID',
    'if': 'IF', 
    'else': 'ELSE', 
    'while': 'WHILE', 
    'do': 'DO',
    'print': 'PRINT', 
    'read': 'READ', 
    'return': 'RETURN',
}

tokens = [
    'ID', 
    'CTE_INT', 
    'CTE_FLOAT', 
    'CTE_STRING',
    'ASSIGNOP', 
    'EXPOPERATOR', 
    'TERMOPERATOR', 
    'RELOPERATOR',
    'FINISHDOT', 
    'REPEATDOT', 
    'TYPEASSIGNDOT',
    'OPENPAR', 
    'CLOSEPAR', 
    'OPENBRACE', 
    'CLOSEBRACE', 
    'OPENBRACKET', 
    'CLOSEBRACKET',
] + list(reservadas.values())

# ----- Operadores y símbolos -----
t_RELOPERATOR = r'!=|<|>'
t_ASSIGNOP = r'='
t_EXPOPERATOR = r'[+-]'
t_TERMOPERATOR = r'[*/]'
t_FINISHDOT = r';'
t_REPEATDOT = r','
t_TYPEASSIGNDOT = r':'
t_OPENPAR = r'\('
t_CLOSEPAR = r'\)'
t_OPENBRACE = r'\{'
t_CLOSEBRACE = r'\}'
t_OPENBRACKET = r'\['
t_CLOSEBRACKET = r'\]'

# Espacios y tabuladores se ignoran 
t_ignore = ' \t\r'


# ----- Constantes e ids -----
def t_CTE_FLOAT(t):
    r'(?:0|[1-9][0-9]*)\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CTE_INT(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9]+)*'
    t.type = reservadas.get(t.value, 'ID')
    return t


def t_CTE_STRING(t):
    r"'[^'\r\n]*'"
    t.value = t.value[1:-1]  # sin las comillas
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ----- Errores léxicos -----
errores = []


def t_error(t):
    errores.append(f"Error léxico en línea {t.lineno}: "
                   f"carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)


def nuevo_lexer():
    errores.clear()
    return lex.lex()
