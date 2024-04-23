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
    
class Grafo:
    def __init__(self):
        self.vertices = []
        self.conexiones = []  

    def add_conexion(self, conexion):
        self.conexiones.append(conexion)
        if conexion.origen not in self.vertices:
            self.vertices.append(conexion.origen)
        if conexion.destino not in self.vertices:
            self.vertices.append(conexion.destino)          

    def add_conexion_opuesta(self):
        self          

    def __repr__(self):
        return f"Vertices: {(self.vertices)} , conexiones:{(self.conexiones)}"

## FUNCIONES PARTE 1
    
def cargar_conexiones(data):
    lineas = data.strip().split("\n") # divide todas las lineas si hay un enter
    index = 0
    cant_casos = int(lineas[index]) #saca la cantidad de casos
    index += 1 #empieza a contar a partir de la segunda linea
    all_cases = []
    
    for _ in range(cant_casos):
        n, w1, w2 = map(int, lineas[index].split())  # lee la linea del primer caso
        index += 1
        grafo = Grafo()
        
        for _ in range(n):
            origen, destino = map(int, lineas[index].split())

            masa_origen = abs(origen)
            carga_origen = "-" if origen < 0 else "+"
            origen = Vertice(masa_origen,carga_origen)

            masa_destino = abs(destino)
            carga_destino = "-" if destino < 0 else "+"
            destino = Vertice(masa_destino,carga_destino)

            costo =  (1 + abs(w1-w2) % w1) if (carga_origen == carga_destino) else (w2 - abs(w1-w2) % w2)

            conexion = Conexion(origen, destino,costo) 
            grafo.add_conexion(conexion)
            index += 1
        
        all_cases.append(grafo)
    
    return all_cases

def crear_grafo_vertices_opuestos(grafo): #crear un grafo conectado para hacerle dijkstra n veces
    nuevos_vertices = []
    original_vertices = set(grafo.vertices)
    for vertice in grafo.vertices:
        carga_opuesta = "-" if vertice.carga == "+" else  "+"
        vertice_opuesto = Vertice(vertice.masa, carga_opuesta)
        if vertice_opuesto not in original_vertices:
            nuevos_vertices.append(vertice_opuesto)
    vertices_sin_repetir = list(dict.fromkeys(nuevos_vertices, None))
    return vertices_sin_repetir



#dijkstra normal

#dijkstra grande

# metodo para crear el nuevo grafo

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
print(result)
for grafo in result:
    unique_vertices = crear_grafo_vertices_opuestos(grafo)
    print("Unique vertices with opposite charges added:")
    for vertex in unique_vertices:
        print(vertex,"vertice jeje")
