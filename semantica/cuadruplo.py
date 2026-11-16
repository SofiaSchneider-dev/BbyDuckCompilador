VACIO = -1   # para los espacios del cuádruplo que no se usan


class Cuadruplo:
    """
    operador:  la operación ('+', '-', '*', '/', '>', '<', '!=', '=', 'PRINT', 'READ')
    izq:       dirección del operando izquierdo
    der:       dirección del operando derecho
    resultado: dirección donde se guarda el resultado
    """

    def __init__(self, operador, izq=VACIO, der=VACIO, resultado=VACIO):
        self.operador = operador
        self.izq = izq
        self.der = der
        self.resultado = resultado

    def __str__(self):
        # ('+', 1000, 1001, 9000)
        return str((self.operador, self.izq, self.der, self.resultado))


def imprimir_cuadruplos(fila):
    print("Cuádruplos generados:")
    for i, cuadruplo in enumerate(fila.elementos):
        print(f"{i}: {cuadruplo}")
