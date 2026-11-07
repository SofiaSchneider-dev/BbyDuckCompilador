
class TablaVariables:
    """Tabla de variables, el programa (variables globales) o una función (serían sus parámetros y variables locales)
    Key: nombre de la variable
    value: {'tipo': .. 'direccion': ..}
    """

    def __init__(self):
        self.variables = {}

    def existe(self, nombre):
        return nombre in self.variables

    def agregar(self, nombre, tipo, direccion):
        self.variables[nombre] = {'tipo': tipo, 'direccion': direccion}

    def buscar(self, nombre):
        """Regresa {'tipo', 'direccion'} o si no está en esta tabla."""
        return self.variables.get(nombre)


    def imprimir(self, titulo):
        print(f"  Tabla de variables de {titulo}:")
        for nombre, var in self.variables.items():
            print(f"    {nombre}: {var['tipo']}, dirección {var['direccion']}")
