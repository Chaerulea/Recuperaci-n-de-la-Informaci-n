import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Proyecto Final\\reviewText.csv')

# Crear un nuevo DataFrame con las columnas 'numero de review', 'overall', 'reviewText' y 'evaluacion'
nuevo_df = pd.DataFrame({
    'numero de review': df.index + 1,
    'overall': df['overall'],
    'reviewText': df['reviewText'],
    'evaluacion': ['Negativa' if x < 4 else 'Positiva' for x in df['overall']]
})

# Guardar el nuevo DataFrame en un archivo CSV en la ruta deseada
nuevo_df.to_csv('C:\\Users\\reda0\\OneDrive\\Documentos\\Universidad\\Otoño 2023\\Recuperacion de la informacion\\Proyecto Final\\Salidas\\reviewEvaluada.csv', index=False)

# Generar una gráfica de pastel con las reviews positivas y negativas
evaluaciones = nuevo_df['evaluacion'].value_counts()
plt.pie(evaluaciones, labels=evaluaciones.index, autopct='%1.1f%%')
plt.title('Distribución de las evaluaciones')
plt.show()
