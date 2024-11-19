# Aprendizaje Automático Avanzado (AAA)
# One-Class Classification
# Alan García Justel
# 
#
# Wine Dataset:
# https://archive.ics.uci.edu/dataset/109/wine
# 13 attributes and 3 classes: [1, 2, 3]
#
# Scikit LOF:
# https://scikit-learn.org/dev/auto_examples/neighbors/plot_lof_outlier_detection.html
#
# Idea: analizar el dataset en busca de outliers (probar con todas las clases)
# LOF es independiente del número de clases
# Eliminar la columna de la clase sobre el conjunto de datos para LOF
# Obtener la gráfica de outlierness (eje X) vs numero de instancias (eje Y)
#
# Entrenar un autoencoder con datos de vino tipo 2 (generar train, val y test)
# Medir el rendimiento del autoencoder frente al test de los vinos tipo 2
# Finalmente, medir el error de recontrucción cuando hay inputs de vinos tipo 1 y 3 
#


import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_wine_dataset(wine_path: str, 
                      class_of_interest: int = None, 
                      normalize = True) -> tuple:
    attributes_names = ["Alcohol", "Malic acid", "Ash", "Alcalinity of ash  ", 
                        "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols", 
                        "Proanthocyanins", "Color intensity", "Hue", 
                        "OD280/OD315 of diluted wines", "Proline"]

    wine_dataframe = pd.read_csv(wine_path)
    if class_of_interest is not None:
        # Filter by the class name
        wine_dataframe = wine_dataframe[wine_dataframe.iloc[:, 0] == class_of_interest]

    Y = wine_dataframe.iloc[:, 0] # The first column is the wine class
    X = wine_dataframe.iloc[:, 1:] # The other columns are the data

    if normalize:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled)
    
    # Set up the attribute names
    X.columns = attributes_names
    return X, Y


# Utilizar LOF para calcular el Local Outlier factor de cada instancia
# En principio, deberían distinguirse 3 grupos con poco outlierness (1 por cada clase)
# y quizás se encuentren instancias con un valor más alto (outliers)
X, Y = load_wine_dataset("./data/AAA/wine.data")
print(X)
print(Y)

from sklearn.neighbors import LocalOutlierFactor
clf = LocalOutlierFactor(n_neighbors=20)
clf.fit(X)
outlierness = clf.negative_outlier_factor_
print(outlierness)
