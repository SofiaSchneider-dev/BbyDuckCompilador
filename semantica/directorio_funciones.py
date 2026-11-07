from semantica.direcciones import Direcciones
from semantica.tabla_variables import TablaVariables


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
                raise Exception(f"Error semántico en línea {linea}: "
                                f"la variable '{nombre}' ya está declarada")
            tabla.agregar(nombre, tipo, self.Direcciones.nueva_direccion(segmento, tipo))
            # agregar la variable a la tabla de variables de la función actual con tipo y direcci´øn nueva

    def buscar_variable(self, nombre, linea):
        # primero en la función actual, luego en las globales
        for alcance in (self.actual, self.programa):
            tabla = self.funciones[alcance]['tabla']
            if tabla is not None and tabla.existe(nombre):
                return tabla.buscar(nombre)
        raise Exception(f"Error semántico en línea {linea}: "
                        f"la variable '{nombre}' no está declarada")


    def agregar_funcion(self, nombre, tipo, linea):
        if nombre in self.funciones:
            # si ya está declarada como funcion o programa
            raise Exception(f"Error semántico en línea {linea}: "
                            f"el nombre '{nombre}' ya está declarado como función o programa")
        self.funciones[nombre] = {
            'tipo': tipo,      # void, int o float
            'tabla': None,     # su tabla de variables
            'params': [],      # tipos de los parámetros en orden
        }
        self.actual = nombre
        self.Direcciones.reiniciar_locales() # se reinician las direcciones locales  para esta nueva funcion
        self.crear_tabla_variables()   # sus parámetros van en esta tabla

    def agregar_parametro(self, nombre, tipo, linea):
        self.declarar_variables([(nombre, linea)], tipo) #agregar la variable 
        self.funcion_actual()['params'].append(tipo) # agregar el tipo del parametro 

    def terminar_funcion(self):
        self.funcion_actual()['tabla'] = None # se termina una funcion y se borra su tabla de variables 
        self.actual = self.programa

    def buscar_funcion(self, nombre, linea):
        if nombre not in self.funciones or nombre == self.programa:
            raise Exception(f"Error semántico en línea {linea}: "
                            f"la función '{nombre}' no está declarada")
        return self.funciones[nombre]


    def imprimir(self):
        print("Directorio de funciones:")
        for nombre, f in self.funciones.items():
            if nombre == self.programa:
                print(f"  {nombre}: programa")
            else:
                print(f"  {nombre}: {f['tipo']}, params {f['params']}")
            if f['tabla'] is not None:
                f['tabla'].imprimir(nombre)