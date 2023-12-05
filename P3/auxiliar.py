import pandas as pd
import nltk
import string as string
from tqdm import tqdm

# Leer el archivo CSV
df = pd.read_csv('C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Proyecto Final\\Salidas\\reviewEvaluada.csv')

# Convertir todo el texto a minúsculas
df['reviewText'] = df['reviewText'].str.lower()

# Eliminar la puntuación y reemplazarla con un espacio
df['reviewText'] = df['reviewText'].fillna('').astype(str).apply(lambda x: x.translate(str.maketrans('', '', string.punctuation))).apply(lambda x: x.replace(string.punctuation, ' '))

# Eliminar las palabras vacías (stopwords)
stopwords = nltk.corpus.stopwords.words('english')
df['reviewText'] = df['reviewText'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopwords]))

# Eliminar los números
df['reviewText'] = df['reviewText'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

# Crear un DataFrame para el vocabulario
vocabulario = pd.DataFrame(list(set(' '.join(df['reviewText'].tolist()).split())), columns=['palabra'])

# Contar el número de veces que cada palabra aparece en una review positiva y negativa
print("Contando apariciones de palabras en reviews positivas y negativas...")
for i in tqdm(range(len(vocabulario))):
    palabra = vocabulario.loc[i, 'palabra']
    vocabulario.loc[i, 'Positiva'] = sum(df[df['evaluacion'] == 'Positiva']['reviewText'].str.contains(r'\b' + palabra + r'\b'))
    vocabulario.loc[i, 'Negativa'] = sum(df[df['evaluacion'] == 'Negativa']['reviewText'].str.contains(r'\b' + palabra + r'\b'))

# Guardar el vocabulario en un archivo CSV
print("Guardando el vocabulario en un archivo CSV...")
vocabulario.reset_index().rename(columns={'index': 'Numero de entrada en el vocabulario'}).to_csv('C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Proyecto Final\\Salidas\\vocabulario.csv', index=False)

# Imprimir la longitud del vocabulario
print(f'La longitud del vocabulario es {len(vocabulario)}.')
