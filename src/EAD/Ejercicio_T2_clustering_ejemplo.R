# Ejemplo idiomas clustering ----------------------------------------------
# De la carpeta de datos.

data <- read.table('idiomas.dat', header=F, sep=" ")
dat <- as.numeric(data)
dat 
n <- 14
idiomas <-c("Aleman", "Ingles", "Euskara", "Catalan", "Castellano", "Danes", "Finlandes", "Frances", "Gallego", "Holandes", "Hungaro", "Italiano", "Noruego", "Polaco")
d <- matrix(0 , n, n, dimnames = list(idiomas))
aux <- 1
for (i in 1:n){
  for (j in i:n){
    d[i,j] <- dat[aux]
    d[j,i] <- dat[aux]
    aux <- aux +1
  }
}

hc <- hclust(as.dist(d), method= "ward.D2") # Distancia median sale rara porque la distancia nueva puede ser menor a la que se han juntado los clusters antes.
plot(hc, hang=-0.1)
 
# La heterogeneidad sirve para ver si estan bien agrupados los datos.
# Para saber cuantos clusters hacer, hay que buscar la menor suma de las heterogeneidades.

# La formula de Lance-WIlliams sirve para ver la distancia de 2 clusters que se van a unir con otro cluster.
# Con el metodo de ward en la formula Lance-williams se utiliza la distancia al cuadrado.

#Ejemplo diapositiva 32
x <- matrix(c(1,2,2,1,2,2.7,5,3,6.5,2,7,3), ncol=2, byrow=T)
x
dist
distancias <- dist(x, method = "euclidean")^2
distancias

# La distancia de ward al cuadrado es la distancia euclidea al cuadrado. Para cuando haya clusters de mas de un elemento hay que calcular medias y asi... 
hc2 <- hclust(dist(x), method="ward.D2")
hc2$merge

# Ejercicio 3 clustering -------------------------------------------------
data2 <- read.table('elipticos.txt')
plot(data2)

hc3 <- hclust(dist(data2), method="ward.D2")
plot(hc3, hang=-0.1)
part1 <- cutree(hc3, k=3)
plot(data2)
points(data2, col=part1)

#Hay que hacer la distancia de mahalanobis bien.
distMaha <- mahalanobis(data2, colMeans(data2), cov(data2))
hc4 <- hclust(distMaha, method="ward.D2")
plot(hc4, hang=-0.1)
part2 <- cutree(hc4, k=3)
plot(data2)
points(data2, col=part2)
