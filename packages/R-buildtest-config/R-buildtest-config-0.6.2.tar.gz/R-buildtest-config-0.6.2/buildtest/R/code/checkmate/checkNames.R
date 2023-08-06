library(checkmate)
x = 1:3
testNames(x, "unnamed")
names(x) = letters[1:3]
testNames(x, "unique")
cn = c("Species", "Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")
assertNames(names(iris), permutation.of = cn)
