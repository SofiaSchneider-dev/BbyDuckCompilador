from semantica.estructuras import Pila, Fila
from semantica.cuadruplo import Cuadruplo, imprimir_cuadruplos
from semantica.cubo_semantico import cubo, ERROR, BOOL
from semantica.tabla_constantes import TablaConstantes
from semantica.errores import error_semantico


class GeneradorCuadruplos:
    """
    POper:  pila de operadores pendientes
    PilaO:  pila de operandos pendientes (sus direcciones)
    PTipos: pila con el tipo de cada operando de PilaO
    fila:   fila con los cuádruplos generados en orden
    """

    def __init__(self, direcciones):
        self.POper = Pila()
        self.PilaO = Pila()
        self.PTipos = Pila()
        self.fila = Fila()
        self.PSaltos = Pila()                      # saltos pendientes (posiciones de cuádruplos por llenar)
        self.PLlamadas = Pila()                    # llamadas pendientes: función y número de argumento (k)
        self.direcciones = direcciones             
        self.constantes = TablaConstantes(direcciones)

    def imprimir(self):
        imprimir_cuadruplos(self.fila)


    def agregar_operando(self, direccion, tipo):
        self.PilaO.push(direccion)
        self.PTipos.push(tipo)

    def agregar_constante(self, valor, tipo):
        # una constante es un operando con su dirección de la tabla de constantes
        self.agregar_operando(self.constantes.obtener_direccion(valor, tipo), tipo)

    def agregar_operador(self, operador):
        self.POper.push(operador)


    def generar_si(self, operadores, linea=None):
        if self.POper.top() not in operadores:
            return
        der = self.PilaO.pop()
        tipo_der = self.PTipos.pop()
        izq = self.PilaO.pop()
        tipo_izq = self.PTipos.pop()
        operador = self.POper.pop()

        tipo = cubo.resultado(tipo_izq, tipo_der, operador)
        if tipo == ERROR:
            error_semantico(f"no se puede hacer {tipo_izq} {operador} {tipo_der}", linea)

        resultado = self.direcciones.nueva_direccion('temporal', tipo) 
        self.fila.agregar(Cuadruplo(operador, izq, der, resultado))
        self.agregar_operando(resultado, tipo)


    def negar(self, linea=None):
        # -A se traduce como 0 - A
        operando = self.PilaO.pop()            # A ya estaba en la pila
        tipo = self.PTipos.pop()
        self.agregar_constante(0, 'int')       # se mete el 0 como operando izquierdo
        self.agregar_operando(operando, tipo)  # A queda como operando derecho
        self.agregar_operador('-')
        self.generar_si(('-',), linea)         # se genera  - 0 A  -> temporal


    def asignar(self, direccion_var, tipo_var, linea=None):
        # x = expresión  ->  ('=', resultado de la expresión, -1, x)
        resultado = self.PilaO.pop()
        tipo = self.PTipos.pop()
        if cubo.resultado(tipo_var, tipo, '=') == ERROR:
            error_semantico(f"no se puede asignar {tipo} a una variable {tipo_var}", linea)
        self.fila.agregar(Cuadruplo('=', resultado, resultado=direccion_var))

    def imprimir_expresion(self, linea=None):
        # print(expresión)  ->  ('PRINT', -1, -1, resultado)
        resultado = self.PilaO.pop()
        tipo = self.PTipos.pop()
        if tipo == BOOL:
            error_semantico("no se puede imprimir una comparación", linea)
        self.fila.agregar(Cuadruplo('PRINT', resultado=resultado))

    def imprimir_letrero(self, texto):
        # print('hola')  ->  ('PRINT', -1, -1, dirección de la constante 'hola')
        direccion = self.constantes.obtener_direccion(texto, 'string')
        self.fila.agregar(Cuadruplo('PRINT', resultado=direccion))

    def leer(self, direccion_var):
        # read(x)  ->  ('READ', -1, -1, x)
        self.fila.agregar(Cuadruplo('READ', resultado=direccion_var))


    # ----- Saltos (if / else / while) -----

    def cont(self):
        # número del siguiente cuádruplo que se va a generar
        return len(self.fila.elementos)

    def rellenar(self, posicion, destino):
        # FILL: se llena el destino del salto que estaba pendiente
        self.fila.elementos[posicion].resultado = destino

    def gotof(self, estatuto, linea=None):
        # la condición debe ser bool; se genera GOTOF con el destino pendiente
        tipo = self.PTipos.pop()
        resultado = self.PilaO.pop()
        if tipo != BOOL:
            error_semantico(f"la condición del {estatuto} debe ser una comparación", linea)
        self.fila.agregar(Cuadruplo('GOTOF', resultado))
        self.PSaltos.push(self.cont() - 1)

    def inicio_else(self):
        # GOTO para saltarse el else (destino pendiente) y se llena el GOTOF hacia el else
        self.fila.agregar(Cuadruplo('GOTO'))
        falso = self.PSaltos.pop()
        self.PSaltos.push(self.cont() - 1)
        self.rellenar(falso, self.cont())

    def fin_if(self):
        # se llena el último salto pendiente del if con el cuádruplo que sigue
        fin = self.PSaltos.pop()
        self.rellenar(fin, self.cont())

    def inicio_while(self):
        # se guarda dónde empieza la condición, para regresar ahí
        self.PSaltos.push(self.cont())

    def fin_while(self):
        # GOTO de regreso a la condición y se llena el GOTOF para salir del ciclo
        fin = self.PSaltos.pop()
        regreso = self.PSaltos.pop()
        self.fila.agregar(Cuadruplo('GOTO', resultado=regreso))
        self.rellenar(fin, self.cont())


    # ----- Programa y funciones -----

    def inicio_programa(self):
        # el primer cuádruplo salta a main (destino pendiente)
        self.fila.agregar(Cuadruplo('GOTO'))
        self.PSaltos.push(self.cont() - 1)

    def inicio_main(self):
        # se llena el GOTO del inicio con el cuádruplo donde empieza main
        self.rellenar(self.PSaltos.pop(), self.cont())

    def regresar(self, tipo_funcion, direccion_retorno, linea=None):
        # return expresión  ->  ('RETURN', valor, -1, variable global de la función)
        valor = self.PilaO.pop()
        tipo = self.PTipos.pop()
        if cubo.resultado(tipo_funcion, tipo, '=') == ERROR:
            error_semantico(f"no se puede regresar {tipo} en una función {tipo_funcion}", linea)
        self.fila.agregar(Cuadruplo('RETURN', valor, resultado=direccion_retorno))

    def fin_funcion(self):
        self.fila.agregar(Cuadruplo('ENDFUNC'))

    def fin_programa(self):
        self.fila.agregar(Cuadruplo('END'))


    # ----- Llamadas a función -----

    def inicio_llamada(self, nombre, funcion):
        # ERA antes de evaluar los argumentos, y se empieza a contar los argumentos 
        self.fila.agregar(Cuadruplo('ERA', resultado=nombre))
        self.PLlamadas.push({'nombre': nombre, 'funcion': funcion, 'k': 0})
        self.agregar_operador('(')                 # fondo falso: los argumentos no se mezclan con la expresión de afuera

    def argumento(self, linea=None):
        # se saca el argumento, se valida contra el parámetro k y se genera PARAM
        llamada = self.PLlamadas.top()
        nombre = llamada['nombre']
        params = llamada['funcion']['params']
        k = llamada['k']
        argumento = self.PilaO.pop()
        tipo = self.PTipos.pop()
        if k >= len(params):
            error_semantico(f"la función '{nombre}' recibe {len(params)} argumento(s)", linea)
        if cubo.resultado(params[k], tipo, '=') == ERROR:
            error_semantico(f"el argumento {k + 1} de '{nombre}' debe ser {params[k]}, no {tipo}", linea)
        self.fila.agregar(Cuadruplo('PARAM', argumento, resultado=k + 1))
        llamada['k'] += 1

    def fin_llamada(self, linea=None):
        # se valida que no falten argumentos y se genera GOSUB
        llamada = self.PLlamadas.pop()
        nombre = llamada['nombre']
        funcion = llamada['funcion']
        if llamada['k'] != len(funcion['params']):
            error_semantico(f"la función '{nombre}' recibe {len(funcion['params'])} argumento(s), "
                            f"se mandaron {llamada['k']}", linea)
        self.POper.pop()                           # se saca el fondo falso
        self.fila.agregar(Cuadruplo('GOSUB', nombre, resultado=funcion['inicio']))
        return nombre, funcion

    def valor_llamada(self, funcion):
        # se copia el resultado de la variable global a un temporal (para no perderlo con otra llamada)
        tipo = funcion['tipo']
        temporal = self.direcciones.nueva_direccion('temporal', tipo)
        self.fila.agregar(Cuadruplo('=', funcion['retorno'], resultado=temporal))
        self.agregar_operando(temporal, tipo)
