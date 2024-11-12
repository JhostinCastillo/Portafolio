import numpy as np
from minmax import *

class CPU:
    def __init__(self, dificultad, time=5):
        self.dificultad = dificultad
        self.time = time
        self.max_nodos = 0
        self.max_depth = 0

    def _malo(self, game):
        minmaxinv = MinMaxInvert()
        option = minmaxinv.solve(game, self.time)
        return option, minmaxinv.nodos, minmaxinv.max_depth
        
    def _aleatorio(self, game):
        lista_acciones = game.todas_las_acciones(game.turno)
        option = np.random.choice(lista_acciones)
        return option, 0, 0
    
    def _estandar(self, game):
        minmax = MinMaxSolver()
        option = minmax.solve(game, self.time)
        return option, minmax.nodos, minmax.max_depth
    
    def _greedy(self, game):
        minmax = MinMaxSolver()
        option = minmax.solve(game, 2, depth_limit=1)
        return option, minmax.nodos, minmax.max_depth
    
    def _config1(self, game):
        #Agresivo
        config = {'h1':'10',
                  'h2':'20',
                  'h3':'20',
                  'h4':'20',
                  'h5':'30'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _config2(self, game):
        #Defensivo
        config = {'h1':'35',
                  'h2':'10',
                  'h3':'5',
                  'h4':'20',
                  'h5':'30'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _heuristica1v(self, game):
        config = {'h1':'100'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _heuristica2v(self, game):
        config = {'h1':'50',
                  'h2':'50'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _heuristica3v(self, game):
        config = {'h1':'33',
                  'h2':'33',
                  'h3':'33'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _heuristica4v(self, game):
        config = {'h1':'25',
                  'h2':'25',
                  'h3':'25',
                  'h4':'25'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _heuristica5v(self, game):
        config = {'h1':'20',
                  'h2':'20',
                  'h3':'20',
                  'h4':'20',
                  'h5':'20'}
        minmax = MinMaxSolver()
        option = minmax.solve(game, 5, config=config)
        return option, minmax.nodos, minmax.max_depth

    def _tiempo1segs(self, game):
        minmax = MinMaxSolver()
        option = minmax.solve(game, 1)
        return option, minmax.nodos, minmax.max_depth

    def _tiempo3segs(self, game):
        minmax = MinMaxSolver()
        option =  minmax.solve(game, 3)
        return option, minmax.nodos, minmax.max_depth

    def _tiempo10segs(self, game):
        minmax = MinMaxSolver()
        option = minmax.solve(game, 10)
        return option, minmax.nodos, minmax.max_depth
    

    def jugar(self, game):
        match self.dificultad:
            case 'malo':
                option, nodos, depth = self._malo(game)
            case 'aleatorio':
                option, nodos, depth = self._aleatorio(game)
            case 'estandar':
                option, nodos, depth = self._estandar(game)
            case 'greedy':
                option, nodos, depth = self._greedy(game)
            case 'config1':
                option, nodos, depth = self._config1(game)
            case 'config2':
                option, nodos, depth = self._config2(game)
            case 'heuristica1v':
                option, nodos, depth = self._heuristica1v(game)
            case 'heuristica2v':
                option, nodos, depth = self._heuristica2v(game)
            case 'heuristica3v':
                option, nodos, depth = self._heuristica3v(game)
            case 'heuristica4v':
                option, nodos, depth = self._heuristica4v(game)
            case 'heuristica5v':
                option, nodos, depth = self._heuristica5v(game)
            case 'tiempo1segs':
                option, nodos, depth = self._tiempo1segs(game)
            case 'tiempo3segs':
                option, nodos, depth = self._tiempo3segs(game)
            case 'tiempo10segs':
                option, nodos, depth = self._tiempo10segs(game)

        if nodos > self.max_nodos:
            self.max_nodos = nodos
        if depth > self.max_depth:
            self.max_depth = depth

        option(game)