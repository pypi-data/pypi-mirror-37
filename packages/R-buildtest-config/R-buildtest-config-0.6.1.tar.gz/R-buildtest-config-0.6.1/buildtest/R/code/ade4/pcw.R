library(ade4)
if(adegraphicsLoaded()) {
data(pcw)
if(requireNamespace("spdep", quietly = TRUE)) {
nb1 <- spdep::graph2nb(spdep::gabrielneigh(pcw$xy.utm), sym = TRUE)
s.label(pcw$xy, nb = nb1, Sp = pcw$map)
}
}
