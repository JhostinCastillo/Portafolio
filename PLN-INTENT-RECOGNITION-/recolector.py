from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import urllib3
urllib3.disable_warnings()

options = Options()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--disable-extensions')
options.add_argument('--log-level=3')


class Recolector:
    def __init__(self, max_page, num_pages, games_x_page):
        self.__max_page = max_page
        self.__num_pages = num_pages
        self.__games_x_page = games_x_page

    def __titulos(self):
        titulos_f = []
        for page in np.random.choice(range(1,self.__max_page+1), self.__num_pages, replace=False):

            url = f'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page={page}'

            header = headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            html = requests.get(url, headers=header)

            soup = BeautifulSoup(html.text, 'html.parser')

            divs_titulos = soup.find_all('a', class_='c-finderProductCard_container g-color-gray80 u-grid')

            titulos = list(map(lambda x: x['href'],divs_titulos))

            titulos = np.random.choice(titulos, size=self.__games_x_page, replace=False).tolist()

            titulos_f += titulos

        return titulos_f
    

    def generar_datos(self):

        titulos_f = self.__titulos()

        reviews = ['Positive','Mixed','Negative']
        calificacion = []
        comentarios = []
        categoria = []
        juego = []
        for game in titulos_f:
            print(f'Titulo {titulos_f.index(game)+1}')
            for review in reviews:

                url = f'https://www.metacritic.com{game}user-reviews/?filter={review}%20Reviews'

                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

                # Abre una página web
                driver.get(url)

                # Espera a que se cargue el contenido dinámico si es necesario
                
                # Captura el contenido HTML de la página
                html = driver.page_source

                # Cierra el navegador
                driver.quit()

                #print(html.status_code)
                soup = BeautifulSoup(html, 'html.parser')

                divs_con_clase_especifica = soup.find_all('div', class_='c-siteReview g-bg-gray10 u-grid g-outer-spacing-bottom-large')


                calificacion_t = list(map(lambda x: x.find_all('span')[0].text, divs_con_clase_especifica))
                comentarios_t = list(map(lambda x: x.find_all('span')[1].text, divs_con_clase_especifica))
                categoria_t = [review]*len(calificacion_t)
                juego_t = [game]*len(calificacion_t)

                calificacion += calificacion_t
                comentarios += comentarios_t
                categoria += categoria_t
                juego += juego_t

        datos = pd.DataFrame({'comentarios':comentarios,
                      'calificacion': calificacion,
                      'categoria':categoria,
                      'juego': juego})

        datos.drop_duplicates(inplace=True, ignore_index=True)
        datos = datos[~datos['comentarios'].str.contains('SPOILER ALERT')].reset_index(drop=True)
        datos.to_excel('./datos/datos_recopilados.xlsx', index=False)
        