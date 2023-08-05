library(ade4)
data(julliot)
## Not run:
if(adegraphicsLoaded()) {
if(requireNamespace("sp", quietly = TRUE)) {
obj1 <- sp::SpatialPolygonsDataFrame(Sr = julliot$Spatial, data = log(julliot$tab + 1))
g1 <- s.Spatial(obj1)
g2 <- s.value(julliot$xy, scalewt(log(julliot$tab + 1)), Sp = julliot$Spatial,
pSp.col = "white", pgrid.draw = FALSE)
}
} else {
if(requireNamespace("splancs", quietly = TRUE)) {
par(mfrow = c(3, 3))
for(k in 1:7)
area.plot(julliot$area, val = log(julliot$tab[, k] + 1),
sub = names(julliot$tab)[k], csub = 2.5)
par(mfrow = c(1, 1))
par(mfrow = c(3, 3))
for(k in 1:7) {
area.plot(julliot$area)
s.value(julliot$xy, scalewt(log(julliot$tab[, k] + 1)),
sub = names(julliot$tab)[k], csub = 2.5, add.p = TRUE)
}
par(mfrow = c(1, 1))
}
}
## End(Not run)
if(adegraphicsLoaded()) {
if(requireNamespace("sp", quietly = TRUE)) {
g3 <- s.image(julliot$xy, log(julliot$tab + 1), span = 0.25)
}
g4 <- s.value(julliot$xy, log(julliot$tab + 1))
} else {
if(requireNamespace("splancs", quietly = TRUE)) {
par(mfrow = c(3, 3))
for(k in 1:7)
s.image(julliot$xy, log(julliot$tab[, k] + 1), kgrid = 3, span = 0.25,
sub = names(julliot$tab)[k], csub = 2.5)
par(mfrow = c(1, 1))
par(mfrow = c(3, 3))
for(k in 1:7)
s.value(julliot$xy, log(julliot$tab[, k] + 1),
sub = names(julliot$tab)[k], csub = 2.5)
par(mfrow = c(1, 1))
}
}
## Not run:
if(requireNamespace("spdep", quietly = TRUE)) {
neig0 <- nb2neig(spdep::dnearneigh(as.matrix(julliot$xy), 1, 1.8))
if(adegraphicsLoaded()) {
g5 <- s.label(julliot$xy, nb = spdep::dnearneigh(as.matrix(julliot$xy), 1, 1.8))
} else {
par(mfrow = c(1, 1))
s.label(julliot$xy, neig = neig0, clab = 0.75, incl = FALSE,
addax = FALSE, grid = FALSE)
}
gearymoran(ade4:::neig.util.LtoG(neig0), log(julliot$tab + 1))
orthogram(log(julliot$tab[, 3] + 1), ortho = scores.neig(neig0),
nrepet = 9999)
}
## End(Not run)
