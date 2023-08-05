library(ade4)
data(tintoodiel)
if(!adegraphicsLoaded()) {
## Not run:
if(requireNamespace("pixmap", quietly = TRUE)) {
estuary.pnm <- pixmap::read.pnm(system.file("pictures/tintoodiel.pnm", package = "ade4"))
s.label(tintoodiel$xy, pixmap = estuary.pnm, neig = tintoodiel$neig,
clab = 0, cpoi = 2, cneig = 3, addax = FALSE, cgrid = 0, grid = FALSE)
}
## End(Not run)
estuary.pca <- dudi.pca(tintoodiel$tab, scan = FALSE, nf = 4)
if(requireNamespace("maptools", quietly = TRUE) & requireNamespace("spdep", quietly = TRUE)) {
estuary.listw <- spdep::nb2listw(neig2nb(tintoodiel$neig))
estuary.pca.ms <- multispati(estuary.pca, estuary.listw, scan = FALSE, nfposi = 3, nfnega = 2)
summary(estuary.pca.ms)
par(mfrow = c(1, 2))
barplot(estuary.pca$eig)
barplot(estuary.pca.ms$eig)
par(mfrow = c(1, 1))
}}
