
import ply.yacc as yacc

from lexer import tokens
from semantica.directorio_funciones import DirectorioFunciones
from semantica.generador import GeneradorCuadruplos
from semantica.errores import error_semantico

dir_func = None   # el directorio de funcones se inicializa cuando se encuentra la palabra reservada "program"
gen = None        # generador de cuádruplos se crea en "program"

start = 'programa'


class ErrorSintactico(Exception):
    pass


def p_programa(p):
    'programa : prog_head FINISHDOT listvars listfuncs main_palabra body END'
    gen.fin_programa()                         # cuádruplo END
    dir_func.terminar_programa()               # se guardan los recursos del programa


def p_main_palabra(p):
    'main_palabra : MAIN'
    dir_func.Direcciones.reiniciar_locales()   # main empieza sus temporales desde la primera dirección
    gen.inicio_main()                          # se llena el GOTO main del inicio


def p_prog_head(p):
    'prog_head : program_palabra ID'
    dir_func.agregar_programa(p[2])


def p_program_palabra(p):
    'program_palabra : PROGRAM'
    global dir_func, gen
    dir_func = DirectorioFunciones()
    gen = GeneradorCuadruplos(dir_func.Direcciones) 
    gen.inicio_programa()                      # GOTO main (destino pendiente)


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
    'funcs : func_head OPENPAR paramslist CLOSEPAR func_vars body CLOSEBRACKET FINISHDOT'
    gen.fin_funcion()                          # cuádruplo ENDFUNC
    dir_func.terminar_funcion()                # valida el return, guarda recursos y borra la tabla


def p_func_vars(p):
    'func_vars : OPENBRACKET listvars'
    dir_func.funcion_actual()['inicio'] = gen.cont()   # aquí empieza el código de la función


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


def p_statement_call(p):
    'statement : call FINISHDOT'
    nombre, funcion, linea = p[1]
    if funcion['tipo'] != 'void':
        error_semantico(f"la función '{nombre}' regresa un valor y debe usarse en una expresión", linea)


