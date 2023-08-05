library(ade4)
data(veuvage)
par(mfrow = c(3,2))
for (j in 1:6) plot(veuvage$age, veuvage$tab[,j],
xlab = "age", ylab = "pourcentage de veufs",
type = "b", main = names(veuvage$tab)[j])
