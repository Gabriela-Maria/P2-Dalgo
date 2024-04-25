import sys

## CLASES 


class Vertice:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga
        self.pareja = None
    
    def add_pareja(self, vertice):
        self.pareja = vertice

    def es_opuesto(self, vertice):
        return self.masa == vertice.masa and self.carga != vertice.carga  

    def __repr__(self):
        tipo = "fundamental" if self.pareja is not None else "libre" # esto es solo para imprimirlo  con repr, se puede borrar
        return f"Vertice(masa={self.masa}, carga={self.carga}), tipo={tipo}"

    def __eq__(self, other):
        # Compara si otro objeto de 'Vertice' es igual a este.
        if not isinstance(other, Vertice) or (self.pareja is None and other.pareja is not None) or (self.pareja is not None and other.pareja is None):
            # No es igual si 'other' no es una instancia de Vertice
            return False
        
        elif self.pareja is None and other.pareja is None:
            return self.masa == other.masa and self.carga == other.carga
        
        else:
            return self.masa == other.masa and self.carga == other.carga \
                and self.pareja.masa == other.pareja.masa and self.pareja.carga == other.pareja.carga

    def __hash__(self):
        # Devuelve un número único para cada objeto de 'Vertice'.
        return hash((self.masa, self.carga))
    
class Conexion:
    def __init__(self, origen, destino, costo):
        self.origen = origen
        self.destino = destino
        self.costo=costo
        self.tipo = ""
    def get_costo (self, vertice1, vertice2):
        if (vertice1 == self.origen or vertice1 == self.destino) and (vertice2 == self.origen or vertice2 == self.destino):
            return self.costo

    def __repr__(self):
        return f"Conexion(origen={self.origen}, destino={self.destino}, costo={self.costo})"  
    
 
    
class Grafo:
    def __init__(self):
        self.vertices = []
        self.conexiones = []
        self.matriz_ady=[]
        self.diccionario_indices = {}
    def add_conexion(self, conexion):
        self.conexiones.append(conexion)
        if conexion.origen not in self.vertices:
            self.vertices.append(conexion.origen)
        if conexion.destino not in self.vertices:
            self.vertices.append(conexion.destino)          

    def add_vertice(self,vertice):
        self.vertices.append(vertice)          

    def crear_matriz_ady(self):
        self.matriz_ady = [[0] * len(self.vertices) for _ in range(len(self.vertices))]  # Inicializa la matriz de adyacencia con ceros
        count = 0
        for vertice_f in self.vertices:
            self.diccionario_indices[vertice_f] = count
            count +=1
        for conexion in self.conexiones:
            for indice in self.diccionario_indices.keys():
                v1 = self.diccionario_indices[conexion.origen]
                v2 = self.diccionario_indices[conexion.destino]
                if conexion.origen == indice and self.matriz_ady[v1][v2] == 0:
                    self.matriz_ady[v1][v2] = conexion.costo 
                if conexion.destino == indice and self.matriz_ady[v2][v1] == 0:
                    self.matriz_ady[v2][v1] = conexion.costo 

        return self.matriz_ady, self.diccionario_indices

    def determinar_si_se_puede(self) -> bool:
        conteo  = {}
        impares = 0
        for conexion in self.conexiones:
            origen = str(conexion.origen.masa) + str(conexion.origen.carga)
            destino = str(conexion.destino.masa)+ str(conexion.destino.carga)
            if  origen not in conteo.keys():
                conteo[origen] = 0
            elif origen in conteo.keys():
                conteo[origen] +=1
            
            if destino not in conteo.keys():
                conteo[destino] = 0
            elif destino in conteo.keys():
                conteo[destino] +=1
        for vertice in conteo:
            if conteo[vertice]%2 != 0:
                impares +=1
        if impares > 2 or impares == 1:
            return False
        return True

    def __repr__(self):
        return f"Vertices: \n" + "\n".join([str(vertice) for vertice in self.vertices]) + "\n" \
                + "Conexiones: \n" + "\n".join([str(conexion) for conexion in self.conexiones]) + "\n"


