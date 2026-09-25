import heapq
import math
import pandas as pd # Manejo de excel
import igraph as ig # Librería de grafos eficientes
import matplotlib.pyplot as plt # Librería para imágenes


class Grafos:

    def __init__(self, nombre, file):
        self.nombre = nombre
        self.grafo = self.crearGrafoExcel(file) # Se pone "self" para usar métodos dentro de la 
        

    def crearGrafoExcel(self, file):

        # Pasar el Excel a DataFrame
        df = pd.read_excel(file)

        # Proceso de buscar edges y número de vértices
        edges = []
        for i in range(len(df)):
            for j in range(1, len(df.columns)):
                if df.iloc[i, j] != 0 and (j-1, i) not in edges:
                    edges.append( (i, j-1) )
                    

        nVertices = len(df)

        # Instanciar el objeto grafo
        g = ig.Graph(nVertices, edges)

        # Añadir nombres a los vértices
        for i in range(len(df)):
            g.vs[i]['name'] = df.iloc[i, 0]

        # Añadir el peso a las aristas (el tiempo de transporte)
        for i in range(len(df)):
            for j in range(1, len(df.columns)):
                if df.iloc[i, j] != 0 and (j-1, i) not in edges:
                    g.es[g.get_eid(i, j-1)]['Tiempo'] = df.iloc[i, j]

        # Retornar
        return g



    def mostrarGrafo(self, ruta, cerrados):

        fig, ax = plt.subplots(figsize=(6, 6))

        coloresAristas = ["#000000"] * len(self.grafo.es)

        # Colorear los nodos cerrados
        coloresVertices = []

        for vertice in self.grafo.vs:
            if vertice["name"] in cerrados:
                coloresVertices.append("#000000")
            else:
                coloresVertices.append("#FF0000")

        # Colorear la ruta más corta
        if ruta is not None:
            for i in range(len(ruta) - 1):
                u = self.grafo.vs.find(name=ruta[i]).index
                v = self.grafo.vs.find(name=ruta[i + 1]).index

                eid = self.grafo.get_eid(u, v)

                coloresAristas[eid] = "#00AA00"

        ig.plot(
            self.grafo,
            target=ax,
            layout="circle",

            vertex_size=32,
            vertex_frame_width=2.5,
            vertex_frame_color="#000000",
            vertex_color=coloresVertices,
            vertex_label=self.grafo.vs["name"],
            vertex_label_color="#616161",
            vertex_label_dist=1.5,

            edge_label=self.grafo.es["Tiempo"],
            edge_color=coloresAristas,
            edge_label_color="#616161",
            edge_width=2
        )

        # Guardar imagen
        fig.savefig("imagenGrafo.png", dpi=300, bbox_inches="tight")

        plt.show()



    # Camino más corto

    def algDijkstra(self, origen, nodosCerrados):

        pq = []

        verticesDistancia = {self.grafo.vs.find(name=origen): 0}

        predecesor = {}

        for v in self.grafo.vs:
            if v != self.grafo.vs.find(name=origen):
                verticesDistancia[v] = math.inf

        heapq.heappush(pq, (verticesDistancia[self.grafo.vs.find(name=origen)], self.grafo.vs.find(name=origen).index, self.grafo.vs.find(name=origen)))

        while len(pq) != 0:

            distancia, index, v = heapq.heappop(pq)

            if distancia <= verticesDistancia[v]:

                for indexEdge in self.grafo.incident(index):
                    edge = self.grafo.es[indexEdge]

                    vAdj = edge.vertex_tuple[0]
                    if vAdj == v:
                        vAdj = edge.vertex_tuple[1]

                    if vAdj["name"] not in nodosCerrados and distancia + edge["Tiempo"]< verticesDistancia[vAdj]:
                        verticesDistancia[vAdj] = distancia + edge["Tiempo"]
                        heapq.heappush(pq, (verticesDistancia[vAdj], vAdj.index, vAdj))
                        predecesor[vAdj] = v

        return predecesor, verticesDistancia



    def obtenerCamino(self, nombreOrigen, nombreDestino, predecesor):
        origen = self.grafo.vs.find(name=nombreOrigen)
        destino = self.grafo.vs.find(name=nombreDestino)

        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual["name"])

            if actual == origen:
                break

            actual = predecesor[actual]

        camino.reverse()

        return camino


    def recalcularDijkstra(self, nombreOrigen, nombreDestino, rutaAnterior, distanciaAnterior, nodosCerrados):
        for cerrados in nodosCerrados:
            if cerrados in rutaAnterior:
                dictRuta, distancias = self.algDijkstra(nombreOrigen, nodosCerrados)
                destino = self.grafo.vs.find(name=nombreDestino)

                distanciaNueva = distancias[destino]

                if distanciaNueva == math.inf:
                    return [], math.inf

                rutaNueva = self.obtenerCamino(nombreOrigen, nombreDestino, dictRuta)


                return rutaNueva, distanciaNueva

        return rutaAnterior, distanciaAnterior


    
    def setNombre(self, nombre):
        self.nombre = nombre

    def getNombre(self):
        return self.nombre

    def getGrafo(self):
        return self.grafo
    
    def setGrafo(self, grafo):
        self.grafo = grafo
    
    
    





