from collections import deque


class Pila:
    """Pila que se usa para POperadores, PilaOperandosy PTipos
    """

    def __init__(self):
        self.elementos = []

    def push(self, elemento):
        self.elementos.append(elemento) # se agrega arriba de la pila

    def pop(self):
        if self.vacia():
            raise Exception("Pila esta vacía")
        return self.elementos.pop()

    def top(self):
        if self.vacia():
            return None
        return self.elementos[-1]

    def vacia(self):
        return len(self.elementos) == 0



class Fila:
    """Fila para guardar los cuádruplos en el orden en que se generan.
    """

    def __init__(self):
        self.elementos = deque()

    def agregar(self, elemento):
        self.elementos.append(elemento) # se agrega al final de la fila

    def sacar(self):
        if self.vacia():
            raise Exception("Fila esta vacía")
        return self.elementos.popleft() #sacar el primero

    def vacia(self):
        return len(self.elementos) == 0
