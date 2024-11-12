from Recursos import recursos
from juego import Game
import time 
import os
import json
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from Busqueda.estructuras import Nodo

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

    def gameover(self, ganador):
        recurso = None
        if ganador == 'rojo':
            recurso = self.recursos['GANAROJO']
        elif ganador == 'azul':
            recurso = self.recursos['GANAAZUL']

        os.system('cls')
        print(recurso)
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
        
        modo_juego = int(modo)

        os.system('cls')
        self.mostrarniveles()
        nivel = input()

        while nivel not in ['1','2','3','4','5']:
            print('Opción no válida')
            nivel = input()

        match nivel:
            case '1':
                with open(ruta_base+r'tableros\ACE\ACE.txt', 'r') as archivo:
                    partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'tableros\ACE\inicio.json', 'r') as archivo:
                    inicio= json.load(archivo)

            case '2':
                with open(ruta_base+r'tableros\CURIOSITY\CURIOSITY.txt', 'r') as archivo:
                    partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'tableros\CURIOSITY\inicio.json', 'r') as archivo:
                    inicio= json.load(archivo)

            case '3':
                with open(ruta_base+r'tableros\GRAIL\GRAIL.txt', 'r') as archivo:
                    partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'tableros\GRAIL\inicio.json', 'r') as archivo:
                    inicio= json.load(archivo)

            case '4':

                with open(ruta_base+r'tableros\MERCURY\MERCURY.txt', 'r') as archivo:
                    partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'tableros\MERCURY\inicio.json', 'r') as archivo:
                    inicio= json.load(archivo)

            case '5':

                with open(ruta_base+r'tableros\SOPHIE\SOPHIE.txt', 'r') as archivo:
                    partida = [line.strip().split() for line in archivo.readlines()]

                with open(ruta_base+r'tableros\SOPHIE\inicio.json', 'r') as archivo:
                    inicio= json.load(archivo)



        game = Game(partida, inicio)
        os.system('cls')
        game.jugar(modo_juego)

            
                