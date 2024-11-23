

#
# Generar dos muestras
#
# Pareado: test de normalidad sobre las diferencias y 
#   luego calcular p-value a través de algún método 
#   paramétrico (como t-test por ejemplo). Si no se supera
#   el test de normalidad hay que optar por algún método no
#   paramétrico
# No pareado: dos test de normalidad (una para cada modelo)
#   y si no se supera alguno de los dos se opta por los 
#   métodos no paramétricos
#
#
# Normality test:
# Para hacer el test de normalidad se busca ver cuánto se
# aproximan los datos a una distribución normal. En el caso
# de datos pareados, realizamos el normality test sobre las
# diferencias de los resultados de cada modelo.
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html
#
#

import numpy as np

import matplotlib.pyplot as plt

from scipy.stats import normaltest, shapiro, wilcoxon
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# For reproducibility
np.random.seed(42)

# Use Iris dataset for this test
X, y = load_iris(return_X_y=True)


# Generate Paired Data
def generate_paired_accuracy(n:int):
    accuracy_1  = []
    accuracy_2  = []

    for i in range(n):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
        
        model_1 = GaussianNB()
        y_pred = model_1.fit(X_train, y_train).predict(X_test)
        acc = accuracy_score(y_pred,y_test)
        accuracy_1.append(acc)

        svm = SVC(kernel='rbf', random_state=0, gamma=.10, C=1.0)
        y_pred = svm.fit(X_train, y_train).predict(X_test)
        acc = accuracy_score(y_pred,y_test)
        accuracy_2.append(acc)

    return np.array(accuracy_1), np.array(accuracy_2)

accuracy_1, accuracy_2 = generate_paired_accuracy(1000)

assert accuracy_1.shape == accuracy_2.shape


# Compute the differences for paired data
difference = accuracy_1 - accuracy_2

# Se aproxima a una normal
plt.hist(difference)
plt.show()

# Hacemos el normality test
normality_value = normaltest(difference)
shapiro_value = shapiro(difference)
print(normality_value)
print(shapiro_value)

# Los normality test para la hipótesis nula "the data was drawn 
# from a normal distribution" dan unos p-values super bajos
# Esto implica un riesgo estadístico alto para decir que sí que provienen
# de una distribución normal.
# Por ello, recurrimos a tests no paramétricos para muestras pareadas
# non-parametric but paired -> wilcoxon
# non-parametric and paired -> mannwhitneyu

plt.hist(accuracy_1, bins=10, alpha = 0.7, color= "blue")
plt.hist(accuracy_2, bins=10, alpha = 0.7, color= "orange")
plt.show()

# null hypothesis that two related paired samples come from the same distribution
wilcoxon_value = wilcoxon(accuracy_1, accuracy_2) 
print(wilcoxon_value)

# Wilcoxon p-value es muy pequeño por lo que es estadísticamente significativo
# el decir que las dos distribuciones no se parecen 