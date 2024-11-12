class Laser:
  """izquierda = (-1,0), derecha = (1,0), abajo = (0,1), arriba = (0,-1), arriba_izquierda = (-1,-1),
     arriba_derecha = (1,-1), abajo_izquierda = (-1,1), abajo_derecha = (1,1) """
  def __init__(self, direccion=(0,1), posicion=(0,0)):
    self.posicion = posicion
    self.direccion = direccion
    self.izquierda = '\033[92m←\033[0m'
    self.derecha = '\033[92m→\033[0m'
    self.arriba = '\033[92m↑\033[0m'
    self.abajo = '\033[92m↓\033[0m'
    self.arriba_izquierda = '\033[92m↖\033[0m'
    self.arriba_derecha = '\033[92m↗\033[0m'
    self.abajo_izquierda = '\033[92m↙\033[0m'
    self.abajo_derecha = '\033[92m↘\033[0m'
    
  def move(self):
    self.posicion = (self.posicion[0] + self.direccion[0], self.posicion[1] + self.direccion[1])

  def replace(self, laser):
    self = laser