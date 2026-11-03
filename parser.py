
import ply.yacc as yacc

from lexer import tokens

start = 'programa'


class ErrorSintactico(Exception):
    pass


def p_programa(p):
    'programa : PROGRAM ID FINISHDOT listvars listfuncs MAIN body END'


def p_listvars(p):
    '''listvars : VAR vardecks
                | empty'''


def p_vardecks(p):
    '''vardecks : vardeck
                | vardecks vardeck'''


def p_vardeck(p):
    'vardeck : idlist TYPEASSIGNDOT type FINISHDOT'


def p_idlist(p):
    '''idlist : ID
              | idlist REPEATDOT ID'''


def p_type(p):
    '''type : INT
            | FLOAT'''


# ===================== Funciones =====================

def p_listfuncs(p):
    '''listfuncs : listfuncs funcs
                 | empty'''


def p_funcs(p):
    'funcs : functype ID OPENPAR paramslist CLOSEPAR OPENBRACKET listvars body CLOSEBRACKET FINISHDOT'


def p_functype(p):
    '''functype : VOID
                | type'''


def p_paramslist(p):
    '''paramslist : params
                  | empty'''


def p_params(p):
    '''params : parameter
              | params REPEATDOT parameter'''


def p_parameter(p):
    'parameter : ID TYPEASSIGNDOT type'


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
              | EXPOPERATOR idorcte
              | cte
              | ID
              | call'''


def p_idorcte(p):
    '''idorcte : ID
               | cte'''


def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''


def p_call(p):
    '''call : ID OPENPAR arglist CLOSEPAR
            | ID OPENPAR CLOSEPAR'''


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
