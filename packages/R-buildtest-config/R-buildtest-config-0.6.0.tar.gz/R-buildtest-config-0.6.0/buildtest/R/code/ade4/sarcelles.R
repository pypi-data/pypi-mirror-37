library(ade4)
## Not run:
if(!adegraphicsLoaded()) {
# depends of pixmap
if(requireNamespace("pixmap", quietly = TRUE)) {
bkgnd.pnm <- pixmap::read.pnm(system.file("pictures/sarcelles.pnm", package = "ade4"))
data(sarcelles)
par(mfrow = c(4, 3))
for(i in 1:12) {
s.distri(sarcelles$xy, sarcelles$tab[, i], pixmap = bkgnd.pnm,
sub = sarcelles$col.names[i], clab = 0, csub = 2)
s.value(sarcelles$xy, sarcelles$tab[, i], add.plot = TRUE, cleg = 0)
}
par(mfrow = c(1, 1))
}
}
## End(Not run)

