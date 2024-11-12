
from laser import Laser

class Ficha:
  def __init__(self, posicion):
    self.posicion = posicion
    self.grado = None

  def cambiar_grados(self,ngrado):
    self.grado = ngrado

  def rotar_45(self):
    self.grado += 45
    if self.grado >= 360:
      self.grado = self.grado % 360

  def rotar_90(self):
    self.grado += 90
    if self.grado >= 360:
      self.grado = self.grado % 360


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

  def __init__(self, posicion, tipo):
    super().__init__(posicion)
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

  def reflejar(self, laser):
    reflexion = self._obtener_reflexion(laser)
    laser.direccion = reflexion
    return laser

  def cambiar_tipo(self, tipo):
    self.tipo = 'simple' if self.tipo == 'doble' else 'doble'



class Plano(Espejo):
  def __init__(self, posicion, tipo):
    super().__init__(posicion, tipo)
    self.simbolo = 'P'+tipo

  def _calcular_reflexion(self, laser):
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


class Curvo(Espejo):
  def __init__(self, posicion, tipo, curvatura='arriba'):
    if curvatura not in ['arriba', 'abajo']:
      raise ValueError("La curvatura debe ser 'arriba' o 'abajo'.")
    super().__init__(posicion, tipo)
    self.curvatura = curvatura
    self.simbolo = 'C'+tipo

  def _calcular_reflexion(self, laser):
    desvio = -1 if self.curvatura == 'arriba' else 1
    if self.grado in [0,180]:
      if 0 in laser.direccion:
        reflexion = desvio, laser.direccion[0] * -1
      else:
        reflexion = 0, laser.direccion[1] * -1

    elif self.grado in [90,270]:
      if 0 in laser.direccion:
        reflexion = laser.direccion[0] * -1, desvio
      else:
        reflexion = laser.direccion[0] * -1, 0

    elif self.grado in [45,135,225,315]:
      if 0 not in laser.direccion:
        reflexion = laser.direccion[0] * -1, laser.direccion[1] * -1
      else:
        reflexion = laser.direccion[1], laser.direccion[0]

    return reflexion

  def cambiar_curvatura(self):
    self.curvatura = 'arriba' if self.curvatura == 'abajo' else 'abajo'


class Divisor(Plano):
  def __init__(self, posicion, tipo):
    super().__init__(posicion, tipo)
    self.simbolo = 'D'+tipo
    self._laserattr = None

  def _crear_laser(self, laser):
    reflexion = self._obtener_reflexion(laser)
    if reflexion != (0,0):
      direccion = laser.direccion
      posicion = laser.posicion
      self._laserattr = (direccion, posicion)


  def reflejar(self, laser):
    self._crear_laser(laser)
    if self._laserattr is not None:
      direccion, posicion = self._laserattr
      oldLaser = super().reflejar(laser)
      newLaser = Laser(direccion, posicion)
      return oldLaser, newLaser
    else:
      oldLaser = super().reflejar(laser)
      return oldLaser, None
  

class Emisor(Ficha):
  def __init__(self, posicion):
    super().__init__(posicion)
    self.simbolo = 'L'
    self.obtener_direccion()

  def disparar(self):
    self.obtener_direccion()
    laser = Laser(direccion= self.direccion, posicion=self.posicion)
    return laser

  def obtener_direccion(self):
    if self.grado == 0:
      self.direccion = (0,1)
    elif self.grado == 90:
      self.direccion = (1,0)
    elif self.grado == 180:
      self.direccion = (0,-1)
    elif self.grado == 270:
      self.direccion = (-1,0)
    elif self.grado == 45:
      self.direccion = (1,-1)
    elif self.grado == 135:
      self.direccion = (-1,-1)
    elif self.grado == 225:
      self.direccion = (-1,1)
    elif self.grado == 315:
      self.direccion = (1,1)


class MetaCara(Ficha):
  def __init__(self, posicion):
    super().__init__(posicion)
    self.completado=False
    self.simbolo = 'k'

  def check(self, laser):
    if laser.posicion == self.posicion:
      if self.grado == 0 and laser.direccion == (0,-1):
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 180 and laser.direccion == (0,1):
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 90 and laser.direccion == (-1,0):
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 270 and laser.direccion == (1,0):
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 45 and laser.direccion == (-1,-1): 
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 135 and laser.direccion == (-1,1): 
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 225 and laser.direccion == (1,1): 
        self.completado = True
        laser.direccion = (0,0)
      elif self.grado == 315 and laser.direccion == (1,-1): 
        self.completado = True
        laser.direccion = (0,0)
      else:
        self.completado = False
    else:
      self.completado = False

    return self.completado

class Meta(Ficha):
  def __init__(self, posicion):
    super().__init__(posicion)
    self.completado=False
    self.simbolo = 'm'

  def check(self, laser):
    if laser.posicion == self.posicion:
      laser.direccion = (0,0)
      self.completado = True
      return self.completado
    

class MetaEspejo(Plano):
  def __init__(self, posicion):
    super().__init__(posicion, tipo='1')
    self.simbolo = 'me'
    self.completado = False

  def check(self, laser):
    direccion = self._obtener_reflexion(laser)
    if laser.posicion == self.posicion and direccion==(0,0):
      self.completado = True
      return self.completado
    

  # def check(self, laser):
  #   if laser.posicion == self.posicion:
  #     laser.direccion = (0,0)
  #     self.completado = True
  #     return self.completado

class CheckPoint(Ficha):
  def __init__(self, posicion):
    super().__init__(posicion)
    self.completado=False
    self.simbolo = 'S'

  def check(self, laser):
    if self.grado in [0, 180] and laser.direccion[0] == 0:
      self.completado = True
    elif self.grado in [90, 270] and laser.direccion[1] == 0:
      self.completado = True
    elif self.grado in [45, 225] and laser.direccion in [(-1,-1),(1,1)]:
      self.completado = True
    elif self.grado in [135, 315] and laser.direccion in [(-1,1),(1,-1)]:
      self.completado = True
    else:
      self.completado = False

    return self.completado
  

class Obstaculo(Ficha):
  def __init__(self, posicion):
    super().__init__(posicion)
    self.simbolo = '#'

