library(ade4)
## Not run:
data(rpjdl)
xy <- dudi.coa(rpjdl$fau, scann = FALSE)$l1
xy1 <- dudi.pca(rpjdl$fau, scal = FALSE, scann = FALSE)$l1
if(adegraphicsLoaded()) {
g1 <- s.distri(xy, rpjdl$fau, xax = 2, yax = 1, starSize = 0.3, ellipseSize = 0, plab.cex = 0)
g2 <- s.distri(xy1, rpjdl$fau, xax = 2, yax = 1, starSize = 0.3, ellipseSize = 0, plab.cex = 0)
} else {
s.distri(xy, rpjdl$fau, 2, 1, cstar = 0.3, cell = 0)
s.distri(xy1, rpjdl$fau, 2, 1, cstar = 0.3, cell = 0)
}
cca1 <- cca(rpjdl$fau, rpjdl$mil, scan = FALSE)
plot(cca1)
## End(Not run)

