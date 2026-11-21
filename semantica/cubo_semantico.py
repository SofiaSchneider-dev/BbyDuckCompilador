

INT, FLOAT, BOOL, ERROR = 'int', 'float', 'bool', 'error'

class CuboSemantico:
    def __init__(self):
        # ( izquierdo,  derecho) -> {tipo del resultado}
        self.tabla = {
            (INT, INT):     {'+': INT,   
                             '-': INT,   
                             '*': INT,   
                             '/': FLOAT,
                             '>': BOOL, 
                             '<': BOOL, 
                             '!=': BOOL, 
                             '=': INT},

            (INT, FLOAT):   {'+': FLOAT, 
                             '-': FLOAT, 
                             '*': FLOAT, 
                             '/': FLOAT,
                             '>': BOOL,  
                             '<': BOOL,  
                             '!=': BOOL},

            (FLOAT, INT):   {'+': FLOAT,
                            '-': FLOAT, 
                            '*': FLOAT, 
                            '/': FLOAT,
                             '>': BOOL,  
                             '<': BOOL,  
                             '!=': BOOL, 
                             '=': FLOAT},

            (FLOAT, FLOAT): {'+': FLOAT, 
                             '-': FLOAT, 
                             '*': FLOAT, 
                             '/': FLOAT,
                             '>': BOOL,  
                             '<': BOOL,  
                             '!=': BOOL, 
                             '=': FLOAT},
        }

    def resultado(self, izq, der, op):
        "Tipo del resultado o ERROR si no existe"
        if (izq, der) not in self.tabla:
            return ERROR                  # no existe esa combinación de tipos
        operadores = self.tabla[(izq, der)]
        if op not in operadores:
            return ERROR                  # ese operador no se puede usar con esos tipos
        return operadores[op]


cubo = CuboSemantico()