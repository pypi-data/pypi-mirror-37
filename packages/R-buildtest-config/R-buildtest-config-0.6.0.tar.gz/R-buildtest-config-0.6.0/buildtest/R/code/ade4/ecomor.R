library(ade4)
data(ecomor)
ric <- apply(ecomor$habitat, 2, sum)
s.corcircle(dudi.pca(log(ecomor$morpho), scan = FALSE)$co)
forsub <- data.frame(t(apply(ecomor$forsub, 1, function (x) x / sum(x))))
pca1 <- dudi.pca(forsub, scan = FALSE, scale = FALSE)
w1 <- as.matrix(forsub)
if(adegraphicsLoaded()) {
g1 <- s.arrow(pca1$c1, plot = FALSE)
g2 <- s.label(w1, plab.cex = 0, ppoi.cex = 2, plot = FALSE)
G1 <- superpose(g1, g2, plot = TRUE)
} else {
s.arrow(pca1$c1)
s.label(w1, clab = 0, add.p = TRUE, cpoi = 2)
}
diet <- data.frame(t(apply(ecomor$diet, 1, function (x) x / sum(x))))
pca2 <- dudi.pca(diet, scan = FALSE, scale = FALSE)
w2 <- as.matrix(diet)
if(adegraphicsLoaded()) {
g3 <- s.arrow(pca2$c1, plot = FALSE)
g4 <- s.label(w2, plab.cex = 0, ppoi.cex = 2, plot = FALSE)
G2 <- superpose(g3, g4, plot = TRUE)
} else {
s.arrow(pca2$c1)
s.label(w2, clab = 0, add.p = TRUE, cpoi = 2)
## Not run:
dmorpho <- dist.quant(log(ecomor$morpho), 3)
dhabitat <- dist.binary(ecomor$habitat, 1)
dtaxo <- dist.taxo(ecomor$taxo)
mantel.randtest(dmorpho, dhabitat)
RV.rtest(pcoscaled(dmorpho), pcoscaled(dhabitat), 999)
procuste.randtest(pcoscaled(dmorpho), pcoscaled(dhabitat))
ecophy <- taxo2phylog(ecomor$taxo, add.tools=TRUE)
table.phylog(ecomor$habitat, ecophy, clabel.n = 0.5, f = 0.6,
clabel.c = 0.75, clabel.r = 0.5, csi = 0.75, cleg = 0)
plot(ecophy, clabel.n = 0.75, clabel.l = 0.75,
labels.l = ecomor$labels[,"latin"])
mantel.randtest(dmorpho, dtaxo)
mantel.randtest(dhabitat, dtaxo)
## End(Not run)
