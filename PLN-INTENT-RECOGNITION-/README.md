# PLN-INTENT-RECOGNITION-
Este repositorio será usado con la finalidad de desarrollar el segundo proyecto  "INTENT RECOGNITION" de la materia de Procesamiento del Lenguaje Natural.

## Instrucciones
En este proyecto desarrollarán un pipeline para recolectar reviews de una página web o de un dataset, y con esta data crear un modelo usando NLTK y Scikit-Learn para 
reconocimiento de intención.

### 1. *Recoleccion de datos:*
  a.  En este proyecto desarrollarán un pipeline para recolectar reviews de una página web y con esta data crear un modelo usando      NLTK     y Scikit-Learn para reconocimiento de intención que permita devolver predicciones a través de un API. 

### 1. *Preparación de la data/ preprocesamiento la data:*
  a.	Va a aplicar las técnicas de preprocesamiento del lenguaje que optimicen más su modelo como la tokenización, lematización, uso   de palabras frecuentes, etc. 
  
  b.	Después de limpiar el texto realizará una ingeniería de características para vectorizar la información como se documenta en el   acápite 3. 

### 3. *Entrenamiento del modelo:* 
  a.	División del dataset en entradas y salidas/etiquetas (x, y). 
  
  b.	División del dataset en entrenamiento y testeo. 

  c.	Entrenamiento de cada algoritmo con el dataset. 

### 4. *Validación y testeo del modelo:* 
  a.	Análisis de performance (métricas de rendimiento) 
  
  b.	Selección de algoritmo óptimo. 

## Requerimientos de la entrega
*Va a buscar una página web con los siguientes requerimientos:*

a.	Debe tener al menos 1000 reviews, cada uno con su puntuación. 

b.  La etiqueta de salida debe ser de tipo categórica. 

c.  Debe evitar el mayor sesgo por lo que trate de que los reviews estén lo más equilibrados posibles en cantidad por clase. 

d.	La etiqueta puede ser de 2 o más clases. 
* Ejemplo: 
  
  - Positivo o Negativo
    
  -	Positivo, Negativo o Neutral o Spam o No Spam o Aprobado o Reprobado o Música, Película, Pintura o Ciencia
  
e.  Debe entregar todas las fuentes del proyecto, incluyendo un cuaderno de Jupyter con el código fuente con el se entrenaron los modelos y se hicieron las pruebas. 

f.  Debe entrenar los siguientes modelos de clasificación con el dataset: 

  - KNearest Neighbors Classifier o Random Forest Classifier o Decision Tree Classifier o Naive Bayes Classifier o MultinomialNB 
  	AdaBoostClassifier 
   
g.	Debe mostrar las métricas de rendimiento de cada uno de los modelos. 

h.	Se debe poder hacerle pruebas a cada uno de los modelos ingresando un texto.

i.	Las fuentes deben estar debidamente documentadas con docstrings y anotaciones. 

j.  Debe entregar un documento de infraestructura del proyecto que contenga: 
  -	Gráficas analíticas de modelo (EDA). 
      
  -  Proporción de testeo/entrenamiento. 
      
  -  Descripción de algoritmos empleados. 
      
  -  Hiperparámetros usados en los modelos. 
      
  -  Matriz de confusión de modelos. 
      
  -  Estadísticas de modelos. 
      
  -  Explicación de cómo funciona el sistema de clasificación creado. 

### Colaboradores
- [Kevin Soler](https://www.linkedin.com/in/kevin-soler-887a28130?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
- [Anwar Julian](https://github.com/Anexty113)





