from tablero import Tablero
from fichas import *
import time
import os
import menu
from copy import deepcopy
from recursos.Recursos import printdecoracion
from recursos.Recursos import recursos
from copy import deepcopy
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Busqueda.estructuras import Nodo
from Busqueda.funciones import ponderar

# Crear una manera de establecer la rotacion de las fichas sin que sea el usuario. 
# Puede ser mediante el archivo json

# Buscar una manera de que el usuario sepa la rotacion actual de todas las fichas cuando se imprima el tablero.

# Bloquear la seleccion de una pieza si esta se acaba

# Probar la nueva ficha Meta-Espejo


class Game:
  fichas = {'P':Plano,
            'C':Curvo,
            'D':Divisor,
            'me':MetaEspejo,
            'm':Meta,
            'S':CheckPoint,
            '#':Obstaculo,
            'L': Emisor}
  def __init__(self, partida, herramientas, inicio):
    self.partida = partida
    self.__herramientas_json = herramientas
    self.herramientas = list(herramientas.items())
    self.inicio = inicio
    self.tablero = Tablero(partida, inicio)
    self.__estado = None

# ----Funciones internas para algoritmos de busqueda

# Funcion de meta
  def __configurar_juego(self, estado):
    self.tablero.tablero = [['.' for elemento in sublista] for sublista in self.tablero.tablero]
    for simbolo, valores in estado.items():
      for valor in valores:
        if simbolo[0] in ['P','C','D']:
          ficha = self.fichas[simbolo[0]]((valor['j'], valor['i']), simbolo[-1])
          ficha.cambiar_grados(valor['grado'])
        else:
          ficha = self.fichas[simbolo]((valor['j'], valor['i']))
          ficha.cambiar_grados(valor['grado'])

        self.tablero.colocar_ficha(ficha,desbloqueo=True)
    self.__estado = estado
    #self.tablero.imprimir_tablero()

  def __jugar_estado(self):
    self.__iniciar_juego()
    while True:
      if self.__verificar_lasers():
        return False
        
      self.__actualizar_laser()
      if self.__es_ganador():
        return True
      
      
      

        

  def probar_estado(self, nodo):
    estado = nodo.dato[0]
    self.__configurar_juego(estado)
    return self.__jugar_estado()

