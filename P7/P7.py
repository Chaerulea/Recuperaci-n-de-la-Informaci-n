import pandas as pd

# Rutas de los archivos
qrels_path = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\CACM\\qrels.csv'
cacm_tf_rels_path = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P6\\Salidas\\cacm_tf_rels.csv'
aux_qrels_path = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Auxiliares\\Auxiliarqrels.csv'
aux_tf_path = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\CACM\\AuxiliarTF.csv'
tf_path = 'C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\P7\\Salidas\\tf.csv'

# Leer los archivos
qrels = pd.read_csv(qrels_path, sep='\t', names=['Numero consulta', 'Numero documento'])
cacm_tf_rels = pd.read_csv(cacm_tf_rels_path, sep=',', names=['Numero consulta', 'Numero documento'])

# Convertir la columna 'Numero documento' a tipo string
qrels['Numero documento'] = qrels['Numero documento'].astype(str)

# Agrupar los datos por consulta y convertir a cadena de texto
qrels_grouped = qrels.groupby('Numero consulta')['Numero documento'].apply(','.join).reset_index()
cacm_tf_rels_grouped = cacm_tf_rels.groupby('Numero consulta')['Numero documento'].apply(lambda x: ','.join(map(str, x[:50]))).reset_index()  # Solo usar los primeros 50 documentos

# Escribir los datos agrupados en los archivos auxiliares
qrels_grouped.to_csv(aux_qrels_path, index=False, sep='\t', header=False)
cacm_tf_rels_grouped.to_csv(aux_tf_path, index=False, sep='\t', header=False)

# Leer los archivos auxiliares
aux_qrels = pd.read_csv(aux_qrels_path, sep='\t', names=['Numero consulta', 'Numero documento'])
aux_tf = pd.read_csv(aux_tf_path, sep='\t', names=['Numero consulta', 'Numero documento'])

# Convertir la columna 'Numero documento' a tipo string
aux_qrels['Numero documento'] = aux_qrels['Numero documento'].astype(str)
aux_tf['Numero documento'] = aux_tf['Numero documento'].astype(str)

# Calcular la precisión para cada consulta
precision = {}
for query_num in aux_qrels['Numero consulta']:
    relevant_docs = set(aux_qrels[aux_qrels['Numero consulta'] == query_num]['Numero documento'].str.split(',').values[0])
    retrieved_docs = set(aux_tf[aux_tf['Numero consulta'] == query_num]['Numero documento'].str.split(',').values[0]) if query_num in aux_tf['Numero consulta'].values else set()
    precision[query_num] = len(relevant_docs & retrieved_docs) / len(retrieved_docs) if retrieved_docs else 0

# Crear un DataFrame con las métricas
metrics = pd.DataFrame.from_dict(precision, orient='index', columns=['Precision'])
metrics['Numero de documentos relevantes'] = aux_qrels['Numero consulta'].apply(lambda x: len(aux_qrels[aux_qrels['Numero consulta'] == x]['Numero documento'].str.split(',').values[0]))

# Escribir las métricas en el archivo de salida
metrics.reset_index().rename(columns={'index': 'Numero consulta'}).to_csv(tf_path, index=False, sep='\t')