def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | printstatement
                 | readstatement
                 | returnstatement
                 | OPENBRACKET liststatement CLOSEBRACKET'''


def p_assign(p):
    'assign : ID ASSIGNOP expression FINISHDOT'
    var = dir_func.buscar_variable(p[1], p.lineno(1))
    gen.asignar(var['direccion'], var['tipo'], p.lineno(1))  


def p_condition(p):
    'condition : if_cond statement elsepart FINISHDOT'
    gen.fin_if()                               # llenar el último salto pendiente


def p_if_cond(p):
    'if_cond : IF OPENPAR expression CLOSEPAR'
    gen.gotof('if', p.lineno(1))               # GOTOF con destino pendiente


def p_elsepart(p):
    '''elsepart : else_palabra statement
                | empty'''


def p_else_palabra(p):
    'else_palabra : ELSE'
    gen.inicio_else()                          # GOTO al final y llenar el GOTOF


def p_cycle(p):
    'cycle : while_cond DO statement FINISHDOT'
    gen.fin_while()                            # GOTO de regreso y llenar el GOTOF


def p_while_cond(p):
    'while_cond : while_palabra OPENPAR expression CLOSEPAR'
    gen.gotof('while', p.lineno(1))            # GOTOF con destino pendiente


def p_while_palabra(p):
    'while_palabra : WHILE'
    gen.inicio_while()                         # guardar dónde empieza la condición
    p.set_lineno(0, p.lineno(1))


def p_printstatement(p):
    'printstatement : PRINT OPENPAR printlist CLOSEPAR FINISHDOT'


def p_printlist(p):
    '''printlist : printelem
                 | printlist REPEATDOT printelem'''


def p_printelem_exp(p):
    'printelem : expression'
    gen.imprimir_expresion(p.lexer.lineno)     # PRINT del resultado de la expresión


def p_printelem_str(p):
    'printelem : CTE_STRING'
    gen.imprimir_letrero(p[1])                 # PRINT del letrero


def p_readstatement(p):
    'readstatement : READ OPENPAR ID CLOSEPAR FINISHDOT'
    var = dir_func.buscar_variable(p[3], p.lineno(3))
    gen.leer(var['direccion'])                 # cuádruplo READ


def p_returnstatement(p):
    'returnstatement : RETURN expression FINISHDOT'
    if dir_func.en_programa():
        error_semantico("return solo puede usarse dentro de una función", p.lineno(1))
    funcion = dir_func.funcion_actual()
    if funcion['tipo'] == 'void':
        error_semantico(f"la función '{dir_func.actual}' es void y no puede tener return", p.lineno(1))
    gen.regresar(funcion['tipo'], funcion['retorno'], p.lineno(1))
    funcion['tiene_return'] = True


# ===================== Expresiones =====================
# Un nivel por precedencia: expression (> < !=), exp (+ -), term (* /), factor.
# La recursión izquierda (exp : exp + term) agrupa de izquierda a derecha.

def p_expression(p):
    '''expression : exp
                  | exp op_rel exp'''
    if len(p) == 4:
        linea = p.lineno(2)       # línea del operador
    else:
        linea = None              # no hay operador
    gen.generar_si(('>', '<', '!='), linea)   #  si arriba hay un relacional se genera


def p_op_rel(p):
    'op_rel : RELOPERATOR'
    gen.agregar_operador(p[1])                
    p.set_lineno(0, p.lineno(1))


def p_exp(p):
    '''exp : term
           | exp op_exp term'''
    if len(p) == 4:
        linea = p.lineno(2)       # línea del operador
    else:
        linea = None              # no hay operador
    gen.generar_si(('+', '-'), linea)          


def p_op_exp(p):
    'op_exp : EXPOPERATOR'
    gen.agregar_operador(p[1])                 
    p.set_lineno(0, p.lineno(1))


def p_term(p):
    '''term : factor
            | term op_term factor'''
    if len(p) == 4:
        linea = p.lineno(2)       # línea del operador
    else:
        linea = None              # no hay operador
    gen.generar_si(('*', '/'), linea)         


def p_op_term(p):
    'op_term : TERMOPERATOR'
    gen.agregar_operador(p[1])                
    p.set_lineno(0, p.lineno(1))


def p_factor(p):
    '''factor : abre_par expression CLOSEPAR
              | idorcte
              | EXPOPERATOR idorcte'''
    if len(p) == 4:
        gen.POper.pop()                        # sacar fondo falso
    elif len(p) == 3 and p[1] == '-':
        gen.negar(p.lineno(1))                


def p_factor_call(p):
    'factor : call'
    nombre, funcion, linea = p[1]
    if funcion['tipo'] == 'void':
        error_semantico(f"la función '{nombre}' es void y no se puede usar en una expresión", linea)
    gen.valor_llamada(funcion)                 # = global de la función -> temporal


def p_abre_par(p):
    'abre_par : OPENPAR'
    gen.agregar_operador('(')                  # poner fondo falso


def p_idorcte_id(p):
    'idorcte : ID'
    var = dir_func.buscar_variable(p[1], p.lineno(1))
    gen.agregar_operando(var['direccion'], var['tipo']) 


def p_idorcte_cte(p):
    'idorcte : cte'


def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
    if p.slice[1].type == 'CTE_INT':
        tipo = 'int'
    else:
        tipo = 'float'
    gen.agregar_constante(p[1], tipo)          # se mete la dirección de la constante


def p_call(p):
    '''call : call_head arglist CLOSEPAR
            | call_head CLOSEPAR'''
    nombre, funcion = gen.fin_llamada(p.lineno(1))   # valida número de argumentos y GOSUB
    p[0] = (nombre, funcion, p.lineno(1))


def p_call_head(p):
    'call_head : ID OPENPAR'
    funcion = dir_func.buscar_funcion(p[1], p.lineno(1))   # la función debe existir
    gen.inicio_llamada(p[1], funcion)                       # ERA y fondo falso
    p.set_lineno(0, p.lineno(1))


def p_arglist(p):
    '''arglist : arg
               | arglist REPEATDOT arg'''


def p_arg(p):
    'arg : expression'
    gen.argumento(p.lexer.lineno)              # valida el tipo y genera PARAM


def p_empty(p):
    'empty :'


# ===================== Errores =====================

def p_error(t):
    if t is None:
        raise ErrorSintactico("Error sintáctico: el archivo terminó antes de tiempo")
    raise ErrorSintactico(f"Error sintáctico en línea {t.lineno}: no se esperaba '{t.value}'")


def nuevo_parser():
    return yacc.yacc()
