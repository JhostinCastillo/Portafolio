
from laser import Laser
import math

class Ficha:
  def __init__(self, posicion, color):
    self.posicion = posicion
    self.color = color
    self.grado = None
    self.eliminado = False
    self.puntos=0

  def cambiar_grados(self,ngrado):
    "Asignar grados especificos"
    self.grado = ngrado

  def rotar(self):
    "Rota la ficha 90º"
    self.grado += 90
    if self.grado >= 360:
      self.grado = self.grado % 360
  
  def mover(self,direccion):
    "Mover la ficha a una casilla adyacente si es posible"
    siguiente_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
    self.posicion = siguiente_posicion
    
class Espejo(Ficha):
  espejos = {'1': 'simple',
             '2': 'doble'}
  caras = {
        'simple':
     {0: [(1,0), (-1,0), (0,1),(1,1), (-1,1)],
      45: [(1,0), (1,1), (1,-1), (0,1), (-1,1)],
      90: [(0,-1), (0,-1), (1,0), (1,-1), (1,1)],
      135: [(1,0),(1,-1),(1,1),(-1,-1),(0,-1)], #\
      180: [(1,0), (-1,0), (0,-1),(1,-1), (-1,-1)],
      225: [(-1,0), (0,-1), (-1,-1),(-1,1),(1,-1)], #/
      270: [(0,-1), (0,-1), (-1,0),(-1,-1),(-1,1)],
      315: [(0,1),(-1,0),(-1,-1),(1,1),(-1,1)]},
        'doble':
      {0: [(1,0), (-1,0)],
      45: [(1,-1), (-1,1)],
      90: [(0,1), (0,-1)],
      135: [(1,1),(-1,-1)], #\
      180: [(1,0), (-1,0)],
      225: [(-1,1),(1,-1)], #/
      270: [(0,1), (0,-1)],
      315: [(1,1),(-1,-1)]},
        } #\

  def __init__(self, posicion, color, tipo):
    super().__init__(posicion,color)
    self.tipo = self.espejos[tipo]
    self.simbolo = 'E'+tipo
    self.grado = 135

  def _calcular_reflexion(self, laser):
    return (0,0)

  def _obtener_reflexion(self, laser):
    if laser.direccion in self.caras[self.tipo][self.grado]:
      reflexion = (0,0)
    else:
      reflexion = self._calcular_reflexion(laser)

    return reflexion

  def accion(self, laser):
    "Cambia la direccion del laser a 90º"
    reflexion = self._obtener_reflexion(laser)
    laser.direccion = reflexion
    return laser

class Deflector(Espejo):
  def __init__(self, posicion, color):
    super().__init__(posicion, color, tipo='1')
    self.simbolo = 'D' if color == 'azul' else "d"
    self.puntos = 2

  def _calcular_reflexion(self, laser):
    reflexion = None
    if self.grado in [135,315]:
      if 0 not in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      else:
        reflexion = laser.direccion[1], laser.direccion[0]

    elif self.grado in [45,225]:
      if 0 not in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      elif laser.direccion[0]==0:
        reflexion = laser.direccion[1]*-1, laser.direccion[0]
      else:
        reflexion = laser.direccion[1], laser.direccion[0]*-1
    return reflexion

  def verificar_eliminacion(self, laser):
    "return True si la ficha fue eliminada"
    direccion = self._obtener_reflexion(laser)
    if laser.posicion == self.posicion and direccion==(0,0):
      self.eliminado = True
      return self.eliminado
    
