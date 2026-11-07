
import ply.yacc as yacc

from lexer import tokens
from semantica.directorio_funciones import DirectorioFunciones

dir_func = None   # el directorio de funcones se inicializa cuando se encuentra la palabra reservada "program"

start = 'programa'


class ErrorSintactico(Exception):
    pass


def p_programa(p):
    'programa : prog_head FINISHDOT listvars listfuncs MAIN body END'


def p_prog_head(p):
    'prog_head : program_palabra ID'
    dir_func.agregar_programa(p[2])


def p_program_palabra(p):
    'program_palabra : PROGRAM'
    global dir_func
    dir_func = DirectorioFunciones()


def p_listvars(p):
    '''listvars : var_palabra vardecks
                | empty'''


def p_var_palabra(p):
    'var_palabra : VAR'
    dir_func.crear_tabla_variables()


def p_vardecks(p):
    '''vardecks : vardeck
                | vardecks vardeck'''


def p_vardeck(p):
    'vardeck : idlist TYPEASSIGNDOT type FINISHDOT'
    dir_func.declarar_variables(p[1], p[3])


def p_idlist(p):
    '''idlist : ID
              | idlist REPEATDOT ID'''
    if len(p) == 2:
        p[0] = [(p[1], p.lineno(1))]
    else:
        p[0] = p[1] + [(p[3], p.lineno(3))]


def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]


# ===================== Funciones =====================

def p_listfuncs(p):
    '''listfuncs : listfuncs funcs
                 | empty'''


def p_funcs(p):
    'funcs : func_head OPENPAR paramslist CLOSEPAR OPENBRACKET listvars body CLOSEBRACKET FINISHDOT'
    dir_func.terminar_funcion()


def p_func_head(p):
    'func_head : functype ID'
    dir_func.agregar_funcion(p[2], p[1], p.lineno(2))


def p_functype(p):
    '''functype : VOID
                | type'''
    p[0] = p[1]


def p_paramslist(p):
    '''paramslist : params
                  | empty'''


def p_params(p):
    '''params : parameter
              | params REPEATDOT parameter'''


def p_parameter(p):
    'parameter : ID TYPEASSIGNDOT type'
    dir_func.agregar_parametro(p[1], p[3], p.lineno(1))


# ===================== Estatutos =====================

def p_body(p):
    'body : OPENBRACE liststatement CLOSEBRACE'


def p_liststatement(p):
    '''liststatement : liststatement statement
                     | empty'''


def p_statement(p):
    '''statement : assign
                 | call FINISHDOT
                 | condition
                 | cycle
                 | printstatement
                 | readstatement
                 | returnstatement
                 | OPENBRACKET liststatement CLOSEBRACKET'''


def p_assign(p):
    'assign : ID ASSIGNOP expression FINISHDOT'
    dir_func.buscar_variable(p[1], p.lineno(1))


def p_condition(p):
    'condition : IF OPENPAR expression CLOSEPAR statement elsepart FINISHDOT'


def p_elsepart(p):
    '''elsepart : ELSE statement
                | empty'''


def p_cycle(p):
    'cycle : WHILE OPENPAR expression CLOSEPAR DO statement FINISHDOT'


def p_printstatement(p):
    'printstatement : PRINT OPENPAR printlist CLOSEPAR FINISHDOT'


def p_printlist(p):
    '''printlist : printelem
                 | printlist REPEATDOT printelem'''


def p_printelem(p):
    '''printelem : expression
                 | CTE_STRING'''


def p_readstatement(p):
    'readstatement : READ OPENPAR ID CLOSEPAR FINISHDOT'
    dir_func.buscar_variable(p[3], p.lineno(3))


def p_returnstatement(p):
    'returnstatement : RETURN expression FINISHDOT'


# ===================== Expresiones =====================
# Un nivel por precedencia: expression (> < !=), exp (+ -), term (* /), factor.
# La recursión izquierda (exp : exp + term) agrupa de izquierda a derecha.

def p_expression(p):
    '''expression : exp
                  | exp RELOPERATOR exp'''


def p_exp(p):
    '''exp : term
           | exp EXPOPERATOR term'''


def p_term(p):
    '''term : factor
            | term TERMOPERATOR factor'''


def p_factor(p):
    '''factor : OPENPAR expression CLOSEPAR
              | idorcte
              | EXPOPERATOR idorcte
              | call'''


def p_idorcte_id(p):
    'idorcte : ID'
    dir_func.buscar_variable(p[1], p.lineno(1)) 
    #buscar variable en la expresion


def p_idorcte_cte(p):
    'idorcte : cte'


def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''


def p_call(p):
    '''call : ID OPENPAR arglist CLOSEPAR
            | ID OPENPAR CLOSEPAR'''
    dir_func.buscar_funcion(p[1], p.lineno(1))


def p_arglist(p):
    '''arglist : expression
               | arglist REPEATDOT expression'''


def p_empty(p):
    'empty :'


# ===================== Errores =====================

def p_error(t):
    if t is None:
        raise ErrorSintactico("Error sintáctico: el archivo terminó antes de tiempo")
    raise ErrorSintactico(f"Error sintáctico en línea {t.lineno}: no se esperaba '{t.value}'")


def nuevo_parser():
    return yacc.yacc()
