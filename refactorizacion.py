import heapq

class AStar:
    def __init__(self, mapa, inicio_x, inicio_y, final_x, final_y):
        self.mapa = mapa
        self.tamanho = len(mapa)
        self.inicio = (inicio_x, inicio_y)
        self.final = (final_x, final_y)
        self.nodos_abiertos = []
        self.nodos_cerrados = [[False for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.g = {self.inicio: 0}
        self.h = {self.inicio: self.distancia_manhattan(self.inicio, self.final)}
        self.f = {self.inicio: self.g[self.inicio] + self.h[self.inicio]}
        self.padres = {self.inicio: None}
        heapq.heappush(self.nodos_abiertos, (self.f[self.inicio], self.inicio))

    def distancia_manhattan(self, nodo_actual, nodo_objetivo):
        return abs(nodo_actual[0] - nodo_objetivo[0]) + abs(nodo_actual[1] - nodo_objetivo[1])

    def encontrar_camino(self):
        while self.nodos_abiertos:
            _, nodo_actual = heapq.heappop(self.nodos_abiertos)
            self.nodos_cerrados[nodo_actual[0]][nodo_actual[1]] = True

            if nodo_actual == self.final:
                camino = []
                nodo = nodo_actual
                while nodo:
                    camino.append(nodo)
                    nodo = self.padres[nodo]
                camino.reverse()
                return camino

            for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (nodo_actual[0] + dx, nodo_actual[1] + dy)

                if 0 <= vecino[0] < self.tamanho and 0 <= vecino[1] < self.tamanho:
                    if self.nodos_cerrados[vecino[0]][vecino[1]]:
                        continue

                    if self.mapa[vecino[0]][vecino[1]] == 'x':
                        continue

                    nuevo_costo_g = self.g[nodo_actual] + 1

                    if vecino not in self.g or nuevo_costo_g < self.g[vecino]:
                        self.g[vecino] = nuevo_costo_g
                        self.h[vecino] = self.distancia_manhattan(vecino, self.final)
                        self.f[vecino] = self.g[vecino] + self.h[vecino]
                        self.padres[vecino] = nodo_actual
                        heapq.heappush(self.nodos_abiertos, (self.f[vecino], vecino))

        return None

class Mapa:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.mapa = [['.' for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.obstaculos = []

    def imprimir(self, inicio_x, inicio_y, final_x, final_y, path=None):
        for i, fila in enumerate(self.mapa):
            for j, celda in enumerate(fila):
                if path and (i, j) in path:
                    if i == inicio_x and j == inicio_y:
                        print('I', end=' ')
                    elif i == final_x and j == final_y:
                        print('F', end=' ')
                    else:
                        print('*', end=' ')
                else:
                    print(celda, end=' ')
            print()

    def agregar_obstaculo(self, obstaculo_x, obstaculo_y):
        if self.mapa[obstaculo_x][obstaculo_y] != 'x':
            self.mapa[obstaculo_x][obstaculo_y] = 'x'
            self.obstaculos.append((obstaculo_x, obstaculo_y))

    def eliminar_obstaculo(self, obstaculo_x, obstaculo_y):
        if (obstaculo_x, obstaculo_y) in self.obstaculos:
            self.mapa[obstaculo_x][obstaculo_y] = '.'
            self.obstaculos.remove((obstaculo_x, obstaculo_y))

# Ejemplo de uso
tamanho = 10
mapa_obj = Mapa(tamanho)

# Solicitar al usuario las coordenadas de inicio y fin
coordenadas_inicio = input("Ingresa las coordenadas de inicio (x y): ") 
inicio_x, inicio_y = map(int, coordenadas_inicio.split())
mapa_obj.mapa[inicio_x][inicio_y] = "I"

coordenadas_final = input("Ingresa las coordenadas finales (x y): ")
final_x, final_y = map(int, coordenadas_final.split())
mapa_obj.mapa[final_x][final_y] = "F"

# Solicitar al usuario las coordenadas de los obstáculos
while True:
    obstaculo = input("Ingresa las coordenadas del obstáculo (x y), o presiona Enter para terminar: ")
    if obstaculo == "":
        break
    obstaculo_x, obstaculo_y = map(int, obstaculo.split())
    mapa_obj.agregar_obstaculo(obstaculo_x, obstaculo_y)
    

# Encontrar el camino utilizando A*
a_star = AStar(mapa_obj.mapa, inicio_x, inicio_y, final_x, final_y)
camino = a_star.encontrar_camino()

# Imprimir el mapa con el camino encontrado (si existe)
if camino:
    print("\nMapa con camino encontrado:")
    mapa_obj.imprimir(inicio_x, inicio_y, final_x, final_y, path=camino)
else:
    print("\nNo se encontró un camino válido.")

# Ejemplo para eliminar obstáculos
print("\nEliminar obstáculos:")
while True:
    eliminar = input("Ingresa las coordenadas del obstáculo que quieres eliminar (x y), o presiona Enter para terminar: ")
    if eliminar == "":
        break
    eliminar_x, eliminar_y = map(int, eliminar.split())
    mapa_obj.eliminar_obstaculo(eliminar_x, eliminar_y)

# Imprimir el mapa actualizado
print("\nMapa actualizado:")
mapa_obj.imprimir(inicio_x, inicio_y, final_x, final_y)


