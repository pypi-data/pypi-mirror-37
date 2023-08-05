library(ade4)
## an example corresponding to 10 statistics and 100 repetitions
cv <- as.krandxval(RMSEc = matrix(rnorm(1000), nrow = 100), RMSEv =
matrix(rnorm(1000, mean = 1), nrow = 100))
cv
if(adegraphicsLoaded())
plot(cv)

