library(ade4)
data(apis108)
apis <- count2genet(as.data.frame(t(apis108)))
apis.pca <- dudi.pca(apis$tab, center = apis$center,
scale = FALSE, scannf = FALSE, nf = 3)

