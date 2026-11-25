class Memoria:
    """Una memoria de ejecución: la global, la de constantes o la de una llamada a función.

    Llave: dirección virtual
    Valor: el valor que está guardado en esa dirección
    """

    def __init__(self, nombre):
        self.nombre = nombre      # para saber de quién es: 'global', 'constantes' o el nombre de la función
        self.valores = {}

    def escribir(self, direccion, valor):
        # se guarda o se cambia el valor de esa dirección
        self.valores[direccion] = valor

    def leer(self, direccion):
        # si la dirección todavía no tiene valor, la variable se usó sin asignarle nada
        if direccion not in self.valores:
            raise Exception(f"Error de ejecución: la dirección {direccion} no tiene valor "
                            f"(se usó una variable sin asignarle un valor)")
        return self.valores[direccion]

    def imprimir(self):
        print(f"Memoria {self.nombre}:")
        for direccion, valor in self.valores.items():
            print(f"  {direccion}: {valor!r}")
