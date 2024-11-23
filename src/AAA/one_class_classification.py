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


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

### FUNCIONES DE AYUDA #####################################################################
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

# Label colormap
label2color = {
    1: (162, 78, 255),
    2: (0, 235, 111),
    3: (0, 122, 210)
}
label2color = {key: tuple(value / 255 for value in rgb) for key, rgb in label2color.items()}

# Extraer los datos de una única clase
def extract_one_class(X: pd.DataFrame, Y: pd.DataFrame, label: int) -> tuple:
    mask = Y == label
    return X[mask], Y[mask]

# Cargar el Dataset
X, Y = load_wine_dataset("./data/AAA/wine.data")

# Utilizar LOF para calcular el Local Outlier factor de cada instancia
# En principio, deberían distinguirse 3 grupos con poco outlierness (1 por cada clase)
# y quizás se encuentren instancias con un valor más alto (outliers)
clf = LocalOutlierFactor(n_neighbors=20)
outliers_pred = clf.fit_predict(X)
outlierness = pd.DataFrame({"outlierness": clf.negative_outlier_factor_, "outliers_pred": outliers_pred})

# Representar el outlierness de cada instancia con un scatter
def plot_raius_outlierness(X: pd.DataFrame, Y:pd.DataFrame, outlierness: pd.DataFrame):
    # Los labels reales se utiilzan únicamente para visualizar
    # En un entorno real no se contaría con Y

    # Para calcular el scree graph
    all_pca = PCA(n_components=len(X.columns))
    all_pca.fit(X)
    print(f"PLOTTING OUTLIERNESS\nPCA variabilidad: {all_pca.explained_variance_ratio_}\nAutovalores: {all_pca.singular_values_}")
    
    # Reducir a las 2 dimensiones más representativas con PCA
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)
    radius = (outlierness["outlierness"].max() - outlierness["outlierness"]) / (outlierness["outlierness"].max() - outlierness["outlierness"].min())
    color = Y.map(lambda label: label2color[label])

    # Plotear el scree graph y las instancias-outlierness
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.scatter(X_reduced[:, 0], X_reduced[:, 1], color=color, s=3.0, label="Data points")
    ax1.scatter(X_reduced[:, 0], X_reduced[:, 1], s=1000 * radius, edgecolors="r", facecolors="none", label="Outlier scores")
    ax1.set(xlabel='PCA1', ylabel='PCA2')
    ax1.set_title('Local Outlier Factor (LOF)')
    
    ax2.plot(range(1,len(all_pca.singular_values_ )+1), all_pca.singular_values_, marker='o', c='blue', label='Variabilidad PCA')
    ax2.set(xlabel='component number', ylabel='Eigen value')
    ax2.set_title('PCA Scree Graph')

    plt.show()

# Representar el outlierness de cada instancia 
def plot_instance_outlierness(Y: pd.DataFrame, outlierness: pd.DataFrame):
    labels = np.unique(Y)
    for l in labels:
        mask = Y == l
        plt.plot(-outlierness["outlierness"][mask], c = label2color[l], label=f"Wine type: {l}")
        plt.plot()

    # Dibujar puntos en los outliers determinados por LOF
    mask = outlierness["outliers_pred"] == -1
    x_ = outlierness.index[mask]
    y_ = -outlierness["outlierness"][mask]
    plt.scatter(x_, y_, color="red", s=7.0, label = "Outliers")

    # Dibujar el threshold que el algoritmo ha aplicado
    # para determinar si se trata de un outlier o no
    #
    # De la documentación:
    # offset_:
    #   Offset used to obtain binary labels from the raw scores. Observations having a negative_outlier_factor 
    #   smaller than offset_ are detected as abnormal. The offset is set to -1.5 (inliers score around -1), except 
    #   when a contamination parameter different than “auto” is provided. In that case, the offset is defined in 
    #   such a way we obtain the expected number of outliers in training.
    plt.axhline(y=-clf.offset_, color='r', linestyle='--', label="LOF Threshold")


    plt.title("Outlierness of each instance with LOF")
    plt.xlabel("Instance index")
    plt.ylabel("Outlierness Factor") 
    plt.legend()
    plt.show()


plot_raius_outlierness(X, Y, outlierness)
plot_instance_outlierness(Y, outlierness)

### AUTOENCODERS ###########################################################################
# Entrenar un autoencoder con los datos del Wine Dataset pero
# extrayendo todos los outliers y 10 instancias normales del dataset.
# Luego, una vez entrenado, probar si el autoencoder reconstruye
# bien o no las instancias de test extraidas. Comprobar si las que
# no reconstruye bien (tienen mayor error) se corresponden con los
# outliers identificados con LOF




# X, Y = extract_one_class(X, Y, label=2)

