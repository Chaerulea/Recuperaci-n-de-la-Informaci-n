from tqdm import tqdm
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('spanish'))
stop_words.add('a')  # Añade 'a' a la lista de palabras de parada
lemmatizer = WordNetLemmatizer()

def eliminar_puntuacion(texto):
    texto = texto.replace('-', ' ').replace('_', ' ')
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    return texto

def pasar_a_minusculas(texto):
    return texto.lower()

def eliminar_stop_words(texto):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    return ' '.join(palabras_filtradas)

def eliminar_numeros(texto):
    return ''.join(i for i in texto if not i.isdigit())

def truncar(texto, longitud=8):
    return ' '.join([palabra[:longitud] for palabra in texto.split()])

def lematizar(texto):
    return ' '.join([lemmatizer.lemmatize(palabra) for palabra in texto.split()])

def agregar_espacios(texto):
    return texto.replace(',', ', ')

# Nueva función para eliminar palabras cortas
def eliminar_palabras_cortas(texto):
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if len(palabra) >= 3]
    return ' '.join(palabras_filtradas)

def procesar_archivos(archivo, archivo_salida, truncar_activado=False, lematizar_activado=False, eliminar_palabras_cortas_activado=False):
    with open(archivo, 'r', encoding='utf-8') as archivo_all, open(archivo_salida, 'w', encoding='utf-8') as archivo_salida:
        guardar = False
        num_documento = ""
        titulo_documento = ""
        texto_documento = ""

        total_lines = sum(1 for _ in archivo_all)
        archivo_all.seek(0)
        progress_bar = tqdm(total=total_lines, desc=f'Processing {archivo}')

        for linea in archivo_all:
            progress_bar.update(1)
            if linea.startswith(".I"):
                num_documento = linea.strip()[3:]
                guardar = True
                titulo_documento = ""
                texto_documento = ""
            elif linea.startswith(".T") and guardar:
                guardar = True
            elif (linea.startswith(".B") or linea.startswith(".A") or linea.startswith(".N") or linea.startswith(".X")) and guardar:
                guardar = False
                if titulo_documento or texto_documento:
                    titulo_documento = titulo_documento.strip()
                    texto_documento = texto_documento.strip()
                    documento_completo = f"{num_documento}|{titulo_documento} {texto_documento}|"
                    archivo_salida.write(documento_completo + "\n")
            elif linea.startswith(".W") and guardar:
                texto_documento = linea[3:].strip()
            elif guardar:
                linea_procesada = agregar_espacios(linea.strip())
                linea_procesada = eliminar_puntuacion(linea_procesada)
                linea_procesada = pasar_a_minusculas(linea_procesada)
                linea_procesada = eliminar_numeros(linea_procesada)
                if eliminar_palabras_cortas_activado:
                    linea_procesada = eliminar_palabras_cortas(linea_procesada)  # Aplicar la nueva función aquí
                if truncar_activado:
                    linea_procesada = truncar(linea_procesada)
                if lematizar_activado:
                    linea_procesada = lematizar(linea_procesada)
                linea_procesada = eliminar_stop_words(linea_procesada)
                titulo_documento += linea_procesada + " "

        progress_bar.close()

# Resto del código...
# Definir las rutas de los archivos
archivo_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\CACM\\cacm.all'
archivo_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\CACM\\query.text'

while True:
    opcion = input("Seleccione una opción (1 para procesar con truncamiento, 2 para procesar con lematización, 3 para procesar eliminando palabras cortas y aplicando truncamiento, 4 para procesar eliminando palabras cortas y aplicando lematización, 5 para salir): ")

    if opcion == '1':
        archivo_salida_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_all.txt'
        archivo_salida_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_truncado_query.txt'

        procesar_archivos(archivo_all, archivo_salida_all, truncar_activado=True)
        procesar_archivos(archivo_query, archivo_salida_query, truncar_activado=True)

        print("¡Procesamiento con truncamiento completado!")
    elif opcion == '2':
        archivo_salida_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_all.txt'
        archivo_salida_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_lematizado_query.txt'

        procesar_archivos(archivo_all, archivo_salida_all, lematizar_activado=True)
        procesar_archivos(archivo_query, archivo_salida_query, lematizar_activado=True)

        print("¡Procesamiento con lematización completado!")
    elif opcion == '3':
        archivo_salida_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_reducida_truncado_all.txt'
        archivo_salida_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Truncado\\salida_reducida_truncado_query.txt'
        procesar_archivos(archivo_all, archivo_salida_all, truncar_activado=True, eliminar_palabras_cortas_activado=True)
        procesar_archivos(archivo_query, archivo_salida_query, truncar_activado=True, eliminar_palabras_cortas_activado=True)

        print("¡Procesamiento eliminando palabras cortas y aplicando truncamiento completado!")
    elif opcion == '4':
        archivo_salida_all = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_reducida_lematizado_all.txt'
        archivo_salida_query = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P3\\Salidas\\Lematizado\\salida_reducida_lematizado_query.txt'

        procesar_archivos(archivo_all, archivo_salida_all, lematizar_activado=True, eliminar_palabras_cortas_activado=True)
        procesar_archivos(archivo_query, archivo_salida_query, lematizar_activado=True, eliminar_palabras_cortas_activado=True)

        print("¡Procesamiento eliminando palabras cortas y aplicando lematización completado!")
    elif opcion == '5':
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Por favor, seleccione 1, 2, 3, 4 o 5.")
