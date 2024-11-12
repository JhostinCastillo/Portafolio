import numpy
from tablero import Tablero
from fichas import *
import time
import os
import menu
from copy import deepcopy
from Recursos import printdecoracion
from Recursos import recursos
from copy import deepcopy
import sys
from cpu import CPU



# Intercambiador
    # Hacer un bucle que itere dentro de todas las fichas
    # Tomar las fichas en posiciones adyacentes y mostrarlas como opciones
    # pedir opcion al jugador
    # Intercambiar posicion con la opcion seleccionada


class Game:
  fichas = {'F':Defensor,
            'f':Defensor,
            'R':Rey,
            'r':Rey,
            'D':Deflector,
            'd':Deflector,
            'I': Intercambiador,
            'i': Intercambiador,
            'L': Emisor,
            'l': Emisor}
  def __init__(self, partida, inicio, cpu_level=['aleatorio', 'estandar']):
    self.partida = partida
    self.inicio = inicio
    self.tablero = Tablero(partida, inicio)
    self.__estado = None
    self.puntos_maximos = self.sumar_puntos()
    self.turno = 0
    self.mode = None
    self.CPU1 = CPU(cpu_level[0])
    self.CPU2 = CPU(cpu_level[1])
    self.impactos = 0
    self.timer = None
# ----Funciones internas para algoritmos de busqueda

# Funcion meta
  def is_terminal(self):
      reyes = []
      for rey in self.tablero.reyes:
        reyes.append(rey.eliminado)
      
      return any(reyes)
  
  def rey_cazado(self, turno):
    color = 'rojo' if turno % 2 == 0 else 'azul'
    for rey in self.tablero.reyes:
       if rey.eliminado:
        if rey.color != color:
           return 10000
        else:
           return -10000
  # Funcion de puntuacion

  def sumar_puntos(self, turno=None):

    total_puntos = 0

    # Listas de todas las fichas
    todas_las_fichas = (
        self.tablero.deflectores +
        self.tablero.defensores +
        self.tablero.intercambiadores +
        self.tablero.emisores +
        self.tablero.reyes
    )

    if turno is not None:
      puntos_azul = 0
      puntos_rojo = 0
      color = 'rojo' if turno % 2 == 0 else 'azul'
      # Filtrar por color
      for ficha in todas_las_fichas:
          if ficha.color == 'azul':
              puntos_azul += ficha.puntos

      for ficha in todas_las_fichas:
          if ficha.color == 'rojo':
              puntos_rojo += ficha.puntos

      if color == 'azul':
         total_puntos = self.puntos_maximos-puntos_rojo
      else:
         total_puntos = self.puntos_maximos-puntos_azul

    else:
      for ficha in todas_las_fichas:
         if ficha.color == 'rojo':
            total_puntos += ficha.puntos

    return total_puntos

  # Heuristica
    

     #heuristica 1
  def _heuristica1(self, turno):
    return self.sumar_puntos(turno) / self.puntos_maximos

    #heuristica 2
  def _heuristica2(self, turno):
    return -self.sumar_puntos(turno+1) / self.puntos_maximos

    #heuristica 3 - Control del centro
  def _heuristica3(self, turno):
    color = 'rojo' if turno % 2 == 0 else 'azul'
    h3 = 0
    count = 0
    for ficha in self.tablero.todas_fichas:
        if ficha.color == color:
            count +=1
            x, y = ficha.posicion
            if 3 <= x <= 6 and 3 <= y <= 6:
                h3 += 1
    return h3/count  
            
    #heuristica 4 - Movilidad de las piezas

  def _heuristica4(self, turno):
    color = 'rojo' if turno % 2 == 0 else 'azul'
    deflectores = 0
    defensores = 0
    intercambiadores = 0
    
    for ficha in self.tablero.todas_fichas:
        if ficha.color == color:
          if ficha.simbolo == 'F':
              defensores += 1
          elif ficha.simbolo == 'D':
              deflectores += 1
          elif ficha.simbolo == 'I':
              intercambiadores += 1
    defensores = defensores*4*8
    deflectores = deflectores*4*8
    intercambiadores = intercambiadores*4*8
    rey = 8
    laser = 1
    return len(self.todas_las_acciones(turno))/(defensores+deflectores+intercambiadores+rey+laser)

    #heuristica 5 - impactos del laser
  def _heuristica5(self, turno):
    return self.impactos/(len(self.tablero.todas_fichas)-4)
  
  def heuristica(self, turno, config_dict):
     heuristicas = {'h1':'self._heuristica1(turno)',
                    'h2':'self._heuristica2(turno)',
                    'h3':'self._heuristica3(turno)',
                    'h4':'self._heuristica4(turno)',
                    'h5':'self._heuristica5(turno)'}
     
     hs = list(config_dict.keys())
     config = ''
     for h in hs:
        if hs.index(h)==len(hs)-1:
          config += h 
        else:
           config += h

     for h in hs:
        config = config.replace(h, heuristicas[h]+'*'+config_dict[h]+'+')[:-1]

     return eval(config)
  

