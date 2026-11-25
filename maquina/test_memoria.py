# Pruebas de la clase Memoria
# Se corre desde la carpeta del proyecto con:  python3 maquina/test_memoria.py

from memoria import Memoria


def prueba(nombre, condicion):
    if condicion:
        print(f"✓ {nombre}")
        return True
    print(f"✗ {nombre}")
    return False


resultados = []

# escribir y leer un valor
m = Memoria('global')
m.escribir(1000, 5)
resultados.append(prueba("escribir y leer un int", m.leer(1000) == 5))

m.escribir(3000, 2.5)
resultados.append(prueba("escribir y leer un float", m.leer(3000) == 2.5))

# escribir otra vez en la misma dirección cambia el valor
m.escribir(1000, 7)
resultados.append(prueba("escribir de nuevo cambia el valor", m.leer(1000) == 7))

# leer una dirección que no tiene valor marca error
try:
    m.leer(1001)
    resultados.append(prueba("leer una dirección sin valor marca error", False))
except Exception as e:
    print(f"   mensaje: {e}")
    resultados.append(prueba("leer una dirección sin valor marca error", True))

# dos memorias distintas pueden tener la misma dirección con distinto valor (recursión)
llamada1 = Memoria('fact')
llamada2 = Memoria('fact')
llamada1.escribir(5000, 2)
llamada2.escribir(5000, 1)
resultados.append(prueba("dos memorias con la misma dirección no se mezclan",
                         llamada1.leer(5000) == 2 and llamada2.leer(5000) == 1))

# la memoria guarda su nombre
resultados.append(prueba("la memoria guarda su nombre", llamada1.nombre == 'fact'))

print()
m.imprimir()
print(f"\nPruebas: {sum(resultados)}/{len(resultados)} pasaron")
