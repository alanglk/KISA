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
# Para algunas cosas resulta más fácil adecuar el conjunto de datos
df$Pais <- ifelse(df$Europe, "Europeo", "No Europeo")
g <- ggplot(df, aes(Social.support, Ladder.score))
g + geom_point(aes(color=Pais), size=4, alpha=1/2) +
labs(title="Informe: felicidad")+
labs(x="Apoyo social", y="Valor Escalera")
# Modificar el suavizado
g + geom_point(aes(color=Pais), size=4, alpha=1/2) +
geom_smooth(method="lm", size=2, linetype=2, se=FALSE, color="red")

g + geom_point(aes(color=Pais), size=4, alpha=1/2) +
facet_grid(. ~ Europe) +
geom_smooth(method="lm", size=2, linetype=2, se=FALSE, aes(color=Pais))

# Como depende la relacion no en funcion de Europeo/No europeo sino también en función
# de la percepción de la corrupcion?
# Ahora esta variable no es un factor sino que es continua.
# Primero debemos de categorizarlo
df$CorruptionCat <- cut(dat$Perceptions.of.corruption,
breaks = quantile(seq(0, 1, by=0.25)))
g <- ggplot(df, aes(Social.support, Ladder.score))
g <- g + geom_point(alpha=1/2, color="blue") +
facet_wrap(Europe ~ CorruptionCat, nrow=2, ncol=4)
#-------------------------------------------------------------------------------
# GUARDAR GRAFICOS
# Una vez has generado el gráfico que quieres puedes guardarlo en un fichero para
# que puedas incluirlo en otro documento. Por ejemplo, tenemos el último gráfico
# creado en el objeto g. Lo guardaremos en formato pdf. Puedes utilizar de manera
# similar las funciones jpeg() y png().
pdf("MiGrafico.pdf")
g
dev.off()
#-------------------------------------------------------------------------------

#########################################################################
#                            EJERCICIO 1                                #
#########################################################################
datos <- read.table("./data/EAD/TiemposActividades.csv", header = TRUE, sep = "\t")
attach(datos) # Para acceder directamente a los datos del dataframe

# GRAFICO 1
# Los datos de TiempoLAB están en segundos. Hay que pasarlos a horas
TiempoLABh <- TiempoLAB / 3600
meanValue <- mean(TiempoLABh)
hist(TiempoLABh, breaks = 40, col = "purple", xlab = "Dedicación Trabajo Profesional(h.)", ylab = "Frecuencias", ylim = c(0, 4000), main = NULL)
abline(v = meanValue, lty = 2) # Agregar linea punteada en la media
text(meanValue + 2.5 , 1000, labels = paste("Puntuación media", round(meanValue, digits = 3), collapse = " "))


# GRAFICO 2 
# Tiempo Profesion (h) en X y Tiempo Cuidados (h) en Y por Jornadas NORMALES y Jornadas DESCANSO
par(mfrow=c(1,2))
TiempoLABh <- TiempoLAB / 3600
TiempoCUIDADOh <- TiempoCUIDADO / 3600
# Identificamos las entradas de jornadas normales y de descanso
jornadaNormal   <- (JORNADA == "Normal")
jornadaDescanso <- (JORNADA == "DescansoNOTRAB") | (JORNADA == "DescansoSITRAB")
colores <- ifelse(SEXO == "M", "red", "blue")
formas <- ifelse(SEXO == "M", 21, 22)

plot(TiempoLABh[jornadaNormal], TiempoCUIDADOh[jornadaNormal], xlab="Tiempo Profesión (h.)", ylab="Tiempo Cuidados (h.)",
     col="black", bg=colores, main="Jornada NORMAL", pch = formas, ylim = c(0, 12))

plot(TiempoLABh[jornadaDescanso], TiempoCUIDADOh[jornadaDescanso], xlab="Tiempo Profesión (h.)", ylab="Tiempo Cuidados (h.)",
     col="black", bg=colores, main="Jornada DESCANSO", pch = formas, ylim = c(0, 12))

legend("topleft", c("Mujeres", "Hombres"), col = "black", fill = c("red", "blue"), cex=0.8)


# GRAFICO 3
datos <- read.table("./data/EAD/TiemposActividades.csv", header = TRUE, sep = "\t")
attach(datos) # Para acceder directamente a los datos del dataframe
library(ggplot2)

TiempoLABh <- TiempoLAB / 3600
TiempoCUIDADOh <- TiempoCUIDADO / 3600
jornada <- ifelse(JORNADA == "Normal", "Normal", "DescansoNOTRAB")
df <- data.frame( TiempoLABh = TiempoLABh, TiempoCUIDADOh = TiempoCUIDADOh, SEXO = SEXO, JORNADA=jornada)

# Utilizamos ggplot2
g <- ggplot(df, aes(x = TiempoLABh, y = TiempoCUIDADOh, color = SEXO)) # Grafico Jornada Normal
g + geom_point() + facet_grid(. ~ JORNADA)+ scale_color_manual(values=c("#56B4E9", "#E69F00")) + xlab("Tiempo Profesión") + ylab("Tiempo Cuidados")