# Funcion para jugar un estado
  def _configurar_juego(self, estado):
    def obtener_color(x):
      return 'azul' if x.isupper() else 'rojo'
    self.tablero.tablero = [['.' for elemento in sublista] for sublista in self.tablero.tablero]
    for simbolo, valores in estado.items():
      for valor in valores:
        if simbolo in ['L', 'l']:
           ficha = self.fichas[simbolo](color=obtener_color(simbolo))
           ficha.cambiar_grados(valor['grado'])
        else:
          ficha = self.fichas[simbolo]((valor['j'], valor['i']), obtener_color(simbolo))
          ficha.cambiar_grados(valor['grado'])

        self.tablero.colocar_ficha(ficha,desbloqueo=True)
    
  def _ejecutar_estado(game, turno=None, show=True):
    if turno is None:
      game.disparar(game.turno, show)
    else:
       game.disparar(turno, show)
    game.tablero.limpiar_tablero()

      
  def jugar_estado(self, estado, turno=None):
    #estado = nodo.dato[0]
    self._configurar_juego(estado)
    return self._ejecutar_estado(turno)
  
  def obtener_estado_actual(self):
     return self.tablero.obtener_estado()


# ------------------------------------

# Funcion de expansion

  def children(self):
    #base_state = self.obtener_estado_actual()
    #self.tablero.get_analizar_tablero()
    options = self.todas_las_acciones(self.turno)
    children = []
    for option in options:
        # Crear una copia del juego
        copy_game = deepcopy(self)
        #copy_game._configurar_juego(base_state)
        # Aplicar la opción a la copia del juego
        option(copy_game)
        # Ejecutar el estado después de la acción
        copy_game._ejecutar_estado(copy_game.turno, show=False)
        # Agregar el índice, la opción y la copia del juego a la lista de hijos
        children.append((option, copy_game))
    return children

       

