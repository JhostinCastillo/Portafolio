from recursos.Recursos import recursos
from juego import Game
import time 
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Busqueda.estructuras import Nodo

class Menu:
    def __init__(self):
        self.recursos = recursos

    def mostrarlogo(self):
        print(self.recursos['LOGO1'])
        time.sleep(0.3)
        print(self.recursos['LOGO2'])

    def mostrarmodos(self):
        print(self.recursos['MODOS'])

    def mostrarniveles(self):
        print(self.recursos['NIVELES'])

    def gameover(self):
        os.system('cls')
        print(self.recursos['COMPLETADO'])
        opcion = input('Presiona [S] para salir o cualquier tecla para jugar de nuevo').upper()

        if opcion == 'S':
            sys.exit()
        else:
            Menu().run()


    def gameover_fail(self):
        os.system('cls')
        print(self.recursos['PERDIDO'])
        opcion = input('Presiona [S] para salir o cualquier tecla para jugar de nuevo').upper()

        if opcion == 'S':
            sys.exit()
        else:
            Menu().run()

    def run(self):
        ruta_base = os.getcwd().replace("\\code","\\")

        os.system('cls')
        time.sleep(.5)

        self.mostrarlogo()
        time.sleep(0.4)
        self.mostrarmodos()
        modo = input()

        while modo not in ['1','2','3']:
            print('Opción no válida')
            modo = input()

        match modo:
            case '1':
                os.system('cls')
                self.mostrarniveles()
                nivel = input()

                while nivel not in ['1','2','3','4','5','6','7','8','9','10','11','12']:
                    print('Opción no válida')
                    nivel = input()
                
                match nivel:
                    case '1':
                        ## Rutas para Kevin: '../niveles/tableros/nivel_1.txt' , '../niveles/herramientas/nivel_1.json '
                        ## Rutas para Jhostin: 'JuegosInteligentes/LaserMaze/niveles/tableros/nivel_1.txt' , 'JuegosInteligentes/LaserMaze/niveles/herramientas/nivel_1.json'

                        with open(ruta_base+r'niveles\nivel1\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel1\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel1\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '2':
                        with open(ruta_base+r'niveles\nivel2\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel2\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel2\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '3':
                        with open(ruta_base+r'niveles\nivel3\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel3\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel3\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)
                    
                    case '4':

                        with open(ruta_base+r'niveles\nivel4\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel4\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel4\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '5':

                        with open(ruta_base+r'niveles\nivel5\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel5\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel5\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '6':

                        with open(ruta_base+r'niveles\nivel6\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel6\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel6\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)
                    
                    case '7':
                        ## Rutas para Kevin: '../niveles/tableros/nivel_1.txt' , '../niveles/herramientas/nivel_1.json '
                        ## Rutas para Jhostin: 'JuegosInteligentes/LaserMaze/niveles/tableros/nivel_1.txt' , 'JuegosInteligentes/LaserMaze/niveles/herramientas/nivel_1.json'

                        with open(ruta_base+r'niveles\nivel7\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel7\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel7\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '8':
                        with open(ruta_base+r'niveles\nivel8\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel8\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel8\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '9':
                        with open(ruta_base+r'niveles\nivel9\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel9\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel9\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)
                    
                    case '10':

                        with open(ruta_base+r'niveles\nivel10\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel10\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel10\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '11':

                        with open(ruta_base+r'niveles\nivel11\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel11\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel11\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                    case '12':

                        with open(ruta_base+r'niveles\nivel12\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                        with open(ruta_base+r'niveles\nivel12\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                        with open(ruta_base+r'niveles\nivel12\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                

                game = Game(partida, herramientas, inicio)
                os.system('cls')
                game.jugar()

            case '2':
                os.system('cls')
                print('Modo custom en desarrollo')
                time.sleep(2)

            case '3':
                with open(ruta_base+r'niveles\nivel1\tablero.txt', 'r') as archivo:
                            partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'niveles\nivel1\herramientas.json', 'r') as archivo:
                            herramientas = json.load(archivo)

                with open(ruta_base+r'niveles\nivel1\inicio.json', 'r') as archivo:
                            inicio = json.load(archivo)

                estado1 = {'L':[{'j':0, 'i':0, 'grado':None}], 
                            'm':[{'j':3, 'i':2, 'grado':None}],
                            'P2':[{'j':1, 'i':2, 'grado':None}],
                            'D2':[{'j':4, 'i':2, 'grado':None}]}
                
                game = Game(partida, herramientas, inicio)
                os.system('cls')
                nodo = Nodo((estado1, herramientas), peso=0)
                print(game.probar_estado(nodo))
                print(game.generar_estados(nodo))
                