library(ade4)
data(deug)
dd1 <- dudi.pca(deug$tab, scannf = FALSE)
dd1
t(dd1)
is.dudi(dd1)
redo.dudi(dd1,3)
summary(dd1)