# ------------------------------------

  def __dibujar_laser(self, laser):
    try:
      i,j = laser.posicion
      
      if i < 0 or j < 0:
        laser.direccion = (0,0)

      if self.tablero.tablero[j][i] in ['.', '←', '→', '↑', '↓', '↖','↗','↙','↘']:
        if laser.direccion == (0,-1):
          self.tablero.tablero[j][i] = laser.arriba
        elif laser.direccion == (0,1):
          self.tablero.tablero[j][i] = laser.abajo
        elif laser.direccion == (1,0):
          self.tablero.tablero[j][i] = laser.derecha
        elif laser.direccion == (-1,0):
          self.tablero.tablero[j][i] = laser.izquierda
        elif laser.direccion == (1,-1):
          self.tablero.tablero[j][i] = laser.arriba_derecha
        elif laser.direccion == (-1,1):
          self.tablero.tablero[j][i] = laser.abajo_izquierda
        elif laser.direccion == (-1,-1):
          self.tablero.tablero[j][i] = laser.arriba_izquierda
        elif laser.direccion == (1,1):
          self.tablero.tablero[j][i] = laser.abajo_derecha
      else:
        pass
    # El laser salio del tablero
    except IndexError:
      laser.direccion = (0,0)

  def __verificar_lasers(self):
    estatus = []
    for laser in self.tablero.lasers:
      estatus.append(laser.direccion!=(0,0))
    return all(estatus)
  
        

  # def jugar_cpu(self, turno):
  #   lista_acciones = self.todas_las_acciones(turno)
  #   time.sleep(1)
  #   ia = numpy.random.choice(lista_acciones)
  #   ia()



  def __main_loop(self, mode=1):
    match mode:
       case 1:
          self.timer = time.time()
          while True:
              self.__es_ganador()
              self.turno += 1
              self.tablero.imprimir_tablero()
              self.jugar_jugador(self.turno)
              self.disparar(self.turno)
              self.tablero.limpiar_tablero()
       case 2:
          self.timer = time.time()
          while True:
              self.__es_ganador()
              self.turno += 1
              
              self.tablero.imprimir_tablero()
              if self.turno % 2 == 0:
                self.jugar_jugador(self.turno)
              else:
                 self.CPU1.jugar(self)
              self.disparar(self.turno)
              self.tablero.limpiar_tablero()
       case 3:
          self.timer = time.time()
          while True:
              self.__es_ganador()
              self.turno += 1
              self.tablero.imprimir_tablero()
              
              if self.turno % 2 == 0:
                self.CPU1.jugar(self)
              else:
                 self.CPU2.jugar(self)
              self.disparar(self.turno)
              self.tablero.limpiar_tablero()


  def disparar(self,turno,show=True):
    laser = None
    if turno % 2 == 0:
        for emisor in self.tablero.emisores:
           if emisor.color == 'rojo':
                laser = emisor.accion()
    else:
       for emisor in self.tablero.emisores:
           if emisor.color == 'azul':
                laser = emisor.accion()


    self.tablero.lasers[0] = laser
    self.__dibujar_laser(laser)

    while self.__verificar_lasers():
      if show:
        os.system('cls')
        self.tablero.imprimir_tablero()
        time.sleep(.5)
      self.__actualizar_laser()
      if show:
        self.__es_ganador()
       
  def __auxiliar_mover(self,res,direc):

    direcciones = [("→",(1,0)),("↗",(1,-1)),("↑",(0,-1)),("↖",(-1,-1)),("←",(-1,0)),("↙",(-1,1)),("↓",(0,1)),("↘",(1,1))]
    self.tablero.tablero[self.tablero.todas_fichas[res].posicion[1]][self.tablero.todas_fichas[res].posicion[0]] = '.'
    if self.tablero.todas_fichas[res].posicion in self.tablero.posiciones_ocupadas:
      self.tablero.posiciones_ocupadas.remove(self.tablero.todas_fichas[res].posicion)
    self.tablero.todas_fichas[res].mover(direcciones[direc][1])
    self.tablero.posiciones_ocupadas.append(self.tablero.todas_fichas[res].posicion)
    self.tablero.tablero[self.tablero.todas_fichas[res].posicion[1]][self.tablero.todas_fichas[res].posicion[0]] = self.tablero.todas_fichas[res].simbolo
  
  def __auxiliar_intercambiar(self,res,direc):
    self.tablero.tablero[self.tablero.todas_fichas[res].posicion[1]][self.tablero.todas_fichas[res].posicion[0]] = self.tablero.todas_fichas[direc].simbolo
    self.tablero.tablero[self.tablero.todas_fichas[direc].posicion[1]][self.tablero.todas_fichas[direc].posicion[0]] = self.tablero.todas_fichas[res].simbolo
    self.tablero.todas_fichas[res].intercambiar(self.tablero.todas_fichas[direc])

  def jugar_jugador(self, turno):
    
    def mover(self, color):

        direcciones = [("→",(1,0)),("↗",(1,-1)),("↑",(0,-1)),("↖",(-1,-1)),("←",(-1,0)),("↙",(-1,1)),("↓",(0,1)),("↘",(1,1))]

        os.system('cls')
        self.tablero.imprimir_tablero()

        if color == 'azul':
            print(recursos['ACCIONESAZUL'])
            printdecoracion('herramientas','sup')
            print('Fichas disponibles para mover')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
                if ficha.color == "azul" and ficha.simbolo not in 'L R':
                    simbolo = recursos[ficha.simbolo+'AZUL'][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
                elif ficha.color == "azul" and ficha.simbolo == 'R':
                    simbolo = recursos[ficha.simbolo+'AZUL']
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
               
            printdecoracion('herramientas','inf')
            res = int(input())

            for idx, direc in enumerate(direcciones):
               posicion = self.tablero.todas_fichas[res].posicion
               siguiente_pos = (posicion[0] + direc[1][0], posicion[1] + direc[1][1])
               if self.tablero.se_puede_mover("azul",siguiente_pos):
                  print(f"[{idx}] {direc[0]}")
               
            printdecoracion('herramientas','inf')
            direc = int(input())
            
            self.__auxiliar_mover(res,direc)

        elif color == 'rojo':
            print(recursos['ACCIONESROJO'])
            printdecoracion('herramientas','sup')
            print('Fichas disponibles para mover')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
                if ficha.color == "rojo" and ficha.simbolo not in 'l r':
                    simbolo = recursos[ficha.simbolo+'ROJO'][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
                elif ficha.color == "rojo" and ficha.simbolo == 'r':
                    simbolo = recursos[ficha.simbolo+'ROJO']
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
               
            printdecoracion('herramientas','inf')
            res = int(input())

            for idx, direc in enumerate(direcciones):
               posicion = self.tablero.todas_fichas[res].posicion
               siguiente_pos = (posicion[0] + direc[1][0], posicion[1] + direc[1][1])
               if self.tablero.se_puede_mover("rojo",siguiente_pos):
                  print(f"[{idx}] {direc[0]}")
               
            printdecoracion('herramientas','inf')
            direc = int(input())
            
            self.__auxiliar_mover(res,direc)

    def rotar(self, color):
        os.system('cls')
        self.tablero.imprimir_tablero()

        if color == 'azul':
            print(recursos['ACCIONESAZUL'])
            printdecoracion('herramientas','sup')
            print('Fichas disponibles para rotar')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
               if ficha.color == "azul" and ficha.simbolo != 'R':
                simbolo = recursos[ficha.simbolo+'AZUL'][ficha.grado]
                print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
            
            res = int(input())

            for key, val in recursos[self.tablero.todas_fichas[res].simbolo+'AZUL'].items():
               if key != None and key != self.tablero.todas_fichas[res].grado:
                 print(f"[{key}] {val}")
               
            grado = int(input())

            self.tablero.todas_fichas[res].cambiar_grados(grado)

        elif color == 'rojo':
            print(recursos['ACCIONESROJO'])
            printdecoracion('herramientas','sup')
            print('Fichas disponibles para rotar')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
               if ficha.color == "rojo" and ficha.simbolo != 'r':
                simbolo = recursos[ficha.simbolo+'ROJO'][ficha.grado]
                print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')
            
            printdecoracion('herramientas','inf')
            res = int(input())

            for key, val in recursos[self.tablero.todas_fichas[res].simbolo+'ROJO'].items():
               if key != None and key != self.tablero.todas_fichas[res].grado:
                 print(f"[{key}] {val}")
            
            printdecoracion('herramientas','inf')
            grado = int(input())

            self.tablero.todas_fichas[res].cambiar_grados(grado)
        
    def intercambiar(self,color):
        os.system('cls')
        self.tablero.imprimir_tablero()

        if color == 'azul':
            print(recursos['ACCIONESAZUL'])
            printdecoracion('herramientas','sup')
            print('Intercambiadores disponibles')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
                if ficha.color == "azul" and ficha.simbolo == 'I':
                    simbolo = recursos[ficha.simbolo+'AZUL'][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')

            printdecoracion('herramientas','inf')
            res = int(input())
            se_puede_intercambiar = False

            for idx, ficha in enumerate(self.tablero.todas_fichas):
              if self.tablero.todas_fichas[res].es_intercambiable(ficha):
                    se_puede_intercambiar = True
                    simbolo = recursos[ficha.simbolo+ficha.color.upper()][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (columna - fila)')
              
            if not se_puede_intercambiar:
              input('⚠️ No se encontraron fichas para intercambiar')
              os.system('cls')
              self.tablero.imprimir_tablero()
              self.jugar_jugador(turno)

            else:
              printdecoracion('herramientas','inf')
              direc = int(input())
              self.__auxiliar_intercambiar(res,direc)

        elif color == 'rojo':
            print(recursos['ACCIONESROJO'])
            printdecoracion('herramientas','sup')
            print('Intercambiadores disponibles')

            for idx, ficha in enumerate(self.tablero.todas_fichas):
                if ficha.color == "rojo" and ficha.simbolo == 'i':
                    simbolo = recursos[ficha.simbolo+'ROJO'][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (Columna - Fila)')

            printdecoracion('herramientas','inf')
            res = int(input())
            se_puede_intercambiar = False

            for idx, ficha in enumerate(self.tablero.todas_fichas):
              if self.tablero.todas_fichas[res].es_intercambiable(ficha):
                    se_puede_intercambiar = True
                    simbolo = recursos[ficha.simbolo+ficha.color.upper()][ficha.grado]
                    print(f'[{idx}] {simbolo} en {ficha.posicion} (columna - fila)')
              
            if not se_puede_intercambiar:
              input('⚠️ No se encontraron fichas para intercambiar')
              os.system('cls')
              self.tablero.imprimir_tablero()
              self.jugar_jugador(turno)

            else:
              printdecoracion('herramientas','inf')
              direc = int(input())
              self.__auxiliar_intercambiar(res,direc)

    if turno % 2 == 0:
        color = 'rojo'
        print(recursos['ACCIONESROJO'])
        printdecoracion('herramientas','sup')

        print("[1] Rotar ficha \n[2] Mover ficha \n[3] Usar el intercambiador")

        printdecoracion('herramientas','inf')
        opcion = input()
        while opcion not in ['1','2','3']:
           print('opcion no valida')
           opcion = input("[1] Rotar ficha \n[2] Mover ficha \n[3] Usar el intercambiador")

        match opcion:
           
            case '1':
                rotar(self,color)
           
            case '2':
                mover(self,color)
            
            case '3':
                intercambiar(self,color)
                

    elif turno % 2 == 1:
        color = 'azul'
        print(recursos['ACCIONESAZUL'])
        printdecoracion('herramientas','sup')

        print("[1] Rotar ficha \n[2] Mover ficha \n[3] Usar el intercambiador")

        printdecoracion('herramientas','inf')
        opcion = input()
        while opcion not in ['1','2','3']:
           print('opcion no valida')
           opcion = input("[1] Rotar ficha \n[2] Mover ficha \n[3] Usar el intercambiador")

        match opcion:
            
            case '1':
                rotar(self,color)
            
            case '2':
                mover(self,color) 
            
            case '3':
                intercambiar(self,color)

    else:
       raise AssertionError("Turnos incorrector")

  def todas_las_acciones(self, turno):
    if turno % 2 == 0:
        color = 'rojo'
    else:
        color = 'azul'

    list_acciones = []

    # Funciones auxiliares definidas dentro de todas_las_acciones
    def auxiliar_mover(game, res, direc):
        direcciones = [("→", (1, 0)), ("↗", (1, -1)), ("↑", (0, -1)), ("↖", (-1, -1)), ("←", (-1, 0)), ("↙", (-1, 1)), ("↓", (0, 1)), ("↘", (1, 1))]
        ficha = game.tablero.todas_fichas[res]
        posicion_actual = ficha.posicion
        tablero = game.tablero.tablero
        posiciones_ocupadas = game.tablero.posiciones_ocupadas

        # Limpiar la posición actual en el tablero
        tablero[posicion_actual[1]][posicion_actual[0]] = '.'
        if posicion_actual in posiciones_ocupadas:
            posiciones_ocupadas.remove(posicion_actual)

        # Mover la ficha
        movimiento = direcciones[direc][1]
        ficha.mover(movimiento)

        # Actualizar posiciones ocupadas
        nueva_posicion = ficha.posicion
        posiciones_ocupadas.append(nueva_posicion)
        tablero[nueva_posicion[1]][nueva_posicion[0]] = ficha.simbolo

    def auxiliar_intercambiar(game, res, direc):
        ficha_res = game.tablero.todas_fichas[res]
        ficha_direc = game.tablero.todas_fichas[direc]
        tablero = game.tablero.tablero

        # Intercambiar símbolos en el tablero
        tablero[ficha_res.posicion[1]][ficha_res.posicion[0]] = ficha_direc.simbolo
        tablero[ficha_direc.posicion[1]][ficha_direc.posicion[0]] = ficha_res.simbolo

        # Intercambiar posiciones en las fichas
        ficha_res.intercambiar(ficha_direc)

    # Rotar
    if color == 'azul':
        for res, ficha in enumerate(self.tablero.todas_fichas):
            if ficha.color == "azul" and ficha.simbolo != 'R':
                simbolo_color = ficha.simbolo + 'AZUL'
                for key in recursos[simbolo_color].keys():
                    if key is not None and key != ficha.grado:
                        def accion_rotar(game, res=res, key=key):
                            game.tablero.todas_fichas[res].cambiar_grados(key)
                        accion_rotar.res = res
                        accion_rotar.key = key
                        list_acciones.append(accion_rotar)

    elif color == 'rojo':
        for res, ficha in enumerate(self.tablero.todas_fichas):
            if ficha.color == "rojo" and ficha.simbolo != 'r':
                simbolo_color = ficha.simbolo + 'ROJO'
                for key in recursos[simbolo_color].keys():
                    if key is not None and key != ficha.grado:
                        def accion_rotar(game, res=res, key=key):
                            game.tablero.todas_fichas[res].cambiar_grados(key)
                        list_acciones.append(accion_rotar)

    # Mover
    direcciones = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    if color == 'azul':
        for res, ficha in enumerate(self.tablero.todas_fichas):
            if ficha.color == "azul" and ficha.simbolo != 'L':
                for idx, direc in enumerate(direcciones):
                    posicion = ficha.posicion
                    siguiente_pos = (posicion[0] + direc[0], posicion[1] + direc[1])
                    if self.tablero.se_puede_mover("azul", siguiente_pos):
                        def accion_mover(game, res=res, direc=idx):
                            auxiliar_mover(game, res, direc)
                        accion_mover.res = res
                        accion_mover.direc = direc
                        list_acciones.append(accion_mover)
    elif color == 'rojo':
        for res, ficha in enumerate(self.tablero.todas_fichas):
            if ficha.color == "rojo" and ficha.simbolo != 'l':
                for idx, direc in enumerate(direcciones):
                    posicion = ficha.posicion
                    siguiente_pos = (posicion[0] + direc[0], posicion[1] + direc[1])
                    if self.tablero.se_puede_mover("rojo", siguiente_pos):
                        def accion_mover(game, res=res, direc=idx):
                            auxiliar_mover(game, res, direc)
                        list_acciones.append(accion_mover)

    # Intercambiar
    if color == 'azul':
        for res, fichai in enumerate(self.tablero.todas_fichas):
            if fichai.color == "azul" and fichai.simbolo == 'I':
                for direc, fichaj in enumerate(self.tablero.todas_fichas):
                    if fichai.es_intercambiable(fichaj):
                        def accion_intercambiar(game, res=res, direc=direc):
                            auxiliar_intercambiar(game, res, direc)
                        accion_intercambiar.res = res
                        accion_intercambiar.direc = direc
                        list_acciones.append(accion_intercambiar)
    elif color == 'rojo':
        for res, fichai in enumerate(self.tablero.todas_fichas):
            if fichai.color == "rojo" and fichai.simbolo == 'i':
                for direc, fichaj in enumerate(self.tablero.todas_fichas):
                    if fichai.es_intercambiable(fichaj):
                        def accion_intercambiar(game, res=res, direc=direc):
                            auxiliar_intercambiar(game, res, direc)
                        list_acciones.append(accion_intercambiar)

    return list_acciones
     
    
  def __es_ganador(self):
    for rey in self.tablero.reyes:
       if rey.eliminado:
            if rey.color == "azul":
                os.system('cls')
                print(recursos['GANAROJO'])
                input()
                menu.Menu().run()
            else:
                os.system('cls')
                print(recursos['GANAAZUL'])
                print('Nodos expandidos: ', self.CPU2.max_nodos)
                print('Profundidad del arbol: ', self.CPU2.max_depth)
                print('tiempo: ', time.time() - self.timer)
                input()
                menu.Menu().run()

  def __actualizar_laser(self):
    try:
      impactos = 0
      for laser in self.tablero.lasers: 
        laser.move()

        for rey in self.tablero.reyes:
          if rey.verificar_eliminacion(laser):
            laser.direccion = (0,0)
            self.tablero.limpiar_tablero()
            self.tablero.todas_fichas.remove(rey)
            #self.__main_loop(self.mode)
            raise StopIteration()


        for idx,defensor in enumerate(self.tablero.defensores):
          if defensor.posicion == laser.posicion:
            impactos += 1
            if defensor.verificar_eliminacion(laser):
                laser.direccion = (0,0)
                j,i = defensor.posicion
                self.tablero.posiciones_ocupadas.remove((j,i))
                self.tablero.defensores.pop(idx)
                self.tablero.tablero[i][j] = '.'
                self.tablero.limpiar_tablero()
                self.tablero.todas_fichas.remove(defensor)
                #self.__main_loop(self.mode)
                raise StopIteration()
            else:
                defensor.accion(laser)

        for idx,deflector in enumerate(self.tablero.deflectores):
          if deflector.posicion == laser.posicion:
            impactos += 1
            if deflector.verificar_eliminacion(laser):
                laser.direccion = (0,0)
                j,i = deflector.posicion
                self.tablero.posiciones_ocupadas.remove((j,i))
                self.tablero.deflectores.pop(idx)
                self.tablero.tablero[i][j] = '.'
                self.tablero.limpiar_tablero()
                self.tablero.todas_fichas.remove(deflector)
                #self.__main_loop(self.mode)
                raise StopIteration()
            else:
                deflector.accion(laser)
        
        for idx,intercambiador in enumerate(self.tablero.intercambiadores):
          if intercambiador.posicion == laser.posicion:
            impactos += 1
            intercambiador.accion(laser)
        self.impactos = impactos
        self.__dibujar_laser(laser)
    except StopIteration:
       pass
    
  def jugar(self, mode=1):
    self.mode = mode
    self.__main_loop(mode)