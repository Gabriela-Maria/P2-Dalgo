from queue import Queue
import sys

## CLASES 


class Vertice:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga
        self.pareja = None
        self.tipo = "libre"
    
    def add_pareja(self, vertice):
        self.pareja = vertice
        self.tipo = "fundamental"
        
    def es_opuesto(self, vertice):
        return self.masa == vertice.masa and self.carga != vertice.carga  

    def __repr__(self):
        self.tipo = "fundamental" if self.pareja is not None else "libre" # esto es solo para imprimirlo  con repr, se puede borrar
        return f"Vertice(masa={self.masa}, carga={self.carga}), tipo={self.tipo}"

    def __eq__(self, other):
        if not isinstance(other, Vertice) or (self.pareja is None and other.pareja is not None) or (self.pareja is not None and other.pareja is None):
            return False
        
        elif self.pareja is None and other.pareja is None:
            return self.masa == other.masa and self.carga == other.carga
        
        else:
            return self.masa == other.masa and self.carga == other.carga \
                and self.pareja.masa == other.pareja.masa and self.pareja.carga == other.pareja.carga

    def __hash__(self):
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

    def vertices_fundamentales_repetidos(self):
        self.cuenta_vertices_fundamentales_dic ={}
        self.verticesf={}
        for vertice in self.vertices:
            entrada = str(vertice.masa) + str(vertice.carga)
            if entrada in self.cuenta_vertices_fundamentales_dic:
                self.cuenta_vertices_fundamentales_dic[entrada] += 1
                self.verticesf[entrada].append(vertice)
            elif entrada not in self.cuenta_vertices_fundamentales_dic.keys() and vertice.tipo == "fundamental":
                self.cuenta_vertices_fundamentales_dic[entrada] = 1
                self.verticesf[entrada]= [vertice]
        self.entradas_repetidas = []
        self.verticesf_repetidos = []
        for verticef in self.cuenta_vertices_fundamentales_dic.keys():
            if self.cuenta_vertices_fundamentales_dic[verticef] >= 2:
                self.entradas_repetidas.append(verticef)
        for verticef in self.entradas_repetidas:
            self.verticesf_repetidos.append(self.verticesf[verticef])
        return self.verticesf_repetidos

    def crear_matriz_ady(self):
        self.matriz_ady = [[0] * len(self.vertices) for _ in range(len(self.vertices))]
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
        #print (self.diccionario_indices)        

        return self.matriz_ady, self.diccionario_indices

    def determinar_si_se_puede_y_grafo_euleriano(self):
        conteo  = {}
        grafo_euleriano = {}
        #impares = 0
        for conexion in self.conexiones:
            origen = str(conexion.origen.masa) + str(conexion.origen.carga)
            destino = str(conexion.destino.masa)+ str(conexion.destino.carga)

            if  origen not in conteo.keys():
                conteo[origen] = 1
                grafo_euleriano[origen] = [destino]

            else:
                conteo[origen] +=1
                grafo_euleriano[origen].append(destino)

            if destino not in conteo.keys():
                conteo[destino] = 1
                grafo_euleriano[destino] = [origen]

            else:
                conteo[destino] +=1
                grafo_euleriano[destino].append(origen)

        # Verificar si el grafo es euleriano revisando el número de vértices con grado impar
        source = None
        impares = 0
        mayor_grado_impar = 0
        for key, val in conteo.items():
            if val % 2 != 0:
                impares +=1
                if val > mayor_grado_impar:
                    mayor_grado_impar = val
                    source = key

        # Tiene exactamente dos vértices de grado impar o ninguno
        if impares > 2: 
            return False, None, None # No es un grafo euleriano
        return True, grafo_euleriano, source  # Es un grafo euleriano, retorna el grafo y el vértice inicial posible

    def es_alcanzable_BFS(self, origen, destino, grafo_euleriano):
        if len(grafo_euleriano[origen]) > 0:
            visitados = set()
            visitados.add(origen)
            cola = Queue()
            cola.put(origen)
            while not cola.empty():
                actual = cola.get()
                if actual == destino:
                    return True
                for vecino in grafo_euleriano[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.put(vecino)
        else:
            return True

    def encontrar_camino_euleriano(self, inicio, numero_compuestos, grafo_euleriano):
        camino = []
        actual = inicio
        for _ in range(numero_compuestos):
            vecinos = grafo_euleriano[actual].copy()
            for siguiente in vecinos:
                # Intenta remover el enlace temporalmente
                grafo_euleriano[actual].remove(siguiente)
                grafo_euleriano[siguiente].remove(actual)
                if self.es_alcanzable_BFS(actual,siguiente,grafo_euleriano):
                    camino.append((actual,siguiente))
                    actual = siguiente
                    break
                else: 
                    # Restaura el enlace si no es posible avanzar
                    grafo_euleriano[actual].append(siguiente)
                    grafo_euleriano[siguiente].append(actual)   
        return camino

    def dijkstra(self, nodo_inicio):
        distancias = [float('inf')] * len(self.vertices)
        distancias[nodo_inicio] = 0
        visitados = [False] * len(self.vertices)
        caminos = [[] for _ in range(len(self.vertices))] 
        
        for _ in range(len(self.vertices)):
            min_distancia = float('inf')
            min_vertice = -1
            for v in range(len(self.vertices)):
                if not visitados[v] and distancias[v] < min_distancia:
                    min_distancia = distancias[v]
                    min_vertice = v
            visitados[min_vertice] = True
            
            for v in range(len(self.vertices)):
                if (not visitados[v]) and (self.matriz_ady[min_vertice][v] != 0):
                    nueva_distancia = distancias[min_vertice] + self.matriz_ady[min_vertice][v]
                    if nueva_distancia < distancias[v]:
                        distancias[v] = nueva_distancia
                        caminos[v] = caminos[min_vertice] + [min_vertice]
        return distancias, caminos

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
        
        self.grafo, self.vertices_fundamentales, self.num_compuestos_fund = self.cargar_grafo(lineas)
        ################################################################################# DETERMINA SI SE PUEDE HACER O NO :) y halla el euleriano :)
        rpsta, grafo_euleriano, source_eulerian = self.grafo.determinar_si_se_puede_y_grafo_euleriano()

        if rpsta == False:
            self.escribir_resultado("NO SE PUEDE", output_file)
        else:

            camino_euleriano = self.grafo.encontrar_camino_euleriano(source_eulerian, self.num_compuestos_fund, grafo_euleriano)
            print(f"El camino euleriano es {camino_euleriano}")

            self.escribir_resultado(camino_euleriano, output_file)
            self.grafo, self.vertices_libres = self.grafo_vertices_libres(self.grafo)
                        
            self.grafo_completo = self.crear_grafo_completo(self.grafo)
            self.matriz_grafo, self.diccionario_indices = self.grafo_completo.crear_matriz_ady()  # Agrega los paréntesis para invocar el método y captura los valores devueltos
            
            ############################################################################## para no hacerle dijkstra a todos los vertices, estos son los vertices fundamentales repetidos
            self.vertices_iterables = self.grafo_completo.vertices_fundamentales_repetidos()
            
            #TODO: HAY QUE CORREGIR LO DE LOS COSTOS DE LOS VERTICES LIBRES, si ?
            distancias, caminos = self.grafo_completo.dijkstra(0)
            
            ## IMPRIME LA DISTANCIA DESE EL VERTICE 0 HASTA TODOS LOS NODOS, Y SUS RESPECTIVOS CAMINOS
            respuesta_dijkstra(self.grafo_completo, distancias, caminos)
                    
            self.escribir_resultado(self.grafo_completo, output_file)
            
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
        num_compuestos_fund = index
        return grafo, vertices_fundamentales, num_compuestos_fund

    def grafo_vertices_libres(self, grafo): #crear un grafo conectado para hacerle dijkstra n veces
            original_vertices = set(grafo.vertices)
            vertices_libres = []
            for vertice in original_vertices:
                carga_opuesta = "-" if vertice.carga == "+" else  "+"
                vertice_opuesto = Vertice(vertice.masa, carga_opuesta)
                if vertice_opuesto not in original_vertices and vertice_opuesto not in grafo.vertices:
                    grafo.add_vertice(vertice_opuesto)
                    vertices_libres.append(vertice_opuesto)
                
                vertice_real_libre = Vertice(vertice.masa, vertice.carga)
                if vertice_real_libre not in original_vertices and vertice_real_libre not in grafo.vertices:
                    grafo.add_vertice(vertice_real_libre)
                    vertices_libres.append(vertice_real_libre)
                
                
            return grafo, vertices_libres
    
    
    def crear_grafo_completo(self, grafo):
        # Vamos a conectar todos los vertices fundamentales con cada vertice libre, pero no se pueden conectar vertices con la misma masa. 
        #TODO: CORREGIR LO DE LOS COSTOS DE LOS ATOMOS LIBRES, si ?
        for vertice_fund in self.vertices_fundamentales:
            for vertice_libre in self.vertices_libres:
                if vertice_fund.masa != vertice_libre.masa:
                    costo = self.calcular_costo(vertice_fund, vertice_libre)
                    conexion_f_l = Conexion(vertice_fund, vertice_libre, costo)
                    if not any(conex.origen == vertice_fund and conex.destino == vertice_libre for conex in grafo.conexiones):
                        conexion_f_l = Conexion(vertice_fund, vertice_libre, costo)
                        grafo.add_conexion(conexion_f_l)

        for i in range(len(self.vertices_libres)):
            for j in range(i + 1, len(self.vertices_libres)):
                vertice_libre1 = self.vertices_libres[i]
                vertice_libre2 = self.vertices_libres[j]
                if vertice_libre1.masa != vertice_libre2.masa:  
                    costo = self.calcular_costo(vertice_libre1, vertice_libre2)
                    conexion_l_l = Conexion(vertice_libre1, vertice_libre2, costo)
                    if not any(conex.origen == vertice_libre1 and conex.destino == vertice_libre2 for conex in grafo.conexiones):
                        grafo.add_conexion(conexion_l_l)
                        conexion_l_l_inversa = Conexion(vertice_libre2, vertice_libre1, costo)
                        grafo.add_conexion(conexion_l_l_inversa)                    
            

        return grafo
    
    def escribir_camino_minimo(self, distancias, output_file):
        # Escribe el camino minimo en el archivo de salida
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {distancias}\n")
        print(f"Se escribio en el archivo P2.out para el caso {self.case_id}")
        
    
    def escribir_resultado(self, result, output_file):
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {result}\n")

        print (f"Se escribio en el archivo P2.out para el caso {self.case_id}")
        
#FUNCIONES ADICIONALES QUE SE EJECUTAN POR CASO
def respuesta_dijkstra(grafo, distancias, caminos):
    print("Distancias más cortas desde el nodo de inicio:")
    for i, distancia in enumerate(distancias):
        if i < len(grafo.vertices):
            vertice_info = (f"Nodo {i} (masa={grafo.vertices[i].masa}, "
                            f"carga={grafo.vertices[i].carga}, "
                            f"tipo={grafo.vertices[i].tipo}): {distancia}")
        else:
            vertice_info = f"Nodo {i}: {distancia}"
        print(vertice_info)

    print("\nCaminos mínimos desde el nodo de inicio:")
    for i, camino in enumerate(caminos):
        camino_descripcion = [f"nodo {j} (masa={grafo.vertices[j].masa}, "
                              f"carga={grafo.vertices[j].carga}, "
                              f"tipo={grafo.vertices[j].tipo})" for j in camino + [i]]
        print(f"Nodo {i}: " + " -> ".join(camino_descripcion))


#TODO: Funcion para ejecutar dijkstra en todos los vertices necesarios


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


# QUE NOS FALTA
# PROCEDIMIENTO:
# 1. Hallar el camino euleriano
# 2. Para el euleriano, hallar el costo total, para ello:
#   2.1. Hallar el costo de cada conexion entre los vertices fundamentales, 
    # esto significa que se debe hallar el camino minimo (dijkstra) entre cada par de vertices fundamentales
    # Si es 3 con 3, se halla el camino minimo entre 3 con -3 y así sucesivamente
#   2.2. Ir sumando los costos de las conexiones entre los vertices fundamentales
# 3. Retornar el camino incluyendo los atomos libres, y retornar el costo