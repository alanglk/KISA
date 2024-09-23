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



