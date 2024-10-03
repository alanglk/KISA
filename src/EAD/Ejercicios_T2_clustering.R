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
plot(k, type='b', avg_sil, xlab='Numero de clusters data1', ylab='Meida Silhouette Score', frame=FALSE)

# c) Obtener una partici´on en k = 4 clusters con kmeans. Repetir el procedimiento
# kmeans y comparar las dos particiones que has obtenido. Repetirlo varias veces. ¿Coinciden?
p1 <- kmeans(x, centers = 4, nstart = 1)
p2 <- kmeans(x, centers = 4, nstart = 1)
addmargins(table(p1$cluster, p2$cluster))
# Los clusters van variando. Hay veces que salen clusters parecidos en distinto orden, pero hay
# otras veces que son totalmente distintos

# ########### data2.txt
# a) Obtener particiones en k = 2, 3, . . . , 10 clusters. Para cada partici´on en k clusters
# calcular la anchura media del silhouette ¯sk (silhouette()).
x <-read.table("./data/EAD/data2.txt", header = FALSE)
k <- 2:10
avg_sil <- sapply(k, silhouette_score)

# b) Representar gr´aficamente la anchura media del silhouette ¯sk frente al n´umero de
# clusters k de la partici´on. ¿Cu´antos clusters dir´ıas que hay en la partici´on seg´un
# este gr´afico?
plot(k, type='b', avg_sil, xlab='Numero de clusters data2', ylab='Meida Silhouette Score', frame=FALSE)
plot(silhouette(kmeans(x, centers = 2, nstart = 10)$cluster, dist(x)))

# c) Obtener una partici´on en k clusters con kmeans (Elije t´u mismo el valor para k).
# Repetir el procedimiento kmeans y comparar las dos particiones que has obtenido.
# Repetir varias veces. ¿Coinciden?
p1 <- kmeans(x, centers = 4, nstart = 1)
p2 <- kmeans(x, centers = 4, nstart = 1)
addmargins(table(p1$cluster, p2$cluster))
str(p1)

########################### Ejercicio 6 #################################
# El conjunto de datos nutrient.dat recoge los nutrientes de 27 tipos de carne, pescado
# o ave. Las columnas recogen: nombre del alimento, energ´ıa (KCalorias), prote´ınas
# (gramos), grasa (gramos), calcio (miligramos), hierro (miligrams) por 85 gramos de
# alimento.
datos <- read.table("./data/EAD/nutrient.dat", row.names = 1, sep = "\t", header = FALSE)
colnames(datos) <- c("Calorias", "Proteinas", "Grasa", "Calcio", "Hierro")
head(datos)

# a) Aplica el m´etodo de Ward utilizando la distancia eucl´ıdea entre pares de objetos.
# ¿Crees que convendr´ıa estandarizar previamente las variables? ¿Se vislumbra
# alguna estructura entre los objetos?
datos <- scale(datos, center = TRUE, scale = TRUE)
head(datos)
pairs(datos)
library(cluster)
part.ward <- hclust(dist(datos), method = "ward.D2")
plot(part.ward)
part.ward <- cutree(part.ward, 3)

# b) Aplica el PAM para diferentes n´umeros de clusters k = 2, . . . , 10, y mira que
# n´umero de clusters te sugieren las anchuras medias de los silhouettes.
silhouette_pam<- function(k){
  d <- dist(datos)
  pm <- pam(d, k)$clustering
  ss <- silhouette(pm, d)
  mean(ss[, 3])
}
k <- 2:10
plot(sapply(k, silhouette_pam), type = "b", ylim = c(0,1))
part.pam <- pam(dist(datos), k = 3)$clustering

# c) Para el n´umeros de clusters que hayas decidido, calcula las particiones que te da
# el m´etodo de Ward y el PAM. ¿Coinciden?
addmargins(table(part.ward, part.pam))
rbind(part.ward[part.pam==1], row.names(datos)[part.pam==1])

# d) Describe los clusters que has obtenido.
for (cluster in 1:3){
  select <- part.pam==cluster
  aux <- apply(datos[select, ], 2, function(x){c(mean(x), sd(x))})
  cat("\nCluster ", cluster, "\n")
  print(aux)
}

plot(datos$Calcio, datos$Hierro, col = part.pam)
