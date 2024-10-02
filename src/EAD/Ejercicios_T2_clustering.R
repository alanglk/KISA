#########################################################################
#                               CLUSTERING                              #
#########################################################################

########################### Ejercicio 3 #################################
# En el fichero elipticos.txt se recogen datos ficticios para n = 65 objetos.
# a) Repres´entalos gr´aficamente. ¿Qu´e ves?

# b) Aplica el m´etodo de Ward utilizando la distancia eucl´ıdea entre pares de objetos.

# c) Aplica el m´etodo de Ward utilizando la distancia Mahalanobis entre pares de
# objetos.

# d) Comenta los resultados

########################### Ejercicio 4 #################################
# Trabajaremos con el conjunto de datos data1.txt y data2.txt el ´ındice silhouette, la
# estimaci´on del n´umero de clusters y el procedimiento kmeans.

# ########### data1.txt
# a) Obtener particiones en k = 2, 3, . . . , 10 clusters. Para cada partici´on en k clusters
# calcular la anchura media del silhouette ¯sk (silhouette()).
x <-read.table("./data/EAD/data1.txt", header = FALSE)
library(cluster)
k2 <- kmeans(x, centers = 2, nstart = 1)
s2 <- silhouette(k2$cluster, dist = dist(x))

# b) Representar gr´aficamente la anchura media del silhouette ¯sk frente al n´umero de
# clusters k de la partici´on. ¿Cu´antos clusters dir´ıas que hay en la partici´on seg´un
# este gr´afico?
silhouette_score <- function(k){
  km <- kmeans(x, centers = k, nstart=25)
  ss <- silhouette(km$cluster, dist(x))
  mean(ss[, 3])
}
k <- 2:10
avg_sil <- sapply(k, silhouette_score)
plot(k, type='b', avg_sil, xlab='Numero de clusters', ylab='Meida Silhouette Score', frame=FALSE)

# c) Obtener una partici´on en k = 4 clusters con kmeans. Repetir el procedimiento
# kmeans y comparar las dos particiones que has obtenido. Repetirlo varias veces. ¿Coinciden?


