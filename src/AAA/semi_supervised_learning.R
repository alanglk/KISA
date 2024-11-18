library(RSSL)
set.seed(1)
df <- generate2ClassGaussian(2000,d=2,var=0.6)

# Defirir el clasificador supervisado y la estrategia
# SSL y sus parámetros
classifiers <- list("LS"=function(X,y,X_u,y_u) {
  LeastSquaresClassifier(X,y,lambda=0)}, 
  "Self"=function(X,y,X_u,y_u) {
    SelfLearning(X,y,X_u,LeastSquaresClassifier)}
)

# Definir la métrica de performance
measures <- list("Accuracy" =  measure_accuracy)

lc1 <- LearningCurveSSL(as.matrix(df[,1:2]),df$Class,
                          classifiers=classifiers, measures=measures,
                          type = "fraction", test_fraction = 0.4, repeats = 10)
  
# El área de la curva es la varianza y el punto es la media (se realizan 10 steps
# por cada fraccionado).
# test_fraction: definir el conjunto de test 0.4 -> (800 test 1200 entrenamiento)
# De los 1200 de entrenamiento, si type="fraction" se va variando el número de etiquetas verdaderas
# y desconocidas, es decir, se saben todas las etiquetas pero se simula que se pierden 
# La curva verde está por encima de la roja cuando hay pocos casos etiquetados.
# Cuando el numero de casos etiquetados es alto, el semi-supervised learning pierde sentido.
plot(lc1)


