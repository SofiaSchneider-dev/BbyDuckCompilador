from collections import defaultdict

# primera dirección de cada segmento: (segmento, tipo) -> dirección
RANGOS = {
    ('global', 'int'): 1000,
    ('global', 'float'): 3000,
    ('local', 'int'): 5000,
    ('local', 'float'): 7000,
}
TAMANO = 2000


class Direcciones:
    def __init__(self):
        # cuántas direcciones se han usado en cada segmento
        self.contadores = defaultdict(int)

    def nueva_direccion(self, segmento, tipo):
        llave = (segmento, tipo)
        if llave not in RANGOS:
            raise Exception(f"No existe el segmento {segmento} de tipo {tipo}")
        if self.contadores[llave] >= TAMANO:
            raise Exception(f"Ya no hay direcciones disponibles del segmento {segmento} de tipo {tipo}")
        direccion = RANGOS[llave] + self.contadores[llave]
        self.contadores[llave] += 1
        return direccion

    def reiniciar_locales(self):
        # cada función empieza sus locales desde la primera dirección
        for segmento, tipo in self.contadores:
            if segmento == 'local':
                self.contadores[(segmento, tipo)] = 0