class Nodo:
    def __init__(self, dato, peso=None, padre=None):
        self.dato = dato
        self.siguientes = []
        self.peso = peso
        self.padre = padre
        self.profundidad = 0

    def agregar_siguiente(self, nodo):
        self.siguientes.append(nodo)

    def __eq__(self, other):
        if isinstance(other, Nodo):
            return self.dato == other.dato
        return False

    def __hash__(self):
        return hash(str(self.dato))
    

class Estructura:
    def __init__(self):
        self.nodos = []

    def insertar(self,nodo):
        self.nodos.append(nodo)

    def esta_vacia(self):
        return len(self.nodos) == 0


class Pila(Estructura):
    def __init__(self):
        super().__init__()

    def ver_cabeza(self):
        if not self.esta_vacia():
            print(self.nodos[-1].dato)

    def recoger(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.nodos.pop()

    def tamano(self):
        return len(self.nodos)


class Cola(Estructura):
    def __init__(self):
        super().__init__()

    def ver_cabeza(self):
        if not self.esta_vacia():
            print(self.nodos[0].dato)

    def recoger(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.nodos.pop(0)

    def tamano(self):
        return len(self.nodos)


class ColaPrioridad:
    def __init__(self):
        self.heap = []
        self.posiciones = {}  # Mapeo de dato a índice en el heap
        self.nodos_en_frontier = set()
    @property
    def nodos(self):
        return self.nodos_en_frontier

    def esta_vacia(self):
        return len(self.nodos_en_frontier) == 0

    def insertar(self, nodo):
        self.heap.append(nodo)
        index = len(self.heap) - 1
        self.posiciones[nodo] = index
        self.nodos_en_frontier.add(nodo)
        self._flotar_arriba(index)

    def recoger(self):
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía")
        nodo_min = self.heap[0]
        ultimo_nodo = self.heap.pop()
        if self.heap:
            self.heap[0] = ultimo_nodo
            self.posiciones[ultimo_nodo] = 0
            self._hundir_abajo(0)
        del self.posiciones[nodo_min]
        self.nodos_en_frontier.remove(nodo_min)
        return nodo_min

    def eliminar(self, dato):
        index = self.posiciones.get(dato)
        if index is None:
            return  # El nodo no está en el heap
        ultimo_nodo = self.heap.pop()
        if index < len(self.heap):
            self.heap[index] = ultimo_nodo
            self.posiciones[ultimo_nodo] = index
            self._flotar_arriba(index)
            self._hundir_abajo(index)
        del self.posiciones[dato]

    def decrease_key(self, nodo, nuevo_peso, nuevo_padre=None):
        
        index = self.posiciones.get(nodo)
        if index is not None:
            nodo = self.heap[index]
            if nuevo_peso < nodo.peso:
                nodo.peso = nuevo_peso
                self._flotar_arriba(index)
            if nuevo_padre is not None:
                nodo.padre = nuevo_padre
        else:
            # Si el nodo no está en el heap, lo insertamos
            nuevo_nodo = Nodo(nodo.dato, nuevo_peso)
            self.insertar(nuevo_nodo)

    def _flotar_arriba(self, index):
        nodo = self.heap[index]
        while index > 0:
            padre_index = (index - 1) // 2
            padre_nodo = self.heap[padre_index]
            if nodo.peso < padre_nodo.peso:
                # Intercambiar nodos
                self.heap[index], self.heap[padre_index] = padre_nodo, nodo
                # Actualizar posiciones en el mapa
                self.posiciones[nodo] = padre_index
                self.posiciones[padre_nodo] = index
                index = padre_index
            else:
                break

    def _hundir_abajo(self, index):
        tamaño = len(self.heap)
        nodo = self.heap[index]
        while True:
            hijo_izq_index = 2 * index + 1
            hijo_der_index = 2 * index + 2
            menor_index = index

            if hijo_izq_index < tamaño and self.heap[hijo_izq_index].peso < self.heap[menor_index].peso:
                menor_index = hijo_izq_index
            if hijo_der_index < tamaño and self.heap[hijo_der_index].peso < self.heap[menor_index].peso:
                menor_index = hijo_der_index

            if menor_index != index:
                menor_nodo = self.heap[menor_index]
                # Intercambiar nodos
                self.heap[index], self.heap[menor_index] = menor_nodo, nodo
                # Actualizar posiciones en el mapa
                self.posiciones[nodo] = menor_index
                self.posiciones[menor_nodo] = index
                index = menor_index
            else:
                break