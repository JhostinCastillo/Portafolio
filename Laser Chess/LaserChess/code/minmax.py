import numpy as np
import time
from copy import deepcopy
import inspect

config_pred = {'h1':'10',
                'h2':'10',
                'h3':'10',
                'h4':'10',
                'h5':'10'}
# return None, -state.sumar_puntos(self.turno)*1000
class MinMaxSolver:
    def __init__(self):
        self.turno = None
        self.start_time = None
        self.max_time = None
        self.nodos = 0
        self.max_depth = 0

    def _maximize(self, state, alpha, beta, depth, config):

        if time.time() - self.start_time >= self.max_time:
            raise StopIteration('Se acabo el tiempo')

        if state.is_terminal():
            return None, state.rey_cazado(self.turno)
        
        if depth<=0:
            return None, state.heuristica(self.turno, config)
        
        max_child, max_utility = None, -np.inf

        #capturar nodos
        children = state.children()
        self.nodos += len(children)

        for option_copy, child in children:
            _, utility = self._minimize(child, alpha, beta, depth-1, config)
            #print(utility)
            # self.opciones.append((child.obtener_estado_actual(), utility))

            if utility > max_utility:
                max_child, max_utility = option_copy, utility

            if max_utility >= beta:
                break

            alpha = max(alpha, max_utility)

        return max_child, max_utility
    

    def _minimize(self, state, alpha, beta, depth, config):

        if time.time() - self.start_time >= self.max_time:
            raise StopIteration('Se acabo el tiempo')

        if state.is_terminal():
            return None, state.rey_cazado(self.turno)
        
        if depth<=0:
            return None, state.heuristica(self.turno, config)
        
        min_child, min_utility = None, np.inf

        #capturar nodos
        children = state.children()
        self.nodos += len(children)
        for option_copy, child in state.children():
            _, utility = self._maximize(child, alpha, beta, depth-1, config)
            # print(utility)
            # self.opciones.append((child.obtener_estado_actual(), utility))

            if utility < min_utility:
                min_child, min_utility = option_copy, utility

            if min_utility <= alpha:
                break

            beta = min(beta, min_utility)

        return min_child, min_utility
    
    def solve(self, state, max_time, depth_limit=100, config=config_pred):
        self.turno = state.turno
        self.start_time = time.time()
        self.max_time = max_time
        for depth in range(1,depth_limit):
            try:
                option, _ = self._maximize(state, -np.inf, np.inf, depth, config)
            except StopIteration:
                break

        try:
            # if hasattr(option, 'res'):
            #     print(f"res: {option.res}")
            # if hasattr(option, 'key'):
            #     print(f"key: {option.key}")
            # if hasattr(option, 'direc'):
            #     print(f"direc: {option.direc}")
            # input()
            self.max_depth = depth
            return option
        except UnboundLocalError:
            print('Aleatorio')
            input()
            children = state.children()
            return children[np.random.randint(len(children))][0]
    

class MinMaxInvert:
    def __init__(self):
        self.turno = None
        self.start_time = None
        self.max_time = None
        # self.opciones = []
        self.nodos = 0
        self.max_depth = 0

    def _maximize(self, state, alpha, beta, depth, config):

        if time.time() - self.start_time >= self.max_time:
            raise StopIteration('Se acabo el tiempo')

        if state.is_terminal():
            return None, state.rey_cazado(self.turno)
        
        if depth<=0:
            return None, state.heuristica(self.turno, config)
        
        max_child, max_utility = None, -np.inf

        #capturar nodos
        children = state.children()
        self.nodos += len(children)
        for option_copy, child in state.children():
            _, utility = self._minimize(child, alpha, beta, depth-1, config)
            #print(utility)
            # self.opciones.append((child.obtener_estado_actual(), utility))

            if utility > max_utility:
                max_child, max_utility = option_copy, utility

            if max_utility >= beta:
                break

            alpha = max(alpha, max_utility)

        return max_child, max_utility
    

    def _minimize(self, state, alpha, beta, depth, config):

        if time.time() - self.start_time >= self.max_time:
            raise StopIteration('Se acabo el tiempo')

        if state.is_terminal():
            return None, state.rey_cazado(self.turno)
        
        if depth<=0:
            return None, state.heuristica(self.turno, config)
        
        min_child, min_utility = None, np.inf

        #capturar nodos
        children = state.children()
        self.nodos += len(children)
        for option_copy, child in state.children():
            _, utility = self._maximize(child, alpha, beta, depth-1, config)
            # print(utility)
            # self.opciones.append((child.obtener_estado_actual(), utility))

            if utility < min_utility:
                min_child, min_utility = option_copy, utility

            if min_utility <= alpha:
                break

            beta = min(beta, min_utility)

        return min_child, min_utility
    
    def solve(self, state, max_time, depth_limit=100, config=config_pred):
        self.turno = state.turno
        self.start_time = time.time()
        self.max_time = max_time
        for depth in range(1,depth_limit):
            try:
                option, _ = self._minimize(state, -np.inf, np.inf, depth, config)
            except StopIteration:
                break
        try:
            self.max_depth = depth
            return option
        except UnboundLocalError:
            print('Aleatorio')
            input()
            children = state.children()
            return children[np.random.randint(len(children))][0]
    

