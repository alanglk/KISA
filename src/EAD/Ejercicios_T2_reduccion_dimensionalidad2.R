#########################################################################
#                         Multidimensional Scaling                      #
#########################################################################

########################### Ejercicio 1 #################################
# Se han encontrado 5 herramientas arqueol´ogicas en un yacimiemto. ´Estas estaban
# hechas con piedra, bronce y hierro seg´un la siguiente matriz de incidencias:

incidences <- matrix(c(0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0), ncol = 3, byrow = TRUE)
colnames(incidences) <- c("Piedra", "Bronce", "Hierro")

# a) Considera la matriz de distancias donde la distancia entre los objetos i y j viene
#    dada como δ2ij = 1 − sij , donde sij es la similaridad de Jaccard. ¿Cuál es la
#    dimensiónn en la que se han embebido los objetos?
dists1 <- sqrt(dist(incidences, method = "binary"))
x.mds1 <- cmdscale(dists1, eig = TRUE)
# La matriz de distancias se puede embeber en {1, 2... 4 (n-1)}. 
# Luego, la dimensión a la que se ha reducido es 4

x.mds1$eig # Valores propios
plot(x.mds1$eig, type="b" ) # ¿Cuáles son los valores propios más importantes? similar a un scree graph
plot(x.mds1$points, main = "Distancia sqrt(1 - Jaccard)")
x.mds1$GOF # Goodness Of Fit -> % variabilidad



# b) Obtén una representación euclídea de estas herramientas e interpreta los resultados.
dists2 <- dist(incidences, method = "euclidean")
x.mds2 <- cmdscale(dists2)
plot(x.mds2, main = "Distancia Euclidea")

# c) Repite el mismo análisis pero considerando la distancia entre los
#    objetos i y j como δij = 1 − sij . ¿Cuál es la dimensión en la que se han embebido
#    los objetos?
dists3 <- dist(incidences, method = "binary")
x.mds3 <- cmdscale(dists3, eig = TRUE)
plot(x.mds3$points, main = "Distancia (1 - Jaccard)")
