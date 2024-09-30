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
landa <- out$sdev ^ 2
vari <- landa / sum(landa) * 100

descomp_variabilidad <- data.frame(componente = x, landa = landa, variabilidad = vari)
descomp_variabilidad$var_acum = cumsum(vari)

summary(out) # Lo mismo que lo anterior

# Grafico scree
x <- seq(1, length(vari))
plot(x, vari, type = "b", col="darkorchid3")

# b) Interpretar las dos primeras componentes.
eigen(var(X)) # Lo mismo que rotation -> matriz de Us
out$rotation # matriz de autovectores -> matriz de Us
out$x # C -> matriz de componentes principales C = XU
r = cor(X, out$x[, 1:2]) # Correlaciones de Pearson
r
biplot(out)

# c) ¿Hay alguna variable que no queda bien recogida con las dos primeras componentes?
# Cálculo de las comunalidades. Fijamos X1...Xp y calculamos de cuánto son representadas por C1...Cq
# r²(Xj, C1) + ... + r²(Xj, Cq)
r_2 = r ^2
comunalidades = apply(X= r_2, MARGIN=1, FUN= sum)
comunalidades
apply(cor(X, out$x[, 1:2]), 1, function(x){sum(x^2)})

# d) Representar las ciudades según los valores de las dos primeras componentes
# Representar en un plot
plot(out$x[, 1:2], pch = 21, col = "black", bg = "black", cex = )
text(x = out$x[, 1], y = out$x[, 2] + 0.5, row.names(out$x))

# e) Representar las ciudades según los valores de las dos primeras componentes mostrando la region a la que pertenecen
library(dplyr)
X <- read.table("./data/EAD/temperat.csv", header = TRUE, sep = ";")
df <- data.frame(out$x)
df <- df %>% mutate(Region = X$Region)

library(ggplot2)
ggplot(df, aes(x = PC1, y = PC2, colour = Region)) +
    geom_point(size = 3)

########################### Ejercicio 4 #################################
# Se han considerado 9 documentos, de los cuales 5 (d1-d5) tratan de “interacci´on entre
# persona y computador” y los otros 4 (d6-d9) tratan sobre “teor´ıa de grafos”. Consid-
# eremos t´erminos las palabras que aparecen al menos en dos documentos distintos.
datos <-read.table("./data/EAD/dokumentuak.txt", sep = " ", header = TRUE)
# a) Calcula las 2 primeras componentes principales e interpretalas
out <- prcomp(datos)
summary(out) # Variabilidad
out$rotation[, 1:2]

# b) Representa los documentos segun los valores de las dos primeras componentes
plot(out$x[, 1:2])
text(out$x[, 1:2], row.names(out$rotation ))

# c) Supongamos que tenemos un nuevo documento d0 “Graph theory with applications 
#    to engineering and computer science”. Proy´ectalo en el plano construido por
#    las 2 primeras componentes. ¿D´onde se clasificar´ıa este documento, en el ´ambito
#    “interacci´on entre persona y computador” o en “teor´ıa de grafos”?
d0 <- c("graph", "theory", "with", "applications", "to", "engineering", "and", "computer", "science")
d0 <- matrix(c(0 ,0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0), ncol  = 1)

# Hay que centrar los datos primero
m <- apply(datos, 2, mean)
d0_rot <- t(d0 - m) %*% out$rotation[, 1:2] 

points(d0_rot, col = "red")


########################### Ejercicio 5 #################################
# install.packages("kernlab")
library("kernlab")
datos <- read.table("./data/EAD/spherical.csv", sep = " ", col.names = c("X", "Y", "Z"))
#xc <- scale(datos, center = TRUE, scale = FALSE) # Centrado de los datos

# a)  Realiza un ACP sobre las variables originales y repres´entalos en seg´un las dos
#     primeras componentes principales. Utiliza un color para los 100 primeros casos y
#     otro para los restantes.
out <- prcomp(datos, scale = FALSE)
summary(out)
C <- out$x[, 1:2]
n1 <- 100
n <- dim(datos)[1]
kol <- rep(1:2, each = c(n1, n - n1))
plot(x = C[, 1], y = C[, 2], col = kol)

# b)  Considera como funci´on kernel el RBF con σ = 0.2 y representa los objetos seg´un
#     las dos primeras kernel-componentes principales. Comp´aralo con los resultados
#     anteriores.
X <- as.matrix(datos)
s = 0.2
out2 <- kpca(X, kernel = "rbfdot", kpar = list(sigma = s))
plot(out2@rotated[, 1:2], col = kol)


