#########################################################################
#                         REPASO ÁLGEBRA LINEAL                         #
#########################################################################
# %*% producto matricial. Si hacemos solo * hace multiplicacion de elemento por elemento
# Inversa de una matriz: solve(matriz)
Hn <- function(n)
{
  # Matriz de centrado (dim. n)
  unos <- matrix(rep(1, n), ncol=1)
  H <- diag(1, n) - unos%*%t(unos)/n
  return(H)
}
# Comprobar si dos matrices son iguales
matequal <- function(x, y){
  return (is.matrix(x) && is.matrix(y) && dim(x) == dim(y) && all(x == y))
}


#########################################################################
#                           Matriz de centrado                          #
#########################################################################
n <- 20
p <- 3
set.seed(36209)
X <- matrix(round(runif(n*p, min=10, max=20), digits=1), ncol=p, byrow=TRUE)

# Centrar por fila (centrar los datos es restar la media)
cf <- X%*%Hn(p)
apply(cf, 1, mean) # Comprobamos que la media de las columnas es 0 o cercano

# Centrar por columna
cc <- Hn(n)%*%X
apply(cc, 2, mean) # Comprobamos que la media de las filas es 0

# Centramos por columnas y luego por filas
dc <- Hn(n)%*%X%*%Hn(p)
apply(dc, 1, mean)
apply(dc, 2, mean)

# EJERCICIO 1
# Dada la matriz A y sus correspondientes vectores de medias por fila (mF ), columna (mC ) y total (mT ),
# comprueba que HAH = HA − mF + mT (en cada caso con las correctas dimensiones).
A <- matrix(c(1, 4, 2, 3, 3, 1), nrow = 2, ncol = 3)
hah <- Hn(2)%*%A%*%Hn(3)
ha <-  Hn(2)%*%A
mF <- matrix(apply(A, 1, mean), nrow = 2, ncol = 3, byrow = FALSE)
mC <- matrix(apply(A, 2, mean), nrow = 2, ncol = 3, byrow = TRUE)
mT <- mean(A)
ha - mF + mT
# matequal(hah, ha - mF + mT) No funciona, pero sí que son iguales

#########################################################################
#                                Proyección                             #
#########################################################################





