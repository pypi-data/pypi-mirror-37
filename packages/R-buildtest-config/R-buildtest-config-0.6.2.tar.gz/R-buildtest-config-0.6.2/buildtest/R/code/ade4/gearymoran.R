library(ade4)
# a spatial example
data(mafragh)
tab0 <- (as.data.frame(scalewt(mafragh$env)))
bilis0 <- neig2mat(mafragh$neig)
gm0 <- gearymoran(bilis0, tab0, 999)
gm0
plot(gm0, nclass = 20)
## Not run:
# a phylogenetic example
data(mjrochet)
mjr.phy <- newick2phylog(mjrochet$tre)
mjr.tab <- log(mjrochet$tab)
gearymoran(mjr.phy$Amat, mjr.tab)
gearymoran(mjr.phy$Wmat, mjr.tab)
if(adegraphicsLoaded()) {
g1 <- table.value(mjr.phy$Wmat, ppoints.cex = 0.35, nclass = 5,
axis.text = list(cex = 0), plot = FALSE)
g2 <- table.value(mjr.phy$Amat, ppoints.cex = 0.35, nclass = 5,
axis.text = list(cex = 0), plot = FALSE)
G <- cbindADEg(g1, g2, plot = TRUE)
} else {
par(mfrow = c(1, 2))
table.value(mjr.phy$Wmat, csi = 0.25, clabel.r = 0)
table.value(mjr.phy$Amat, csi = 0.35, clabel.r = 0)
par(mfrow = c(1, 1))
}
## End(Not run)
