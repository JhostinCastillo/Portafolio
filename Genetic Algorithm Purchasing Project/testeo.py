import pandas as pd
import numpy as np
import copy 
import random
import json

def importar_ejercicio(ejercicios):
    dataframe = pd.read_excel(r'.\problemset\problemset.xlsx')
    cost_gasolina = float(dataframe['fuel_price'][ejercicios])
    lista_comp =  dataframe['query'].iloc[ejercicios]
    
    # Limpiando la data
    
    lista_comp = lista_comp.replace('[', '')
    lista_comp = lista_comp.replace(']', '')
    lista_comp = lista_comp.replace("'",'')
    
    # Convirtiendo a una lista
    
    lista_comp = lista_comp.split(',')
    for i in lista_comp[1:]:
        lista_comp[lista_comp.index(i)] = i[1:]
    
    # Importanddo las hojas de excel 
    
    catalogo = dataframe['catalog'].iloc[ejercicios] 
    catalogo = pd.read_excel(catalogo, sheet_name='catalogo')
    graph = dataframe['catalog'].iloc[ejercicios]
    graph = pd.read_excel(graph, sheet_name='grafo')
    
    return cost_gasolina, lista_comp, catalogo, graph

#########

def crear_matriz_distancia(graph):
    tiendas_unicas = graph['edge 1'].unique().tolist()
    matrix = pd.DataFrame(index=tiendas_unicas, columns=tiendas_unicas)
    for _, row in graph.iterrows():
        matrix.loc[row['edge 1'], row['edge 2']] = row['distance']

    for edge1 in matrix.index:
        for edge2 in matrix.columns:
            if pd.isna(matrix.loc[edge1, edge2]):
                if not pd.isna(matrix.loc[edge2, edge1]):
                    matrix.loc[edge1, edge2] = matrix.loc[edge2, edge1]
    ''' 
        Maestros, Me di cuenta que la diagonal principal estaba mal, Y agregue esta linea, para que la diagonal principal sea 0, Y se forme una grafo
        totalmente conexo. 

        Ademas a eso, habian valores faltantes, asi que los rellene tomando en cuenta los valores de rutas similares
        ejemplo de ruta similar, La Sirena a Casa hay una distancia de 4 pero de Casa a La Sirena no hay distancia, asi que se 
        toma la distancia de La Sirena a Casa.
    '''
    np.fill_diagonal(matrix.values, 0) 

    return matrix

##########

def creando_pobladores(n_pobladores):
    pobladores = []
    for n in range(n_pobladores):
        poblador = {'Casa':'[]'}
        productos = catalogo['product']
        aux = []
        for elemento in lista_comp:
            productos_filtrados = productos[productos == elemento]
            idx = np.random.choice(productos_filtrados.index)
            aux.append(catalogo['store'][idx] + "," + catalogo['product'][idx] + "," + str(catalogo['price'][idx]))

        for elemento in aux:
            list_elementos = elemento.split(',')
            poblador[list_elementos[0]] = []

        poblador['Precio'] = 0

        for elemento in aux:
            list_elementos = elemento.split(',')
            poblador[list_elementos[0]].append(list_elementos[1])
            poblador['Precio'] += float(list_elementos[2])
        pobladores.append(poblador)

    for poblador in pobladores:
        cost_viaje = 0
        keys = list(poblador.keys())[:-1]
        for tienda in range(len(keys)):
            if keys[tienda] != keys[-1]:
                cost_viaje += distance_matrix.at[keys[tienda], keys[tienda+1]]
                cost_viaje *= cost_gasolina 
                poblador["Precio"] += cost_viaje

        poblador["Precio"] += (distance_matrix.at[keys[-1], 'Casa'] * cost_gasolina)
    
    return pobladores

##########

def fitness(pobladores):
    pobladores_ordenados = sorted(pobladores, key=lambda x: x['Precio'])
    minimos_diferentes = []
    for item in pobladores_ordenados:
        if len(minimos_diferentes) < 2 and (not minimos_diferentes or item['Precio'] != minimos_diferentes[-1]['Precio']):
            minimos_diferentes.append(item)
    
    return minimos_diferentes

##########

