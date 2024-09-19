# Libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Data loading and processing
df = pd.read_csv('Your Path/dataset_inquilinos.csv', index_col='id_inquilino')

df.columns = [
    'horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
    'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
    'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento'
]

# Encode categorical features using OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)
df_encoded = encoder.fit_transform(df)
encoded_feature_names = encoder.get_feature_names_out()

# Compute similarity matrix
matriz_s = np.dot(df_encoded, df_encoded.T)

# Rescale the similarity matrix to a range of -100 to 100
rango_min = -100
rango_max = 100

min_original = np.min(matriz_s)
max_original = np.max(matriz_s)

matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

df_similaridad = pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

def inquilinos_compatibles(id_inquilinos, topn):
    # Check if all tenant IDs are in the similarity matrix
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similaridad.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Calculate average similarity for the given tenants
    filas_inquilinos = df_similaridad.loc[id_inquilinos]
    similitud_promedio = filas_inquilinos.mean(axis=0)
    inquilinos_similares = similitud_promedio.sort_values(ascending=False)
    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)

    # Get the top N similar tenants
    topn_inquilinos = inquilinos_similares.head(topn)
    registros_similares = df.loc[topn_inquilinos.index]
    registros_buscados = df.loc[id_inquilinos]

    # Combine the records of the searched and similar tenants
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')

    return(resultado, similitud_series)