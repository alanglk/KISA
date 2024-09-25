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




