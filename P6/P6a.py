from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Rutas de los archivos de entrada
archivo_entrada_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
archivo_entrada_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
archivo_entrada_all_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_reducida_truncado_all.txt'
archivo_entrada_query_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_reducida_truncado_query.txt'
# Rutas de los archivos de salida
archivo_salida_tf = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P6\\Salidas\\CACM_tf_rels.txt'
archivo_salida_tfidf = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P6\\Salidas\\CACM_tfidf_rels.txt'
archivo_salida_tf_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P6\\Salidas\\CACM_tf_rels_reducido.txt'
archivo_salida_tfidf_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P6\\Salidas\\CACM_tfidf_rels_reducido.txt'

# Leer los archivos
def leer_archivo(ruta):
    with open(ruta, 'r') as archivo:
        contenido = archivo.read().splitlines()
    return contenido

# Calcular la similitud del coseno
def calcular_similitud(vectorizador, documentos, consultas):
    tf = vectorizador.fit_transform(documentos + consultas)
    similitudes = cosine_similarity(tf)
    return similitudes[:len(consultas), len(consultas):]

# Escribir las similitudes en un archivo de salida
def escribir_similitudes(similitudes, ruta_salida):
    with open(ruta_salida, 'w') as archivo:
        for i in range(similitudes.shape[0]):
            for j in range(similitudes.shape[1]):
                if similitudes[i, j] > 0:
                    archivo.write(f'{i+1} {j+1} {similitudes[i, j]:.6f}\n')

# Leer los archivos
documentos = leer_archivo(archivo_entrada_all)
consultas = leer_archivo(archivo_entrada_query)
documentos_reducidos = leer_archivo(archivo_entrada_all_reducido)
consultas_reducidas = leer_archivo(archivo_entrada_query_reducido)

# Calcular la similitud del coseno con TF
vectorizador_tf = CountVectorizer()
similitudes_tf = calcular_similitud(vectorizador_tf, documentos, consultas)
similitudes_tf_reducido = calcular_similitud(vectorizador_tf, documentos_reducidos, consultas_reducidas)

# Calcular la similitud del coseno con TF-IDF
vectorizador_tfidf = TfidfVectorizer()
similitudes_tfidf = calcular_similitud(vectorizador_tfidf, documentos, consultas)
similitudes_tfidf_reducido = calcular_similitud(vectorizador_tfidf, documentos_reducidos, consultas_reducidas)

# Escribir las similitudes en los archivos de salida
escribir_similitudes(similitudes_tf, archivo_salida_tf)
escribir_similitudes(similitudes_tfidf, archivo_salida_tfidf)
escribir_similitudes(similitudes_tf_reducido, archivo_salida_tf_reducido)
escribir_similitudes(similitudes_tfidf_reducido, archivo_salida_tfidf_reducido)