# Funcion de expansion

  def generar_estados(self, nodo):
      """
      Genera todos los posibles estados que se pueden obtener a partir del estado dado,
      realizando un solo cambio por estado.

      :param state: Diccionario que representa el estado actual del juego.
      :return: Lista de tuplas (nuevo_estado, nuevo_herramientas) generados.
      """
      def calculo_peso(state):
        def calcular_heuristica_1(state):
            me_piezas = state.get('me', [])
            meta_piezas = []
            for pieza in ['P1', 'P2', 'D1', 'D2']:
                meta_piezas.extend(state.get(pieza, []))

            if not me_piezas or not meta_piezas:
                # Si no hay 'me' o no hay piezas de meta, la heurística no es aplicable
                return float('inf')

            me_pieza = me_piezas[0]  # Suponiendo que hay una pieza 'me'
            distancias = []
            for pieza in meta_piezas:
                dist_fila = abs(me_pieza['i'] - pieza['i'])
                dist_columna = abs(me_pieza['j'] - pieza['j'])
                distancia = min(dist_fila, dist_columna)
                distancias.append(distancia)

            h1 = sum(distancias) / len(distancias)
            return h1

        def calcular_heuristica_2(state):
            """
            Calcula la heurística 2 para el estado dado.

            :param state: Diccionario que representa el estado actual del juego.
            :return: Valor de la heurística 2.
            """
            checkpoints = state.get('S', [])
            meta_piezas = []
            for pieza in ['P1', 'P2', 'D1', 'D2']:
                meta_piezas.extend(state.get(pieza, []))

            if not checkpoints or not meta_piezas:
                # Si no hay checkpoints 'S' o no hay piezas de meta, la heurística no es aplicable
                return float('inf')

            distancias = []
            for checkpoint in checkpoints:
                for pieza in meta_piezas:
                    dist_fila = abs(checkpoint['i'] - pieza['i'])
                    dist_columna = abs(checkpoint['j'] - pieza['j'])
                    distancia = min(dist_fila, dist_columna)
                    distancias.append(distancia)

            h2 = sum(distancias) / len(distancias)
            return h2
        
        g = nodo.profundidad+1

        

        # Heurística 1
        h1 = calcular_heuristica_1(state)
        

        # Heurística 2
        h2 = calcular_heuristica_2(state)
        

        return ponderar([(h1,20),(h2,10)])+g
      

      state, herramientas = nodo.dato

      n = len(self.tablero.tablero)
      nuevos_estados = []
      max_i, max_j = (n,n)

      # Obtener posiciones ocupadas para evitar superposiciones
      posiciones_ocupadas = set()
      for piezas_lista in state.values():
          for pieza_info in piezas_lista:
              posiciones_ocupadas.add((pieza_info['i'], pieza_info['j']))

      # 1. Modificar piezas existentes
      for pieza, lista_piezas in state.items():
          # Piezas que no se pueden modificar
          if pieza in ['me', 'L', '#']:
              continue

          for index, pieza_info in enumerate(lista_piezas):
              # Piezas que solo pueden rotar
              if pieza == 'S':
                  grados_permitidos = [90, 180]
                  grados_nuevos = [g for g in grados_permitidos if g != pieza_info['grado']]
                  for nuevo_grado in grados_nuevos:
                      nuevo_estado = deepcopy(state)
                      nuevo_estado[pieza][index]['grado'] = nuevo_grado
                      nuevos_estados.append(Nodo((nuevo_estado, deepcopy(herramientas)),
                                                  peso=calculo_peso(nuevo_estado),
                                                  padre=nodo))
              # Piezas que pueden moverse y rotar
              elif pieza in ['P2', 'P1', 'D1', 'D2']:
                  grados_permitidos = [45, 135, 225, 315]
                  # Cambiar posición
                  for i in range(max_i):
                      for j in range(max_j):
                          if (i, j) != (pieza_info['i'], pieza_info['j']) and (i, j) not in posiciones_ocupadas:
                              nuevo_estado = deepcopy(state)
                              nuevo_estado[pieza][index]['i'] = i
                              nuevo_estado[pieza][index]['j'] = j
                              nuevos_estados.append(Nodo((nuevo_estado, deepcopy(herramientas)),
                                                          peso=calculo_peso(nuevo_estado),
                                                          padre=nodo))
                              # Solo un cambio, no combinamos con rotación

                  # Rotar pieza
                  grados_nuevos = [g for g in grados_permitidos if g != pieza_info['grado']]
                  for nuevo_grado in grados_nuevos:
                      nuevo_estado = deepcopy(state)
                      nuevo_estado[pieza][index]['grado'] = nuevo_grado
                      nuevos_estados.append(Nodo((nuevo_estado, deepcopy(herramientas)),
                                                  peso=calculo_peso(nuevo_estado),
                                                  padre=nodo))

      # 2. Agregar nuevas piezas desde las herramientas
      for pieza_herramienta, cantidad in herramientas.items():
          if cantidad > 0:
              # Definir grados permitidos
              if pieza_herramienta == 'S':
                  grados_permitidos = [90, 180]
              else:
                  grados_permitidos = [45, 135, 225, 315]

              for i in range(max_i):
                  for j in range(max_j):
                      if (i, j) not in posiciones_ocupadas:
                          for grado in grados_permitidos:
                              nuevo_estado = deepcopy(state)
                              nuevo_herramientas = deepcopy(herramientas)
                              # Decrementar la cantidad disponible de la herramienta
                              nuevo_herramientas[pieza_herramienta] -= 1
                              if nuevo_herramientas[pieza_herramienta] == 0:
                                  del nuevo_herramientas[pieza_herramienta]
                              # Agregar la nueva pieza
                              if pieza_herramienta not in nuevo_estado:
                                  nuevo_estado[pieza_herramienta] = []
                              nuevo_pieza_info = {'j': j, 'i': i, 'grado': grado}
                              nuevo_estado[pieza_herramienta].append(nuevo_pieza_info)
                              nuevos_estados.append(Nodo((nuevo_estado, nuevo_herramientas),
                                                          peso=calculo_peso(nuevo_estado),
                                                          padre=nodo))
                              # Solo un cambio, no agregamos más piezas
                          break  # Solo una posición por herramienta en esta iteración
                  else:
                      continue
                  break  # Salir si ya agregamos la pieza

      return nuevos_estados



