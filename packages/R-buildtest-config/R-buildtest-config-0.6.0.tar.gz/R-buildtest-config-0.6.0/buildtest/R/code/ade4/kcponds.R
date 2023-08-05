library(ade4)
data(kcponds)
w <- as.numeric(scalewt(kcponds$tab$N))
if(adegraphicsLoaded()) {
if(requireNamespace("sp", quietly = TRUE)) {
g1 <- s.label(kcponds$xy, Sp = kcponds$Spatial, pSp.col = "white", nb = kcponds$nb,
plab.cex = 0, paxes.asp = "fill", plot = FALSE)
g2 <- s.label(kcponds$xy, Sp = kcponds$Spatial, pSp.col = "white", plabels.cex = 0.8,
paxes.asp = "fill", plot = FALSE)
g3 <- s.value(kcponds$xy, w, psub.text = "Nitrogen concentration", paxe.asp = "fill",
plot = FALSE)
G <- rbindADEg(g1, g2, g3, plot = TRUE)
}
} else {
par(mfrow=c(3, 1))
area.plot(kcponds$area)
s.label(kcponds$xy, add.p = TRUE, cpoi = 2, clab = 0)
s.label(kcponds$xy, add.p = TRUE, cpoi = 3, clab = 0)
s.label(kcponds$xy, add.p = TRUE, cpoi = 0, clab = 0, neig = kcponds$neig, cneig = 1)
area.plot(kcponds$area)
s.label(kcponds$xy, add.p = TRUE, clab = 1.5)
s.value(kcponds$xy, w, cleg = 2, sub = "Nitrogen concentration", csub = 4,
possub = "topright", include = FALSE)
par(mfrow = c(1, 1))
}
## Not run:
par(mfrow = c(3, 1))
pca1 <- dudi.pca(kcponds$tab, scan = FALSE, nf = 4)
if(requireNamespace("maptools", quietly = TRUE) & requireNamespace("spdep", quietly = TRUE)) {
multi1 <- multispati(pca1, spdep::nb2listw(neig2nb(kcponds$neig)), scannf = FALSE, nfposi = 2,
nfnega = 1)
summary(multi1)
}
par(mfrow = c(1, 1))
## End(Not run)

