#########################################################################
#                     GRAFICAR CON LA LIBRERÍA ESTÁNDAR                 #
#########################################################################
# Muy útil para realizar la parte exploratoria de los datos y sacar conclusiones
# antes de realizar gráficos más complejos

# Leemos los datos
# datos <- read.csv2("./data/EAD/WHR2021C2.csv", header = TRUE, sep = ";") # Esto lee todo como string. No parsea los datos
datos <- read.table("./data/EAD/WHR2021C2.csv", header = TRUE, sep = ";")
attach(datos) # Para acceder directamente a los datos del dataframe

# Resúmen numérico
summary(Ladder.score)

# Boxplot o diagrama de cajas
boxplot(Ladder.score)
abline(h=4) # Se pueden ir añadiendo elementos a los gráficos

# Histograma default
hist(Ladder.score, col="lightgreen")

# Histograma modificado
hist(Ladder.score, col = "lightblue", breaks = 50)
rug(Ladder.score)
abline(v=4, lwd=2)
abline(v=median(Ladder.score), lwd=3, col="red")


# ¿Cómo se reparten los países según las regiones?
# Diagrama de barras
barplot(table(Regional.indicator), col = "wheat",
        main = "Número de países en las regiones")

# Cambiar orientación de las etiquetas las = (0, 1, 2, 3)
barplot(table(Regional.indicator), col = "wheat",
        main = "Número de países en las regiones", las=2)

# ¿El valor de la escalera está relacionado con el apoyo social?
# Dibujamos el gráfico base: la variable Escalera (Ladder.score)
plot(Social.support, Ladder.score, xlab="Apoyo social", ylab="Escalera")
# Añadimos la línes escalera = 4
abline(h=4)
# Añadimos un punto, grande, en el centroide
points(mean(Social.support), mean(Ladder.score), pch=21, bg="red", col="black", cex=2)
# Añadimos texto dentro del gráfico
text(mean(Social.support)-0.05, mean(Ladder.score), labels="Centroide", col="red")
# Añadimos título
mtext("Percepción felicidad", 3, line=1)

# Utilizando el color para indicar países europeos
europe <- (Regional.indicator == "Central and Eastern Europe") | (Regional.indicator == "Western Europe")
plot(Social.support, Ladder.score, xlab="Apoyo social", ylab="Escalera", col=europe+1)

# En 2 gráficos diferentes
par(mfrow=c(1,2))
plot(Social.support[europe], Ladder.score[europe], xlab="Apoyo social", ylab="Escalera",
     col=2, main="Europa")
plot(Social.support[!europe], Ladder.score[!europe], xlab="Apoyo social", ylab="Escalera",
     col=1, main="No Europa")

# Desvincular la tabla de datos
detach(datos)


# Par y Colores
?par # Abre la ayuda. En este caso de la función "par"
# Colores por números
kol <- rep(1:3, each=3)
x <- rnorm(10)
y <- rnorm(10)
plot(x, y, type="n")
text(x, y, kol, col=kol)

colors() # Te devuelve la lista de los colores disponibles por la librería estándar
kol <- colors()[c(615, 450, 68)] # "steelblue", "magenta", "cyan"
kol <- rep(kol, each=3)
plot(x, y, col=kol )

# Sin transparecia
x <- rnorm(1000)
y <- rnorm(1000)
plot(x, y, pch=19)

# Con transparencia
plot(x, y, pch=19, col=rgb(0,0,0, 0.2))


#########################################################################
#                           GRAFICAR CON GGPLOT2                        #
#########################################################################
# A la hora de realizar gráficos para presentar conclusiones, esta librería 
# proporciona funciones para realizar gráficos más elaborados.

datos <- read.table("./data/EAD/WHR2021C2.csv", header = TRUE, sep = ";")
library(ggplot2)

# Escalera en función del apoyo social
g <- ggplot(datos, aes(Social.support, Ladder.score))
print(g)

# Todavía no hemos añadido las capas
g + geom_point()
# Añadimos una capa de regresion
g + geom_point() + geom_smooth()
g + geom_point() + geom_smooth(method="lm")

# Gráficos condicionados : FACETS
europe <- (Regional.indicator == "Central and Eastern Europe") |
  (Regional.indicator == "Western Europe")
df <- data.frame(Country.names=Country.name, Ladder.score=Ladder.score,
                 Social.support=Social.support, Europe=europe)
g <- ggplot(df, aes(Social.support, Ladder.score))
g + geom_point() + facet_grid(. ~ Europe) + geom_smooth(method="lm")
# Modificando los "Aesthetics"
g + geom_point(color="steelblue", size=4, alpha=1/2)
g + geom_point(aes(color=Europe), size=4, alpha=1/2)
# Modificando etiquetas
g + geom_point(aes(color=Europe), size=4, alpha=1/2) +
  labs(title="Informe: felicidad")+
  labs(x="Apoyo social", y="Valor Escalera")





