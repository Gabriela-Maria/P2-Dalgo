import sys


class Atomo:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga

class Conexion:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        # falta agregar el atributo costo, calculado xd
    
def cargar_conexiones(data):
    lines = data.strip().split("\n")
    index = 0
    num_cases = int(lines[index])
    index += 1
    all_cases = []
    
    for _ in range(num_cases):
        n, w1, w2 = map(int, lines[index].split())  # lee la linea del primer caso
        print(n)
        index += 1
        conexiones = []
        
        for _ in range(n):
            origen, destino = map(int, lines[index].split())
            conexion = Conexion(origen, destino)
            conexiones.append(conexion)
            index += 1
        
        all_cases.append(conexiones)
    
    return all_cases

# Example usage
if __name__ == "__main__":
    data = """2
3 3 5
1 3
-6 3
1 7
3 2 3
1 2
-2 3
3 -4"""
    result = cargar_conexiones(data)
    for case_conexiones in result:
        print(case_conexiones)