class Caso:
    def __init__(self, case_id, n, w1, w2, lineas, output_file):
        self.case_id = case_id
        self.n = n
        self.w1 = w1
        self.w2 = w2
        self.lineas = lineas
        self.output_file = output_file
        
        self.grafo, self.vertices_fundamentales = self.cargar_grafo(lineas)
        ################################################################################# DETERMINA SI SE PUEDE HACER O NO :)
        rpsta = self.grafo.determinar_si_se_puede()
        if rpsta == False:
            self.escribir_resultado("NO SE PUEDE", output_file)
        else:
            self.grafo, self.vertices_libres = self.grafo_vertices_opuestos(self.grafo)
            
            self.grafo_completo = self.crear_grafo_completo(self.grafo)
            self.matriz_grafo, self.diccionario_indices = self.grafo_completo.crear_matriz_ady()  # Agrega los paréntesis para invocar el método y captura los valores devueltos
    
            print("Matriz de Adyacencia:")
            print (self.matriz_grafo)
            
            print("Diccionario de Índices:")
            print(self.diccionario_indices)   
                    
            self.escribir_resultado(self.grafo_completo, output_file)

            camino_minimo, costo_minimo = self.camino_minimo_vertices_fundamentales()
            print(f"El costo minimo es {costo_minimo}")
            print(f"El camino minimo es {camino_minimo}")
            
    def calcular_costo(self, vertice1, vertice2):
        return (1 + abs(vertice1.masa-vertice2.masa) % self.w1) if (vertice1.carga == vertice2.carga) else (self.w2 - abs(vertice1.masa-vertice2.masa) % self.w2)
    
    def cargar_grafo(self, lineas):
        index = 0
        cant_casos = self.n
        vertices_fundamentales = []
        grafo = Grafo()
        for _ in range(cant_casos):
            origen, destino = map(int, lineas[index].split())
            
            masa_origen = abs(origen)
            carga_origen = "-" if origen < 0 else "+"
            origen = Vertice(masa_origen,carga_origen)
            masa_destino = abs(destino)
            carga_destino = "-" if destino < 0 else "+"
            destino = Vertice(masa_destino,carga_destino)
            
            origen.add_pareja(destino)
            destino.add_pareja(origen)
            vertices_fundamentales.append(origen)
            vertices_fundamentales.append(destino)
                    
            # Costo infinito
            costo =  sys.maxsize
            conexion = Conexion(origen, destino,costo)
            grafo.add_conexion(conexion)
            index += 1
            
        return grafo, vertices_fundamentales

    def grafo_vertices_opuestos(self, grafo): #crear un grafo conectado para hacerle dijkstra n veces
        original_vertices = set(grafo.vertices)
        vertices_libres = []
        for vertice in original_vertices:
            carga_opuesta = "-" if vertice.carga == "+" else  "+"
            vertice_opuesto = Vertice(vertice.masa, carga_opuesta)
            vertices_libres.append(vertice_opuesto)
            if vertice_opuesto not in original_vertices and vertice_opuesto not in grafo.vertices:
                grafo.add_vertice(vertice_opuesto)
        return grafo, vertices_libres
    
    
    def crear_grafo_completo(self, grafo):
        # Vamos a conectar todos los vertices fundamentales con cada vertice libre, pero no se pueden conectar vertices con la misma masa. 
        for vertice_fund in self.vertices_fundamentales:
            for vertice_libre in self.vertices_libres:
                if vertice_fund.masa != vertice_libre.masa:
                    costo = self.calcular_costo(vertice_fund, vertice_libre)
                    conexion = Conexion(vertice_fund, vertice_libre, costo)
                    grafo.add_conexion(conexion)
        
        return grafo
    
    def camino_minimo_vertices_fundamentales(self):
        # Ahora vamos a hacer dijkstra para cada vertice fundamental y nos quedamos con el costo minimo
        costo_minimo = sys.maxsize
        for vertice_source in self.vertices_fundamentales:
            vertice_destino = None 
            for vertice_libre in self.vertices_libres:
                if vertice_source.es_opuesto(vertice_libre):
                    vertice_destino = vertice_libre
                    break
                
            camino_minimo, costo = self.dijkstra(vertice_source, vertice_destino)
            costo_minimo = min(costo, costo_minimo)
        return camino_minimo, costo_minimo
            
            
            
            
    # ESTO TOCA CAMBIARLO XD, TAMBIEN QUEREMOS PARA ESTO LA MATRIZ DE ADYACENCIAS         
    def dijkstra(self, vertice_source, vertice_destino):
        # Dijkstra, retorna el camino mínimo y el costo mínimo
        distancias = {vertice: sys.maxsize for vertice in self.grafo.vertices}
        distancias[vertice_source] = 0
        predecesores = {vertice: None for vertice in self.grafo.vertices}
        visitados = set()
        
        while len(visitados) < len(self.grafo.vertices):
            # Elegir el vértice no visitado con la distancia más corta
            vertice_actual = min((v for v in self.grafo.vertices if v not in visitados), key=lambda x: distancias[x])
            visitados.add(vertice_actual)
            
            # Considerar todas las conexiones desde el vértice actual
            for conexion in self.grafo.conexiones:
                if conexion.origen == vertice_actual:
                    if distancias[conexion.destino] > distancias[vertice_actual] + conexion.costo:
                        distancias[conexion.destino] = distancias[vertice_actual] + conexion.costo
                        predecesores[conexion.destino] = vertice_actual
                elif conexion.destino == vertice_actual:
                    if distancias[conexion.origen] > distancias[vertice_actual] + conexion.costo:
                        distancias[conexion.origen] = distancias[vertice_actual] + conexion.costo
                        predecesores[conexion.origen] = vertice_actual

        # Reconstruir el camino mínimo desde el vértice de destino al de origen
        camino = []
        step = vertice_destino
        if predecesores[step] is not None or step == vertice_source:
            while step is not None:
                camino.append(step)
                step = predecesores[step]
            camino.reverse()  # Invertir para obtener el camino desde el origen al destino

        return camino, distancias[vertice_destino]
    
    def escribir_camino_minimo(self, distancias, output_file):
        # Escribe el camino minimo en el archivo de salida
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {distancias}\n")
        print(f"Se escribio en el archivo P2.out para el caso {self.case_id}")
        
    
    def escribir_resultado(self, result, output_file):
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {result}\n")

        print (f"Se escribio en el archivo P2.out para el caso {self.case_id}")



## RESUELVE TODOO
    
def resolver_casos( input_file, output_file):
    
    with open(input_file, 'r') as f:
        data = f.read()
        
    # Clean out file
    with open(output_file, 'w') as f:
        f.write("")
        
    lineas = data.strip().split("\n") # divide todas las lineas si hay un enter
    index = 0
    cant_casos = int(lineas[index]) #saca la cantidad de casos
    index += 1 #empieza a contar a partir de la segunda linea
    
    case_count = 0
    for _ in range(cant_casos):
        n, w1, w2 = map(int, lineas[index].split())
        index += 1
        case = lineas[index:index+n]
        index += n
        caso_actual = Caso(case_count, n, w1, w2, case, output_file)
        case_count += 1
         # Esto toca quitarlo ,es solo para mirar solo el primer caso jeje

        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Entradas esperadas: python script.py archivo_entrada.in archivo_salida.out\nIntente otravez")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    
    #hay que cambiar esto por el resultado q queramos
    resolver_casos(input_file, output_file)

##para probarlo hacerlo desde la terminal
## cuando este en P2-Dalgo:
#   python a compilar |  archivo in  |    archivo out
#   python P2.py      |      P2.in   |      P2.out