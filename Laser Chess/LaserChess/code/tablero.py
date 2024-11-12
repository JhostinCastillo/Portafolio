from fichas import *
from laser import Laser
from Recursos import recursos, printdecoracion

class Tablero:

  def __init__(self, tablero, inicio):
    self.tablero = tablero
    self.emisores = []
    self.reyes = []
    self.deflectores = []
    self.intercambiadores = []
    self.defensores = []
    self.posiciones_ocupadas = []
    self.inicio = inicio
    self.__analizar_tablero()
    self.lasers = [None]
    self.todas_fichas = self.reyes + self.emisores + self.deflectores + self.intercambiadores + self.defensores
    self.helices = {'blancas':[(9,i) for i in range(0,7)]+[(1,0),(1,7)],
                    'rojas':[(0,i) for i in range(1,8)]+[(8,0),(8,7)]}
    
  def __obtener_color(self, x):
    return 'azul' if x.isupper() else 'rojo'

  def get_analizar_tablero(self):
    self.__analizar_tablero()

  def obtener_estado(self):
    estado = {}

    # Mapeo de símbolos y atributos según el tipo de ficha y color
    symbol_map = {
        'Deflector': ('D', 'd', 'grado'),
        'Defensor': ('F', 'f', 'grado'),
        'Intercambiador': ('I', 'i', 'grado'),
        'Emisor': ('L', 'l', 'grado'),
    }

    # Función auxiliar para procesar cada lista de objetos
    def procesar_fichas(lista_fichas, tipo_ficha):
        for ficha in lista_fichas:
            color = ficha.color
            simbolo = symbol_map[tipo_ficha][0] if color == 'azul' else symbol_map[tipo_ficha][1]
            atributo_grados = symbol_map[tipo_ficha][2]
            if simbolo not in estado:
                estado[simbolo] = []
            j, i = ficha.posicion
            grados = getattr(ficha, atributo_grados)
            estado[simbolo].append({'j': j, 'i': i, atributo_grados: grados})

    # Procesar cada lista de objetos
    procesar_fichas(self.deflectores, 'Deflector')
    procesar_fichas(self.defensores, 'Defensor')
    procesar_fichas(self.intercambiadores, 'Intercambiador')
    procesar_fichas(self.emisores, 'Emisor')

    return estado
  

  def __analizar_tablero(self, desbloqueo=False):
    # Configurar para detectar el equipo mediante mayusculas o minusculas
    if desbloqueo:
      self.reyes = []
      self.defensores = []
      self.intercambiadores = []
      self.deflectores = []
      self.emisores = []
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
          if celda in 'L l':
            emisor = Emisor(color=self.__obtener_color(celda))
            self.emisores.append(emisor)
            self.posiciones_ocupadas.append((j,i))
          elif celda in 'R r':
            rey = Rey((j, i), color=self.__obtener_color(celda))
            self.reyes.append(rey)
            self.posiciones_ocupadas.append((j,i))
          elif celda in 'F f':
            defensor = Defensor((j,i), color=self.__obtener_color(celda))
            configurar_inicio(defensor, celda, j, i)
            self.defensores.append(defensor)
            self.posiciones_ocupadas.append((j,i))
          elif celda in 'i I':
            intercambiador = Intercambiador((j,i), color=self.__obtener_color(celda))
            configurar_inicio(intercambiador, celda, j, i)
            self.intercambiadores.append(intercambiador)
            self.posiciones_ocupadas.append((j,i))
          elif celda in 'D d':
            deflector = Deflector((j,i), color=self.__obtener_color(celda))
            configurar_inicio(deflector, celda, j, i)
            self.deflectores.append(deflector)
            self.posiciones_ocupadas.append((j,i))      

  def colocar_ficha(self, ficha, desbloqueo=False):
    columna, fila = ficha.posicion
    try:
      self.tablero[fila][columna] = ficha.simbolo
    except IndexError:
      print(fila, columna, ficha.simbolo)
      raise IndexError
    self.__analizar_tablero(desbloqueo=desbloqueo)

  def modificar_ficha(self, ficha):
    pass

  def se_puede_mover(self, color, siguiente_pos):
    if siguiente_pos not in self.posiciones_ocupadas:
      if siguiente_pos[0] <= 9 and siguiente_pos[1] <= 7 and siguiente_pos[0] >= 0 and siguiente_pos[1] >= 0:
        if color == 'rojo' and siguiente_pos not in self.helices['blancas']:
            return True
        elif color == 'azul' and siguiente_pos not in self.helices['rojas']: 
            return True
    else: 
      return False
    
  def limpiar_tablero(self):
    for i, fila in enumerate(self.tablero):
      for j, celda in enumerate(fila):
        if celda not in ['L','l','R','r','F','f','I','i','D','d','.']:
          self.tablero[i][j] = '.'

  def imprimir_tablero(self):
    tableroHUD = [fila.copy() for fila in self.tablero]
    for i, fila in enumerate(tableroHUD):
      for j, celda in enumerate(fila):
        if celda == 'L' or celda == "l":
          for emisor in self.emisores:
            if emisor.posicion == (j,i):
              tableroHUD[i][j] = recursos[emisor.simbolo+emisor.color.upper()][emisor.grado]

        elif celda == '.':
          tableroHUD[i][j] = recursos['.']
        
        elif 'R' in celda or 'r' in celda:
          for rey in self.reyes:
            if rey.posicion == (j,i):
              print(i,j,rey.simbolo,rey.color)
              tableroHUD[i][j] = recursos[rey.simbolo+rey.color.upper()]
        
        elif 'D' in celda or "d" in celda:
          for deflector in self.deflectores:
            if deflector.posicion == (j,i):
              tableroHUD[i][j] = recursos[deflector.simbolo+deflector.color.upper()][deflector.grado]

        elif celda == 'F' or celda == 'f':
          for defensor in self.defensores:
            if defensor.posicion == (j,i):
              tableroHUD[i][j] = recursos[defensor.simbolo+defensor.color.upper()][defensor.grado]

        elif 'I' in celda or "i" in celda:
          for intercambiador in self.intercambiadores:
            if intercambiador.posicion == (j,i):
              tableroHUD[i][j] = recursos[intercambiador.simbolo+intercambiador.color.upper()][intercambiador.grado]   


    printdecoracion('tablero','sup',len(tableroHUD[0]))
    for fila in tableroHUD:
      print('   '.join(fila))
    printdecoracion('tablero','inf',len(tableroHUD[0]))
    print()