library(ade4)
data(t3012)
data(elec88)
if(adegraphicsLoaded()) {
if(requireNamespace("sp", quietly = TRUE)) {
s.arrow(t3012$xy, pori.ori = as.numeric(t3012$xy["Paris", ]), Sp = t3012$Spatial,
pSp.col = "white", pgrid.draw = FALSE)
}
} else {
area.plot(elec88$area)
s.arrow(t3012$xy, ori = as.numeric(t3012$xy["Paris", ]), add.p = TRUE)
}
