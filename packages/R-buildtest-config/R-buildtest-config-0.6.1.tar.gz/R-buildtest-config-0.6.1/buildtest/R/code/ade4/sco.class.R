library(ade4)
data(meau)
envpca <- dudi.pca(meau$env, scannf=FALSE)
par(mfrow=c(2,1))
sco.class(envpca$li[,1],meau$design$season, col = 1:6)
sco.class(envpca$li[,1],meau$design$season, col = 1:4, reverse = TRUE)

