library(ade4)
data(doubs)
pca1 <- dudi.pca(doubs$env, scal = TRUE, scann = FALSE)
pca2 <- dudi.pca(doubs$fish, scal = FALSE, scann = FALSE)
rv1 <- RV.rtest(pca1$tab, pca2$tab, 99)
rv1
plot(rv1)
