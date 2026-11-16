class TablaConstantes:
    """A cada constante se le da una sola dirección aunque aparezca varais veces

    Llave: (valor, tipo) por ejemplo (5, 'int') o ('hola', 'string')
    Valor: su dirección virtual
    """

    def __init__(self, direcciones):
        self.direcciones = direcciones   # el mismo objeto Direcciones del directorio
        self.constantes = {} 

    def obtener_direccion(self, valor, tipo):
        # la llave lleva el tipo porque en Python 5 es igual que 5.0
        llave = (valor, tipo)
        if llave not in self.constantes:
            self.constantes[llave] = self.direcciones.nueva_direccion('constante', tipo)
        return self.constantes[llave]

    def imprimir(self):
        print("Tabla de constantes:")
        for (valor, tipo), direccion in self.constantes.items():
            print(f"  {valor!r}: {tipo}, dirección {direccion}")
