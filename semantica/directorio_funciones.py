from semantica.direcciones import Direcciones
from semantica.tabla_variables import TablaVariables
from semantica.errores import error_semantico


class DirectorioFunciones:
    """Directorio de funciones: nombre y datos de la función o del programa
    cada entrada tiene su propia tabla de variables
    """

    def __init__(self):
        self.Direcciones = Direcciones()
        self.funciones = {}
        #lista de funciones
        self.programa = None  #noombre del programa
        self.actual = None     # nombre de la función actual o del programa

    def funcion_actual(self):
        return self.funciones[self.actual] # regresa el diccionario de la función actual

    def en_programa(self):
        return self.actual == self.programa # regresa True si la función actual es el programa


    def agregar_programa(self, nombre):
        self.funciones[nombre] = {'tipo': 'programa', 'tabla': None} # agrega el programa al directorio de funciones
        self.programa = nombre # nombre del programa
        self.actual = nombre # nombre de la función actual es el programa


    def crear_tabla_variables(self):
        # solo se crea si la función actual todavía no tiene una tabla
        if self.funcion_actual()['tabla'] is None:
            self.funcion_actual()['tabla'] = TablaVariables() #crear nueva tabla de variables para la función actual

    def declarar_variables(self, ids, tipo):
        tabla = self.funcion_actual()['tabla'] # obtener la tabla de variables de la función actual
        segmento = 'global' if self.en_programa() else 'local' # determinar el segmento de la direccion
        # en la que está según si estamos en el programa o en una función
        for nombre, linea in ids:
            if tabla.existe(nombre):
                error_semantico(f"la variable '{nombre}' ya está declarada", linea)
            tabla.agregar(nombre, tipo, self.Direcciones.nueva_direccion(segmento, tipo))
            # agregar la variable a la tabla de variables de la función actual con tipo y direcci´øn nueva

    def buscar_variable(self, nombre, linea):
        # primero en la función actual, luego en las globales
        for alcance in (self.actual, self.programa):
            tabla = self.funciones[alcance]['tabla']
            if tabla is not None and tabla.existe(nombre):
                return tabla.buscar(nombre)
        error_semantico(f"la variable '{nombre}' no está declarada", linea)


    def agregar_funcion(self, nombre, tipo, linea):
        if nombre in self.funciones:
            # si ya está declarada como funcion o programa
            error_semantico(f"el nombre '{nombre}' ya está declarado como función o programa", linea)
        direccion_retorno = None
        if tipo != 'void':
            # función no-void: una variable global con su nombre guarda el valor del return
            direccion_retorno = self.agregar_global_retorno(nombre, tipo, linea)
        self.funciones[nombre] = {
            'tipo': tipo,      # void, int o float
            'tabla': None,     # su tabla de variables
            'params': [],      # tipos de los parámetros en orden
            'param_dirs': [],  # direcciones de los parámetros en orden
            'inicio': None,    # cuádruplo donde empieza la función
            'recursos': {},    # cuántas locales y temporales usa, por tipo
            'retorno': direccion_retorno,  # dirección global donde se guarda el return
            'tiene_return': False,
            'linea': linea,
        }
        self.actual = nombre
        self.Direcciones.reiniciar_locales() # se reinician las direcciones locales  para esta nueva funcion
        self.crear_tabla_variables()   # sus parámetros van en esta tabla

    def agregar_parametro(self, nombre, tipo, linea):
        self.declarar_variables([(nombre, linea)], tipo) #agregar la variable 
        self.funcion_actual()['params'].append(tipo) # agregar el tipo del parametro 
        direccion = self.funcion_actual()['tabla'].buscar(nombre)['direccion']
        self.funcion_actual()['param_dirs'].append(direccion) # agregar la dirección del parámetro

    def agregar_global_retorno(self, nombre, tipo, linea):
        # se da de alta una variable global con el nombre de la función
        programa = self.funciones[self.programa]
        if programa['tabla'] is None:
            programa['tabla'] = TablaVariables()   # el programa no tenía var
        if programa['tabla'].existe(nombre):
            error_semantico(f"el nombre '{nombre}' ya está declarado como variable global", linea)
        direccion = self.Direcciones.nueva_direccion('global', tipo)
        programa['tabla'].agregar(nombre, tipo, direccion)
        return direccion

    def terminar_funcion(self):
        funcion = self.funcion_actual()
        if funcion['tipo'] != 'void' and not funcion['tiene_return']:
            error_semantico(f"la función '{self.actual}' debe tener return", funcion['linea'])
        # se guardan sus recursos antes de borrar la tabla y reiniciar las direcciones
        funcion['recursos'] = self.Direcciones.recursos(('local', 'temporal'))
        funcion['tabla'] = None # se termina una funcion y se borra su tabla de variables 
        self.actual = self.programa

    def terminar_programa(self):
        # recursos del programa: variables globales y temporales de main
        self.funciones[self.programa]['recursos'] = self.Direcciones.recursos(('global', 'temporal'))

    def buscar_funcion(self, nombre, linea):
        if nombre not in self.funciones or nombre == self.programa:
            error_semantico(f"la función '{nombre}' no está declarada", linea)
        return self.funciones[nombre]


    def imprimir(self):
        print("Directorio de funciones:")
        for nombre, f in self.funciones.items():
            if nombre == self.programa:
                print(f"  {nombre}: programa, recursos {f.get('recursos', {})}")
            else:
                print(f"  {nombre}: {f['tipo']}, params {f['params']}, inicio {f['inicio']}, "
                      f"retorno {f['retorno']}, recursos {f['recursos']}")
            if f['tabla'] is not None:
                f['tabla'].imprimir(nombre)