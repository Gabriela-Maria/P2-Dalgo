import sys

## CLASES 
class Vertice:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga

    def __repr__(self):
        return f"Vertice(masa={self.masa}, carga={self.carga})"

class Conexion:
    def __init__(self, origen, destino, costo):
        self.origen = origen
        self.destino = destino
        self.costo=costo

    def __repr__(self):
        return f"Conexion(origen={self.origen}, destino={self.destino}, costo={self.costo})"   

## FUNCIONES    
def cargar_conexiones(data):
    lines = data.strip().split("\n") # divide todas las lineas si hay un enter
    index = 0
    num_cases = int(lines[index]) #saca la cantidad de casos
    index += 1 #empieza a contar a partir de la segunda linea
    all_cases = []
    
    for _ in range(num_cases):
        n, w1, w2 = map(int, lines[index].split())  # lee la linea del primer caso
        index += 1
        conexiones = []
        
        for _ in range(n):
            origen, destino = map(int, lines[index].split())

            masa_origen = abs(origen)
            carga_origen = "-" if masa_origen <0 else "+"
            origen = Vertice(masa_origen,carga_origen)

            masa_destino = abs(destino)
            carga_destino = "-" if masa_destino <0 else "+"
            destino = Vertice(masa_destino,carga_destino)

            costo =  (1 + abs(w1-w2) % w1) if (carga_origen == carga_destino) else (w2 - abs(w1-w2) % w2)

            conexion = Conexion(origen, destino,costo) # falta añadir el costo
            conexiones.append(conexion)
            index += 1
        
        all_cases.append(conexiones)
    
    return all_cases



# Example usage
if __name__ == "__main__":
    data = """  2
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
