

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
        res = self.tabla.get((izq, der), {}).get(op, ERROR)
        if res == ERROR:
            print(f"Error semántico: operación {izq} {op} {der} no permitida")
        return res


cubo = CuboSemantico()