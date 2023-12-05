import pandas as pd
import nltk
import string as string
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

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

# Calcular la frecuencia total de cada palabra (Positiva + Negativa)
vocabulario['Frecuencia_Total'] = vocabulario['Positiva'] + vocabulario['Negativa']

# Ordenar el vocabulario por frecuencia total en orden descendente
vocabulario_ordenado = vocabulario.sort_values(by='Frecuencia_Total', ascending=False)

# Guardar el vocabulario en un archivo CSV
print("Guardando el vocabulario en un archivo CSV...")
vocabulario.reset_index().rename(columns={'index': 'Numero de entrada en el vocabulario'}).to_csv('C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Proyecto Final\\Salidas\\vocabulario.csv', index=False)

# Imprimir las 50 palabras más comunes
print("Las 50 palabras más comunes son:")
print(vocabulario_ordenado.head(50))

# Imprimir la longitud total del vocabulario
print(f'La longitud total del vocabulario es {len(vocabulario)}.')

# Separate reviews into positive and negative
positive_reviews = df[df['evaluacion'] == 'Positiva']['reviewText']
negative_reviews = df[df['evaluacion'] == 'Negativa']['reviewText']

# Join the reviews into a single string
positive_text = ' '.join(positive_reviews)
negative_text = ' '.join(negative_reviews)

# Create word clouds
positive_wordcloud = WordCloud(max_words=500).generate(positive_text)
negative_wordcloud = WordCloud(max_words=500).generate(negative_text)

# Display the word clouds
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Positive Reviews')

plt.subplot(1,2,2)
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Negative Reviews')

plt.show()

# Crear el vectorizador
vectorizer = TfidfVectorizer()

# Ajustar y transformar las reviews
X = vectorizer.fit_transform(df['reviewText'])

# Codificar las etiquetas de evaluación
y = df['evaluacion'].map({'Positiva': 1, 'Negativa': 0})

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear los modelos
clf_svm = svm.SVC()
clf_lr = LogisticRegression()
clf_dt = DecisionTreeClassifier()

# Entrenar los modelos
clf_svm.fit(X_train, y_train)
clf_lr.fit(X_train, y_train)
clf_dt.fit(X_train, y_train)

# Hacer las predicciones
y_pred_svm = clf_svm.predict(X_test)
y_pred_lr = clf_lr.predict(X_test)
y_pred_dt = clf_dt.predict(X_test)

# Crear un DataFrame para las métricas
metricas = pd.DataFrame(index=['SVM', 'Regresión Logística', 'Árbol de Decisión'], columns=['Matriz de Confusión', 'Precisión', 'Recuerdo', 'Medida F1', 'Exactitud'])

# Calcular las métricas
for clf, y_pred, name in zip([clf_svm, clf_lr, clf_dt], [y_pred_svm, y_pred_lr, y_pred_dt], ['SVM', 'Regresión Logística', 'Árbol de Decisión']):
    metricas.loc[name, 'Matriz de Confusión'] = str(confusion_matrix(y_test, y_pred))
    metricas.loc[name, 'Precisión'] = precision_score(y_test, y_pred)
    metricas.loc[name, 'Recuerdo'] = recall_score(y_test, y_pred)
    metricas.loc[name, 'Medida F1'] = f1_score(y_test, y_pred)
    metricas.loc[name, 'Exactitud'] = accuracy_score(y_test, y_pred)

# Imprimir las métricas
print(metricas)
