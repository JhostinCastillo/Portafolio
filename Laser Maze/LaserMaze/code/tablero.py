from fichas import *
from laser import Laser
from recursos.Recursos import recursos, printdecoracion

class Tablero:
  
  def __init__(self, tablero, inicio):
    self.tablero = tablero
    self.inicio = inicio
    self.emisor = None
    self.meta = []
    self.espejos = []
    self.obstaculos = []
    self.checkpoints = []
    self.posiciones_ocupadas = []
    self.metaespejos = []
    self.__analizar_tablero()
    self.lasers = []
    
    

  def get_analizar_tablero(self):
    self.__analizar_tablero()

  def __analizar_tablero(self, desbloqueo=False):
    if desbloqueo:
      self.meta = []
      self.obstaculos = []
      self.checkpoints = []
      self.espejos = []
      self.posiciones_ocupadas = []

    def configurar_inicio(ficha, simbolo, j, i):
      cambios = self.inicio.get(simbolo)
      if cambios is not None:
        for cambio in cambios:
          ji, ii, grado = cambio.values()
          if j==ji and i==ii:
            ficha.cambiar_grados(grado)

    for i, fila in enumerate(self.tablero):
      for j, celda in enumerate(fila):
        if (j,i) not in self.posiciones_ocupadas:
          if celda == 'L':
            emisor = Emisor((j, i))
            configurar_inicio(emisor, 'L', j, i)
            self.emisor = emisor
            self.posiciones_ocupadas.append((j,i))
          elif celda == 'm':
            meta = Meta((j, i))
            configurar_inicio(meta, 'm', j, i)
            self.meta.append(meta)
            self.posiciones_ocupadas.append((j,i))
          elif celda == 'me':
            metaespejo = MetaEspejo((j,i))
            configurar_inicio(metaespejo, 'me', j, i)
            self.metaespejos.append(metaespejo)
            self.posiciones_ocupadas.append((j,i))
          elif 'P' in celda:
            self.espejos.append(Plano((j,i), celda[-1]))
            self.posiciones_ocupadas.append((j,i))
          elif 'C' in celda:
            self.espejos.append(Curvo((j,i), celda[-1]))
            self.posiciones_ocupadas.append((j,i))
          elif 'D' in celda:
            self.espejos.append(Divisor((j,i), celda[-1]))
            self.posiciones_ocupadas.append((j,i))
          elif celda == '#':
            self.obstaculos.append(Obstaculo((j,i)))
            self.posiciones_ocupadas.append((j,i))
          elif celda == 'S':
            self.checkpoints.append(CheckPoint((j,i)))
            self.posiciones_ocupadas.append((j,i))

  def colocar_ficha(self, ficha, desbloqueo=False):
    fila, columna = ficha.posicion
    self.tablero[fila][columna] = ficha.simbolo
    self.__analizar_tablero(desbloqueo=desbloqueo)

  def modificar_ficha(self, ficha):
    pass

  def imprimir_tablero(self):
    tableroHUD = [fila.copy() for fila in self.tablero]
    for i, fila in enumerate(tableroHUD):
      for j, celda in enumerate(fila):
        if celda == 'L':
          tableroHUD[i][j] = recursos['L'][self.emisor.grado]

        elif celda == '.':
          tableroHUD[i][j] = recursos['.']
        
        elif 'P' in celda:
          for espejo in self.espejos:
            if espejo.posicion == (j,i):
              tableroHUD[i][j] = recursos['P'][espejo.grado]
        
        elif 'D' in celda:
          for espejo in self.espejos:
            if espejo.posicion == (j,i):
              tableroHUD[i][j] = recursos['D'][espejo.grado]

        elif celda == 'm':
          for meta in self.meta:
            if meta.posicion == (j,i):
              tableroHUD[i][j] = recursos['m'][meta.grado]

        elif 'S' in celda:
          for checkpoint in self.checkpoints:
            if checkpoint.posicion == (j,i):
              tableroHUD[i][j] = recursos['S'][checkpoint.grado]   

        elif celda == 'me':
          for metaespejo in self.metaespejos:
            if metaespejo.posicion == (j,i):
              tableroHUD[i][j] = recursos['me'][metaespejo.grado]

        # elif 'C' in celda:
        #   self.espejos.append(Curvo((j,i), celda[-1]))

        elif celda == '#':
          tableroHUD[i][j] = recursos['#']

    printdecoracion('tablero','sup',len(tableroHUD[0]))
    for fila in tableroHUD:
      print('   '.join(fila))
    printdecoracion('tablero','inf',len(tableroHUD[0]))
    print()

