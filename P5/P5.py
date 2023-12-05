import numpy as np
import pandas as pd
import math
from tqdm import tqdm

def contar_lineas(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        return len(lineas)

def generar_matriz(archivo_all, vocabulario_all):
    lineas_all = contar_lineas(archivo_all)
    lineas_vocabulario = contar_lineas(vocabulario_all)
    return np.zeros((lineas_all, lineas_vocabulario), dtype=int)

def contar_apariciones_palabra(palabra, contenido_all):
    return sum(1 for linea in contenido_all if palabra in linea.lower().split())

def save_to_csv(data, headers, filename):
    # Crear un DataFrame con los datos
    df = pd.DataFrame(data, columns=headers)

    # Agregar números de fila como índices
    df.index = range(1, len(df) + 1)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv(filename, index=True, index_label='Documento')

def contar_apariciones(vocabulario, archivo_all, salida_resultados, salida_vectores):
    with open(vocabulario, 'r', encoding='utf-8') as archivo_vocabulario:
        contenido_vocabulario = archivo_vocabulario.readlines()

    lineas_all = contar_lineas(archivo_all)
    matriz_cuentas = generar_matriz(archivo_all, vocabulario)

    with open(archivo_all, 'r', encoding='utf-8') as archivo_all:
        contenido_all = archivo_all.readlines()

    apariciones_palabras = {palabra.strip().lower(): contar_apariciones_palabra(palabra.strip().lower(), contenido_all) for palabra in contenido_vocabulario}

    for i, linea_all in tqdm(enumerate(contenido_all), total=len(contenido_all), desc="Contando apariciones"):
        for j, palabra_vocabulario in enumerate(contenido_vocabulario):
            matriz_cuentas[i][j] = linea_all.lower().split().count(palabra_vocabulario.strip().lower())

    save_to_csv(matriz_cuentas, contenido_vocabulario, salida_resultados.replace('.txt', '.csv'))
    matriz_np = np.array(matriz_cuentas)
    matriz_suma = matriz_np.sum(axis=1, keepdims=True)
    matriz_suma[matriz_suma == 0] = 1

    matriz_vectores = matriz_np / matriz_suma
    save_to_csv(matriz_vectores, contenido_vocabulario, salida_vectores.replace('.txt', '.csv'))

def calcular_tfidf(vocabulario, archivo_all, salida_tfidf):
    N = contar_lineas(archivo_all)
    Nt = contar_lineas(vocabulario)
    matriz_tfidf = np.zeros((N, Nt), dtype=float)

    with open(archivo_all, 'r', encoding='utf-8') as archivo_all:
        contenido_all = archivo_all.readlines()

    with open(vocabulario, 'r', encoding='utf-8') as archivo_vocabulario:
        contenido_vocabulario = archivo_vocabulario.readlines()

    apariciones_palabras = {palabra.strip().lower(): contar_apariciones_palabra(palabra.strip().lower(), contenido_all) for palabra in contenido_vocabulario}

    for i, linea_all in tqdm(enumerate(contenido_all), total=len(contenido_all), desc="Calculando TF-IDF"):
        for j, palabra_vocabulario in enumerate(contenido_vocabulario):
            tf = linea_all.lower().count(palabra_vocabulario.strip().lower())
            idf = math.log(N / (1 + apariciones_palabras[palabra_vocabulario.strip().lower()]))
            matriz_tfidf[i][j] = tf * idf

    save_to_csv(matriz_tfidf, contenido_vocabulario, salida_tfidf.replace('.txt', '.csv'))

# Nombres de archivos
# Archivos de datos
vocabulario_all_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_truncado_filtrado.txt'
vocabulario_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_truncado.txt'
vocabulario_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_truncado.txt'
vocabulario_query_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_truncado_filtrado.txt'

# Salidas
salida_resultados_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TF\\TF_all.txt'
salida_vectores_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Modelo Vectorial\\Vectorial_all.txt'
salida_tfidf_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TFIDF\\TFIDF_all.txt'
#
salida_resultados_all_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TF\\TF_all_reducido.txt'
salida_vectores_all_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Modelo Vectorial\\Vectorial_all_reducido.txt'
salida_tfidf_all_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TFIDF\\TFIDF_all_reducido.txt'
#
salida_resultados_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TF\\TF_query.txt'
salida_vectores_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Modelo Vectorial\\Vectorial_query.txt'
salida_tfidf_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TFIDF\\TFIDF_query.txt'
#
salida_resultados_query_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TF\\TF_query_reducido.txt'
salida_vectores_query_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Modelo Vectorial\\Vectorial_query_reducido.txt'
salida_tfidf_query_reducido = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P5\\Salidas\\Pesado TFIDF\\TFIDF_query_reducido.txt'

# Menú de selección
while True:
    print("\nMenú de selección:")
    print("1. Contar apariciones y generar matrices para vocabulario_all")
    print("2. Calcular TF-IDF para vocabulario_all")
    print("3. Contar apariciones y generar matrices para vocabulario_all_reducido")
    print("4. Calcular TF-IDF para vocabulario_all_reducido")
    print("5. Contar apariciones y generar matrices para vocabulario_query")
    print("6. Calcular TF-IDF para vocabulario_query")
    print("7. Contar apariciones y generar matrices para vocabulario_query_reducido")
    print("8. Calcular TF-IDF para vocabulario_query_reducido")
    print("9. Salir")

    opcion = input("Seleccione una opción (1-9): ")

    if opcion == "1":
        documentos_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        contar_apariciones(vocabulario_all, documentos_all, salida_resultados_all, salida_vectores_all)
        print("Apariciones y matrices generadas para vocabulario_all.")
    elif opcion == "2":
        documentos_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        calcular_tfidf(vocabulario_all, documentos_all, salida_tfidf_all)
        print("TF-IDF calculado para vocabulario_all.")
    elif opcion == "3":
        documentos_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        contar_apariciones(vocabulario_all_reducido, documentos_all, salida_resultados_all_reducido, salida_vectores_all_reducido)
        print("Apariciones y matrices generadas para vocabulario_all_reducido.")
    elif opcion == "4":
        documentos_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        calcular_tfidf(vocabulario_all_reducido, documentos_all, salida_tfidf_all_reducido)
        print("TF-IDF calculado para vocabulario_all_reducido.")
    elif opcion == "5":
        documentos_query ='C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
        contar_apariciones(vocabulario_query, documentos_query, salida_resultados_query, salida_vectores_query)
        print("Apariciones y matrices generadas para vocabulario_query.")
    elif opcion == "6":
        documentos_query ='C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
        calcular_tfidf(vocabulario_query, documentos_query, salida_tfidf_query)
        print("TF-IDF calculado para vocabulario_query.")
    elif opcion == "7":
        documentos_query ='C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
        contar_apariciones(vocabulario_query_reducido, documentos_query, salida_resultados_query_reducido, salida_vectores_query_reducido)
        print("Apariciones y matrices generadas para vocabulario_query_reducido.")
    elif opcion == "8":
        documentos_query ='C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
        calcular_tfidf(vocabulario_query_reducido, documentos_query, salida_tfidf_query_reducido)
        print("TF-IDF calculado para vocabulario_query_reducido.")
    elif opcion == "9":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
