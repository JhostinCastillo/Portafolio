import numpy as np
import pandas as pd
import json
from transformers import AutoModel
from numpy.linalg import norm
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import ollama

class Asistente:
    def __init__(self):
        self.model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-es', trust_remote_code=True)

    def set_database(self, path='Manual-del-Empleadoembed.pdf', chunk_size=200, separator='.\n'):
        split = CharacterTextSplitter(chunk_size=chunk_size, separator=separator)
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        textos = [str(i.page_content) for i in split.split_documents(pages)]
        parrafos = pd.DataFrame(textos, columns=['texto'])

        # Convertir los embeddings a listas y luego a JSON
        parrafos['Embeddings'] = parrafos['texto'].apply(lambda x: json.dumps(self.model.encode(x).tolist()))
        parrafos.to_csv("EMBEDDINGS.csv", index=False)

    def __get_database(self):
        try:
            df = pd.read_csv("EMBEDDINGS.csv")

            # Convertir los embeddings de JSON a numpy arrays
            df['Embeddings'] = df['Embeddings'].apply(lambda x: np.array(json.loads(x), dtype=np.float32))
            return df
        except FileNotFoundError:
            return "No existe base de datos"

    def __cos_sim(self, a, b):
        return np.dot(a, b) / (norm(a) * norm(b))

    def __buscar(self, busqueda, datos, n_resultados=5):
        busqueda_embed = self.model.encode(busqueda)
        datos['Similitud'] = datos['Embeddings'].apply(lambda x: self.__cos_sim(x, busqueda_embed))
        datos = datos.sort_values('Similitud', ascending=False)
        return datos.iloc[:n_resultados][['texto', 'Similitud', 'Embeddings']]

    def __get_context(self, pregunta):
        a = self.__buscar(pregunta, self.__get_database())
        contexto = a.reset_index(drop=True)['texto'][0]
        return contexto

    def chat(self, pregunta):
        contexto = self.__get_context(pregunta)
        mensaje = (f"""Eres un asistente virtual en la corporación La Asociación Pro-Desarrollo Comunal del Patio Inc
                   Estás enfocada en asistir a los empleados de la corporación en sus dudas del día a día
                   responde tomando esto como contexto: {contexto}. No alucines, responde corto y claro
                   Sabiendo esto, responde la siguiente pregunta del usuario: {pregunta}""")

        mensajes = [{'role': 'user', 'content': mensaje}]
        respuesta = ollama.chat(model='llama3.1:latest', messages=mensajes)
        return respuesta['message']['content']