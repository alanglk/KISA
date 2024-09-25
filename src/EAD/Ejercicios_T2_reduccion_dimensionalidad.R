#########################################################################
#                   Análisis de componentes principales                 #
#########################################################################

########################### Ejercicio 1 #################################
x <- matrix(c(2, 1, 5, 4, 3, 4, 5, 2), ncol = 2, byrow = TRUE, dimnames =  list(LETTERS[1:4], c("X1", "X2")))
par(mfrow=c(1,3))
# Representamos los datos en un plot
plot(x, pch = 21, asp = 1, col = "black", bg = "black", main = "Datos")
text(x[, 1] + 0.05, x[, 2] + 0.05, row.names(x))
S <- var(x)
u <- eigen(S)
c1 <- x %*% u$vectors[, 1] # vector u_1 proyección a una dimensión
plot(x = c1[,1], y = rep(0, length(c1[, 1])), main = "Reducción con U_1", ylab = "", xlab = "c1")
text(x = c1[,1], y = rep(0.1, length(c1[, 1])), row.names(x))

c2 <- x %*% u$vectors[, 2] # vector u_1 proyección a una dimensión
plot(x = c2[,1], y = rep(0, length(c2[, 1])), main = "Reducción con U_2", ylab = "", xlab = "c2")
text(x = c2[,1], y = rep(0.1, length(c2[, 1])), row.names(x))
# Nos faltaría centrarlo en torno al 0 (restando la media)


########################### Ejercicio 2 #################################
X <- read.table("./data/EAD/temperat.csv", header = TRUE, sep = ";")
X <- X[, !(names(X) %in% c("Moyenne", "Amplitude", "Latitude", "Longitude", "Region"))]

# ¿Matriz de varianzas o de correlaciones? Si se estandariza se utilizará la de correlaciones
# En este caso todas las variables están en las mismas unidades así que da igual
# Sin embargo, en la mayoría de casos hay que estandarizar los datos
# para estandarizar se puede utilizar la función scale(X) o prcomp(X, scale. = TRUE)

# a) Obtener la descomposición de la variabilidad por componentes en términos de porcentaje.
out <- prcomp(X)
landa <- out$sdev
vari <- landa / sum(landa) * 100

descomp_variabilidad <- data.frame(componente = x, landa = landa, variabilidad = vari)
descomp_variabilidad$var_acum = cumsum(vari)

# b) Interpretar las dos primeras componentes.
eigen(var(X)) # Lo mismo que rotation -> matriz de Us
out$rotation # matriz de autovectores -> matriz de Us
out$x # C -> matriz de componentes principales C = XU
cor(X, out$x[, 1:2]) # Correlaciones de Pearson
biplot(out)

# c) ¿Hay alguna variable que no queda bien recogida con las dos primeras componentes?
# Grafico scree
x <- seq(1, length(vari))
plot(x, vari, type = "b", col="darkorchid3")
# Por los resultados del grafico scree y los valores de las correlaciones entre X1...Xp y C1...Cp, las variables quedan bien representadas con las dos primeras componentes 

# d) Representar las ciudades según los valores de las dos primeras componentes
plot(out$x[, 1:2], pch = 21, col = "black", bg = "black")
text(x = out$x[, 1], y = out$x[, 2] + 0.5, row.names(out$x))

# e) Representar las ciudades según los valores de las dos primeras componentes mostrando la region a la que pertenecen
library(dplyr)
X <- read.table("./data/EAD/temperat.csv", header = TRUE, sep = ";")
df <- data.frame(out$x)
df <- df %>% mutate(Region = X$Region)

library(ggplot2)
ggplot(df, aes(x = PC1, y = PC2, colour = Region)) +
    geom_point(size = 3)
