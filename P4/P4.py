import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from tqdm import tqdm

def lematizar_palabra(palabra):
    lemmatizer = WordNetLemmatizer()
    pos_tag = nltk.pos_tag([palabra])[0][1][0].lower()
    pos_tag = pos_tag if pos_tag in ['a', 'r', 'n', 'v'] else 'n'
    return lemmatizer.lemmatize(palabra, pos=pos_tag)

def truncar_y_filtrar_palabra(palabra):
    palabra_truncada = palabra[:8]
    return palabra_truncada if len(palabra_truncada) >= 3 else None

def procesar_palabras_lematizacion(palabras):
    return [lematizar_palabra(palabra) for palabra in palabras]

def procesar_palabras_truncado_filtrado(palabras):
    return [palabra for palabra in (truncar_y_filtrar_palabra(palabra) for palabra in palabras) if palabra is not None]

def procesar_palabras(palabras, metodo):
    if metodo == 'lematizacion':
        return procesar_palabras_lematizacion(palabras)
    elif metodo == 'truncado':
        return [palabra[:8] for palabra in palabras]
    elif metodo == 'lematizacion_y_filtrado':
        return [palabra for palabra in procesar_palabras_lematizacion(palabras) if len(palabra) >= 10]
    elif metodo == 'truncado_y_filtrado':
        return procesar_palabras_truncado_filtrado(palabras)
    else:
        raise ValueError("Método no válido. Utilice 'lematizacion', 'truncado', 'lematizacion_y_filtrado' o 'truncado_y_filtrado'.")

def generar_vocabulario(archivo_all, archivo_query, archivo_vocabulario_all, archivo_vocabulario_query, metodo):
    vocabulario_all = set()
    vocabulario_query = set()

    # Leer el archivo de salida de 'cacm.all'
    with open(archivo_all, 'r', encoding='utf-8') as file_all:
        total_lines_all = sum(1 for _ in file_all)
        file_all.seek(0)  # Reset file pointer to the beginning
        progress_bar_all = tqdm(total=total_lines_all, desc=f'Procesando {archivo_all}', unit='line')

        for line in file_all:
            _, titulo, texto = line.split('|')
            palabras = set(titulo.split() + texto.split())
            vocabulario_all.update(procesar_palabras(palabras, metodo))
            progress_bar_all.update(1)

        progress_bar_all.close()

    # Leer el archivo de salida de 'query.txt'
    with open(archivo_query, 'r', encoding='utf-8') as file_query:
        total_lines_query = sum(1 for _ in file_query)
        file_query.seek(0)  # Reset file pointer to the beginning
        progress_bar_query = tqdm(total=total_lines_query, desc=f'Procesando {archivo_query}', unit='line')

        for line in file_query:
            _, titulo, texto = line.split('|')
            palabras = set(titulo.split() + texto.split())
            vocabulario_query.update(procesar_palabras(palabras, metodo))
            progress_bar_query.update(1)

        progress_bar_query.close()

    # Guardar vocabulario en archivos separados
    with open(archivo_vocabulario_all, 'w', encoding='utf-8') as vocab_all_file:
        vocab_all_file.write('\n'.join(sorted(vocabulario_all)))
    print(f"Longitud del vocabulario de 'salida_all.txt': {len(vocabulario_all)} palabras")

    with open(archivo_vocabulario_query, 'w', encoding='utf-8') as vocab_query_file:
        vocab_query_file.write('\n'.join(sorted(vocabulario_query)))
    print(f"Longitud del vocabulario de 'salida_query.txt': {len(vocabulario_query)} palabras")

def menu():
    print("1. Generar vocabulario con lematización")
    print("2. Generar vocabulario con truncado")
    print("3. Generar vocabulario con lematización y filtrado (eliminando palabras < 3 caracteres)")
    print("4. Generar vocabulario con truncado y filtrado (eliminando palabras < 3 caracteres)")
    print("5. Salir")
    opcion = input("Seleccione una opción (1, 2, 3, 4 o 5): ")
    return opcion

while True:
    opcion = menu()

    if opcion == '1':
        metodo = 'lematizacion'
    elif opcion == '2':
        metodo = 'truncado'
    elif opcion == '3':
        metodo = 'lematizacion_y_filtrado'
    elif opcion == '4':
        metodo = 'truncado_y_filtrado'
    elif opcion == '5':
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Por favor, seleccione 1, 2, 3, 4 o 5.")
        continue

    if metodo == 'lematizacion':
        archivo_vocabulario_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_lematizado.txt'
        archivo_vocabulario_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_lematizado.txt'
        #
        archivo_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_all.txt'
        archivo_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_query.txt'
    elif metodo == 'truncado':
        archivo_vocabulario_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_truncado.txt'
        archivo_vocabulario_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_truncado.txt'
        #
        archivo_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        archivo_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
    elif metodo == 'lematizacion_y_filtrado':
        archivo_vocabulario_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_lematizado_filtrado.txt'
        archivo_vocabulario_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_lematizado_filtrado.txt'
        #
        archivo_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_all.txt'
        archivo_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_query.txt'
    elif metodo == 'truncado_y_filtrado':
        archivo_vocabulario_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_all_truncado_filtrado.txt'
        archivo_vocabulario_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P4\\Salidas\\vocabulario_query_truncado_filtrado.txt'
        #
        archivo_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        archivo_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'
    generar_vocabulario(archivo_all, archivo_query, archivo_vocabulario_all, archivo_vocabulario_query, metodo)