# ------------------------------------



# ↗,↖,→,←,—,∖,∕,|,↕,⇖,⇗
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


  def __main_loop(self):
    
    self.tablero.imprimir_tablero()

    while True:
        if self.__verificar_todas_rototaciones():
          break
        else:
          self.__rotar_todas_fichas()

    accion = self.imprimir_herramientas()
    while accion != 'D':
      accion = self.imprimir_herramientas()
  
    self.__iniciar_juego()

    self.tablero.imprimir_tablero()
    while True:
      os.system('cls')

      self.tablero.imprimir_tablero()
      time.sleep(.7)
      if self.__verificar_lasers():
        menu.Menu().gameover_fail()
        break
      self.__actualizar_laser()
      if self.__es_ganador():
        menu.Menu().gameover()

  def __es_ganador(self):
    checklist = []
    if self.tablero.meta:
      for meta in self.tablero.meta:
        checklist.append(meta.completado)

    if self.tablero.checkpoints:
      for point in self.tablero.checkpoints:
        checklist.append(point.completado)

    if self.tablero.metaespejos:
      for point in self.tablero.metaespejos:
        checklist.append(point.completado)

    return all(checklist)
  
  def imprimir_herramientas(self, mode='Classic'):
    os.system('cls')
    self.tablero.get_analizar_tablero()
    self.tablero.imprimir_tablero()
    printdecoracion('herramientas','sup')
    print('Elige que quieres hacer')
    print('')

    while True:
      fichas = []

      for tupla in self.herramientas:
        if isinstance(tupla, list) or isinstance(tupla, tuple):
          fichas.append(list(tupla))

      for i,lista in enumerate(fichas):
        if type(lista) == list:
          if lista[1] == 0:
            fichas.pop(i)

      idx = 1
      for i, f in enumerate(fichas):
        i +=1 
        if type(f) == list:
          if 'P' in f[0]:
            simbolo = recursos['P'][45]
            print(f'[{i}] Colocar {simbolo} -- {f[1]} Disponibles')

          if 'D' in f[0]:
            simbolo = recursos['D'][45]
            print(f'[{i}] Colocar {simbolo} -- {f[1]} Disponibles')
          
          if 'C' in f[0]:
            simbolo = recursos['C'][45]
            print(f'[{i}] Colocar {simbolo} -- {f[1]} Disponibles')

          idx += i

      #####
      for i, ficha in enumerate(self.tablero.checkpoints):
        simbolo = recursos['S'][ficha.grado]
        print(f"[{i+idx}] Rotar 90º {simbolo} en {ficha.posicion}")
        fichas.append(ficha)
        idx += 1
    
      for i, ficha in enumerate(self.tablero.espejos):
        simbolo = recursos[ficha.simbolo[0]][ficha.grado]
        print(f"[{i+idx}] Rotar 90º {simbolo} en {ficha.posicion}")
        fichas.append(ficha)
        idx += 1

      simbolo = recursos[self.tablero.emisor.simbolo][self.tablero.emisor.grado]
      print(f"[{idx}] Rotar 90º {simbolo} en {self.tablero.emisor.posicion}")
      fichas.append(self.tablero.emisor)
      #####
      print('\033[31m[D] para disparar el láser\033[0m')
      printdecoracion('herramientas','inf')
      print("")
      r = input().upper()

      if r == 'D':
        return 'D'

      while not r.isnumeric():
        print('Opción no válida')
        r = input().upper()
        if r == 'D':
          return 'D'

      r = int(r)-1

      if r < len(fichas) and r >= 0:
        if type(fichas[r]) == list:
          ficha = fichas[r][0]
          fichas[r] = [ficha, fichas[r][1]-1]
          self.herramientas = fichas
          break
        else:
          fichas[r].rotar_90()
          return 'F'
      else:
        print("Debe seleccionar una de las opciones disponibles")
        return 'F'

    while True:
      print('')
      f = input('Seleccione la fila de la ficha: ')
      c = input('seleccione la columna de la ficha: ')

      while not f.isnumeric() or not c.isnumeric():
        print("Opción no válida")
        f = input('Seleccione la fila de la ficha: ')
        c = input('seleccione la columna de la ficha: ')

      f = int(f)
      c = int(c)

      if f < len(self.tablero.tablero) and f >= 0 and c < len(self.tablero.tablero) and c >= 0 and self.tablero.tablero[f][c] in ['.', '←', '→', '↑', '↓', '↖','↗','↙','↘']:
        break
      else: 
        print('Selección invalida')
        f = int(input('Seleccione la fila de la ficha: '))
        c = int(input('Seleccione la columna de la ficha: '))

    ficha = self.fichas[ficha[0]]((f,c), ficha[-1])
    self.tablero.colocar_ficha(ficha)
    return 'F'
  
  def __rotar_todas_fichas(self):
    os.system('cls')
    self.tablero.get_analizar_tablero()
    self.tablero.imprimir_tablero()
    printdecoracion('herramientas','sup')
    print('Asigna una rotación a las siguientes')
    print('fichas para poder continuar')
    print('')
    idx = 0
    fichas = []
    for i, ficha in enumerate(self.tablero.checkpoints):
      if ficha.grado is None:
        idx += 1
        print(f"[{idx}] \033[33mCheckPoint\033[0m en {ficha.posicion}")
        fichas.append(ficha)
    
    for i, ficha in enumerate(self.tablero.espejos):
      if ficha.grado is None:
        idx += 1
        print(f"[{idx}] \033[36mEspejo\033[0m en {ficha.posicion}")
        fichas.append(ficha)
    
    for i, ficha in enumerate(self.tablero.meta):
      if ficha.grado is None:
        idx += 1
        print(f"[{idx}] \033[97mMeta\033[0m en {ficha.posicion}")
        fichas.append(ficha)
    
    if self.tablero.emisor.grado is None:
      idx += 1
      print(f"[{idx}] \033[31mEmisor\033[0m en {self.tablero.emisor.posicion}")
      fichas.append(self.tablero.emisor)
    printdecoracion('herramientas','inf')
    
    r = int(input('Quiero asignar un grado a: '))

    while r > len(fichas)+1:
      print("No válido")
      r = int(input('Quiero asignar un grado a: '))

    if 'L' in fichas[r-1].simbolo:
      print("Elige el ángulo de disparo del Emisor: ")
      print(f"[0] --> {recursos['L'][0]}")
      print(f"[90] --> {recursos['L'][90]}")
      print(f"[180] --> {recursos['L'][180]}")
      print(f"[270] --> {recursos['L'][270]}")
      print()
      a = int(input())
    
    if 'P' in fichas[r-1].simbolo:
      print("Elige el ángulo de inclinacion del Espejo: ")
      print(f"[45] --> {recursos['P'][45]}")
      print(f"[135] --> {recursos['P'][135]}")
      print()
      a = int(input())
    
    if 'D' in fichas[r-1].simbolo:
      print("Elige el ángulo de inclinacion del Espejo: ")
      print(f"[45] --> {recursos['D'][45]}")
      print(f"[135] --> {recursos['D'][135]}")
      print()
      a = int(input())
    
    if 'S' in fichas[r-1].simbolo:
      print("Elige el ángulo deL ChekPoint: ")
      print(f"[0] --> {recursos['S'][0]}")
      print(f"[90] --> {recursos['S'][90]}")
      print()
      a = int(input())
    
    if 'm' in fichas[r-1].simbolo:
      print("Elige la orientaicón de la meta: ")
      print(f"[0] --> {recursos['m'][0]}")
      print(f"[90] --> {recursos['m'][90]}")
      print(f"[180] --> {recursos['m'][180]}")
      print(f"[270] --> {recursos['m'][270]}")
      print()
      a = int(input())

    fichas[r-1].grado = a

  def __verificar_todas_rototaciones(self): 
    checklist = []

    for espejo in self.tablero.espejos:
        if espejo.grado != None:
          checklist.append(True)
        else:
          checklist.append(False)
    
    for checkpoint in self.tablero.checkpoints:
        if checkpoint.grado != None:
          checklist.append(True)
        else:
          checklist.append(False)

    for meta in self.tablero.meta:
      if meta.grado != None:
          checklist.append(True)
      else:
          checklist.append(False)
    
    if self.tablero.emisor.grado != None:
      checklist.append(True)
    else:
      checklist.append(False)
    return all(checklist)

  def __iniciar_juego(self):
    laser = self.tablero.emisor.disparar()
    #laser.move()
    self.tablero.lasers.append(laser)
    return self.__dibujar_laser(laser)

  def __actualizar_laser(self):
    # print("Se activa la funcion AL")
    for laser in self.tablero.lasers: 
      laser.move()
      # print("Se mueve el laser a la posicion ", laser.posicion)
      for meta in self.tablero.meta:
        #print("Posicion de meta: ", meta.posicion)
        if laser.posicion == meta.posicion:
           meta.check(laser)

      if bool(self.tablero.checkpoints):
        for checkpoint in self.tablero.checkpoints:
          #print("Posicion de meta: ", meta.posicion)
          if laser.posicion == meta.posicion:
            checkpoint.check(laser)

      if bool(self.tablero.metaespejos):
        for metaespejo in self.tablero.metaespejos:
          #print("Posicion de meta: ", meta.posicion)
          if laser.posicion == metaespejo.posicion:
            metaespejo.check(laser)
            nLaser = metaespejo.reflejar(laser)
            laser.replace(nLaser)

      for espejo in self.tablero.espejos:
        # print("posicion del espejo ",espejo.simbolo, espejo.posicion)
        # input()
        #print("posicion espejo: ",espejo.posicion, "Grados del espejo: ", espejo.grado)
        if laser.posicion == espejo.posicion:
          if 'D' in espejo.simbolo:
            oldLaser, newLaser = espejo.reflejar(laser)
            laser.replace(oldLaser)
            if newLaser is not None:
              self.tablero.lasers.append(newLaser)
          else:
            nLaser = espejo.reflejar(laser)
            laser.replace(nLaser)

      
      self.__dibujar_laser(laser)

  def __verificar_lasers(self):
    estatus = []
    for laser in self.tablero.lasers:
      estatus.append(laser.direccion==(0,0))
    return all(estatus)
    
  def rotar_fichas(self):
    while True:
      print('Fichas disponibles para rotar:')
      for i, ficha in enumerate(self.tablero.espejos):
        print(f'[{i+1}] {ficha.simbolo} posicion {ficha.posicion[0]},{ficha.posicion[1]}. Grado actual: {ficha.grado}')
      r = input()
      r = int(r)-1

      if r < len(self.tablero.espejos) and r >= 0:
        break

    
    print(f'Usted selecciono la ficha {self.tablero.espejos[r].simbolo} en la posicion {self.tablero.espejos[r].posicion[0]}, {self.tablero.espejos[r].posicion[1]}, Grado actual: {self.tablero.espejos[r].grado}')
    while True:
      answer = input("Desea rotar la ficha 90 grados? [Y/N]").upper()

      if answer=='Y':
        self.tablero.espejos[r].rotar_90()
        print(f'Se ha rotado la ficha {self.tablero.espejos[r].simbolo} en la posicion {self.tablero.espejos[r].posicion[0]}, {self.tablero.espejos[r].posicion[1]}, Grado actual: {self.tablero.espejos[r].grado}')
      else:
        break

  def jugar(self):
    self.__main_loop()
