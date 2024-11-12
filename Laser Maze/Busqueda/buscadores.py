from estructuras import *

class Buscador:
    def __init__(self, initialState, goalTest, expansionFunction=None, depth=None):
        frontier = None
        self.frontier = frontier
        self._explored = set()
        self.goalTest = goalTest
        self.goalState = None
        self.expansion = expansionFunction
        self.depth = depth

    def search(self):
        while not self.frontier.esta_vacia():
            state = self.frontier.recoger()
            self._explored.add(state)
            print(state.dato)
            if self.goalTest(state):
                self.goalState = state
                break

            if self.depth is None or state.profundidad < self.depth:
                if self.expansion is not None:
                    state.siguientes = self.expansion(state)

            for siguiente in state.siguientes:
                if siguiente not in self.frontier.nodos and siguiente not in self._explored:
                    if self.expansion is None:
                        siguiente.padre = state
                    siguiente.profundidad = siguiente.padre.profundidad+1
                    self.frontier.insertar(siguiente)


    def show_path(self):
        path = []
        node = self.goalState
        while node is not None:
            path.append(node.dato)
            node = getattr(node, 'padre', None)
        path.reverse()
        return path

    def show_explored(self):
        return [i.dato for i in self._explored]

# BFS

class BFS(Buscador):
    def __init__(self, initialState, goalTest, expansionFunction=None, depth=None):
        super().__init__(initialState, goalTest, expansionFunction, depth)
        frontier = Cola()
        frontier.insertar(initialState)
        self.frontier = frontier
        


class DFS(Buscador):
    def __init__(self, initialState, goalTest, expansionFunction=None, depth=None):
        super().__init__(initialState, goalTest, expansionFunction, depth)
        frontier = Pila()
        frontier.insertar(initialState)
        self.frontier = frontier


class UCS(Buscador):
    def __init__(self, initialState, goalTest, expansionFunction=None, depth=None):
        super().__init__(initialState, goalTest, expansionFunction, depth)
        frontier = ColaPrioridad()
        frontier.insertar(initialState)
        self.frontier = frontier

    def search(self):
        #count = 1
        while not self.frontier.esta_vacia():
            state = self.frontier.recoger()
            self._explored.add(state)

            # print(state.dato)
            # print(self.frontier.nodos)
            # print(self.frontier.esta_vacia())
            # print(count)
            # count += 1
            if self.goalTest(state):
                self.goalState = state
                break

            if self.depth is None or state.profundidad < self.depth:
                if self.expansion is not None:
                    state.siguientes = self.expansion(state)

            for siguiente in state.siguientes:
                if siguiente not in self.frontier.nodos and siguiente not in self._explored:
                    if self.expansion is None:
                        siguiente.padre = state
                    siguiente.profundidad = siguiente.padre.profundidad+1
                    self.frontier.insertar(siguiente)
                elif siguiente in self.frontier.nodos and siguiente.padre.peso > state.peso:
                    self.frontier.decrease_key(siguiente, state.peso, state)

