library(ade4)
data(doubs)
pca1 <- dudi.pca(doubs$env, scal = TRUE, scann = FALSE)
pca2 <- dudi.pca(doubs$fish, scal = FALSE, scann = FALSE)
proc1 <- procuste(pca1$tab, pca2$tab)
protest1 <- procuste.rtest(pca1$tab, pca2$tab, 999)
protest1
plot(protest1)

