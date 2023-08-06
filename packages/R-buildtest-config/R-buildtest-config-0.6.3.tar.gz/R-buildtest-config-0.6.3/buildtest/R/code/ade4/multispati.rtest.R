library(ade4)
if (requireNamespace("maptools", quietly = TRUE) & requireNamespace("spdep", quietly = TRUE)) {
data(mafragh)
maf.listw <- spdep::nb2listw(neig2nb(mafragh$neig))
maf.pca <- dudi.pca(mafragh$env, scannf = FALSE)
multispati.rtest(maf.pca, maf.listw)
maf.pca.ms <- multispati(maf.pca, maf.listw, scannf = FALSE)
plot(maf.pca.ms)
}