def crossover(padre, madre, N):

    keys1 = list(padre.keys())
    keys2 = list(madre.keys())

    # Eliminar la clave 'Precio' de las listas de claves
    keys1.remove('Precio')
    keys2.remove('Precio')

    i = 0
    while i < len(keys1) and i < len(keys2):
        key1 = keys1[i]
        key2 = keys2[i]

        # Si cualquiera de los diccionarios se queda sin productos, detener el intercambio
        if not padre[key1] or not madre[key2]:
            break
        
        # Intercambiar los productos de las tiendas actuales
        padre[key1], madre[key2] = madre[key2], padre[key1]
        
        # Eliminar la clave de la lista si el diccionario ya no tiene más productos en esa tienda
        if not padre[key1]:
            keys1.remove(key1)
        if not madre[key2]:
            keys2.remove(key2)
        
        i += 1

    hijo1 = padre
    hijo2 = madre
    hijos = []
    
    for i in range(N):
        # Alternar entre hijo1 y hijo2
        if i % 2 == 0:
            base = copy.deepcopy(hijo1)
        else:
            base = copy.deepcopy(hijo2)
        
        # Obtener las claves de las tiendas, excluyendo 'Casa' y 'Precio'
        tiendas = [clave for clave in base.keys() if clave not in ['Casa', 'Precio']]
        
        # Si hay al menos dos tiendas, intercambiar productos entre dos tiendas aleatorias
        if len(tiendas) > 1:
            tienda1, tienda2 = random.sample(tiendas, 2)
            base[tienda1], base[tienda2] = base[tienda2], base[tienda1]
        
        # Agregar el nuevo hijo a la lista de hijos
        hijos.append(base)
    
    return hijos

###########

def actualizar_precios(lista_diccionarios, catalogo):
    for diccionario in lista_diccionarios:
        precio_total = 0
        
        for tienda, productos in diccionario.items():
            if tienda == 'Casa' or tienda == 'Precio':
                continue
            
            # Verificar si la tienda se encuentra en el catalogo
            if tienda in catalogo['store'].values:
                for producto in productos:
                    # Buscar el precio del producto en la tienda correspondiente
                    precio_producto = catalogo.loc[(catalogo['store'] == tienda) & 
                                                   (catalogo['product'] == producto), 'price']
                    if not precio_producto.empty:
                        precio_total += precio_producto.values[0]
        
        # Actualizar el precio total en el diccionario
        diccionario['Precio'] = precio_total
    
    for poblador in lista_diccionarios:
        cost_viaje = 0
        keys = list(poblador.keys())[:-1]
        for tienda in range(len(keys)):
            if keys[tienda] != keys[-1]:
                cost_viaje += distance_matrix.at[keys[tienda], keys[tienda+1]]
                cost_viaje *= cost_gasolina 
                poblador["Precio"] += cost_viaje

        poblador["Precio"] += (distance_matrix.at[keys[-1], 'Casa'] * cost_gasolina)
    
    return lista_diccionarios

###########

def validacion(lista_de_diccionarios):
    filtrada_lista_de_diccionarios = []

    for dic in lista_de_diccionarios:
        valido = True
        for tienda, productos in dic.items():
            if tienda == 'Precio' or tienda == 'Casa':
                continue
            for producto in productos:
                if not ((catalogo['product'] == producto) & (catalogo['store'] == tienda)).any():
                    valido = False
                    break
            if not valido:
                break
        if valido:
            filtrada_lista_de_diccionarios.append(dic)

    return filtrada_lista_de_diccionarios

"""#####################################################"""

cost_gasolina, lista_comp, catalogo, graph = importar_ejercicio (18)
distance_matrix = crear_matriz_distancia(graph)

pobladores = creando_pobladores(20) #<----

for iteracion in range(3):
    try:
        padre,madre = fitness(pobladores)
    
    except ValueError as e:
        pobladores = fitness(pobladores)
        break

    hijos = crossover(padre,madre,20) #<----
    nueva_generacion = actualizar_precios(hijos , catalogo)
    pobladores = validacion(nueva_generacion)
 
print("Esta es la mejor ruta para comprar:")
print(json.dumps(fitness(pobladores), indent=4, ensure_ascii=False))