class Defensor(Ficha):
  def __init__(self, posicion, color):
    super().__init__(posicion, color)
    self.simbolo = 'F' if color == 'azul' else "f"
    self.puntos = 4

  def accion(self,laser):
    "Frena el laser"
    if laser.posicion == self.posicion:
      if self.grado == 90 and laser.direccion == (0,1):
        laser.direccion = (0,0)
      elif self.grado == 0 and laser.direccion == (-1,0):
        laser.direccion = (0,0)
      elif self.grado == 180 and laser.direccion == (1,0):
        laser.direccion = (0,0)
      elif self.grado == 270 and laser.direccion == (0,-1):
        laser.direccion = (0,0)

  def verificar_eliminacion(self,laser):
    "Return True si la ficha fue eliminada"
    if laser.posicion == self.posicion:
      if self.grado == 0 and laser.direccion == (-1,0):
        self.eliminado = False
      elif self.grado == 180 and laser.direccion == (1,0):
        self.eliminado = False
      elif self.grado == 90 and laser.direccion == (0,1):
        self.eliminado = False
      elif self.grado == 270 and laser.direccion == (0,-1):
        self.eliminado = False
      else:
        self.eliminado = True
    else:
      self.eliminado = False

    return self.eliminado

class Rey(Ficha):
  def __init__(self,posicion, color):
    super().__init__(posicion, color)
    self.simbolo = 'R' if color == 'azul' else "r"
  
  def verificar_eliminacion(self,laser):
    "Return True si la ficha fue eliminada"
    if laser.posicion == self.posicion:
      self.eliminado = True
      return self.eliminado

class Emisor():
  def __init__(self, color):
   self.color = color
   self.posicion = self.__obtener_posicion()
   self.grado = self.__obtener_grado_inicial()
   self.direccion = self.__obtener_direccion
   self.simbolo = "L" if color == 'azul' else "l"
   self.puntos = 0

  def cambiar_grados(self,ngrado):
    "Asignar grados especificos"
    self.grado = ngrado

  def __obtener_grado_inicial(self):
    if self.color == 'rojo':
      return 270
    
    elif self.color == 'azul':
      return 90

  def __obtener_posicion(self):
    if self.color == 'rojo':
      return (0,0)  
    elif self.color == 'azul':
      return (9,7)
    else:
      raise ValueError

  def rotar(self):
    if self.grado == 90:
      self.grado += 90
    elif self.grado == 180:
      self.grado -= 90
    elif self.grado == 270:
      self.grado -= 270
    elif self.grado == 0:
      self.grado += 270

  def accion(self):
    self.__obtener_direccion()
    laser = Laser(direccion= self.direccion, posicion=self.posicion)
    return laser

  def __obtener_direccion(self):
    if self.grado == 0:
      self.direccion = (1,0)
    elif self.grado == 90:
      self.direccion = (0,-1)
    elif self.grado == 180:
      self.direccion = (-1,0)
    elif self.grado == 270:
      self.direccion = (0,1)


class Intercambiador(Espejo):
  def __init__(self, posicion, color):
    super().__init__(posicion, color, tipo='2')
    self.simbolo = 'I' if color == 'azul' else "i"

  def _calcular_reflexion(self, laser):
    reflexion = None
    if self.grado in [0,180]:
      if 0 in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      else:
        reflexion = laser.direccion[0], laser.direccion[1] * -1

    elif self.grado in [90,270]:
      if 0 in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      else:
        reflexion = laser.direccion[0] * -1, laser.direccion[1]

    elif self.grado in [135,315]:
      if 0 not in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      else:
        reflexion = laser.direccion[1], laser.direccion[0]

    elif self.grado in [45,225]:
      if 0 not in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      elif laser.direccion[0]==0:
        reflexion = laser.direccion[1]*-1, laser.direccion[0]
      else:
        reflexion = laser.direccion[1], laser.direccion[0]*-1
        # (1,0) (-0,1) / (-1,0) (-0,-1)

    return reflexion
  
  def intercambiar(self, ficha):
    "Intercambia su posicion con la de una ficha adyasente"

    if self.es_intercambiable(ficha):
      temp_posicion = ficha.posicion
      ficha.posicion = self.posicion
      self.posicion = temp_posicion
      
    
  def es_intercambiable(self, ficha):
    "Verifica si la ficha se puede intercambiar o no"
    intercambiables = ['D','F','d','f']
    return (ficha.simbolo in intercambiables) and self.es_vecino(ficha)

  def es_vecino(self, ficha):
    "Verifica si una ficha es vecino"
    x1, y1 = self.posicion
    x2, y2 = ficha.posicion
    distancia = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
    return distancia<1.5