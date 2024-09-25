#########################################################################
#                 Distancias, similaridades y kernels                   #
#########################################################################
getwd() #setwd()
########################### Ejercicio 1 #################################
dat <- matrix(c(1.1, 2.0,
                1.9, 0.8,
                2.4, 2.5,
                2.0, 2.9,
                5.8, 0.6), byrow = TRUE, ncol = 2)

# a)
plot(dat, asp = 1)

# b)
# Calcula matrices de distancias a partir de coordenadas
# method: "euclidean", "maximum", "manhattan", "canberra" (weighted version of manhattan), "binary" or "minkowski"
dist(dat, method = "euclidean") 

# c)
dist(dat, method ="euclidean")
dist(dat, method ="maximum")
dist(dat, method ="manhattan")
dist(dat, method ="canberra")
dist(dat, method ="binary") 
dist(dat, method ="minkowski")
 
########################### Ejercicio 2 #################################


########################### Ejercicio 7 #################################
# Vector de distancias entre vectores
dists <- seq(0.1, 5, by = 0.05)

KM2 <- function(d){ exp(-d) } # Kernel Matern 1/2
KG <- function(d){ exp(-d ^2) } # Kernel Gausiano desv = 1/2
KM3 <- function(d){ (1 + sqrt(3) * d) * exp(-sqrt(3) * d) } # Kernel Matern 3/2
KM5 <- function(d){ (1 + sqrt(5) * d + sqrt(5) * d ^ 2 / 3) * exp(-sqrt(5) * d) } # Kernel Matern 5/2

plot(dists, KM2(dists), type = "l", col = "lightsalmon")
lines(dists, KG(dists), col = "orange")
lines(dists, KM3(dists), col = "lightgreen")
lines(dists, KM5(dists), col = "purple")


