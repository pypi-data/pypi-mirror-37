library(adegenet)
## Not run:
if(require(ape) && require(igraph)){
## PERFORM SIMULATIONS
x <- haploGen(geo.sim=TRUE)
x
## PLOT DATA
plot(x)
## PLOT SPATIAL SPREAD
plotHaploGen(x, bg="white")
title("Spatial dispersion")
## USE SEQTRACK RECONSTRUCTION
x.recons <- seqTrack(x)
mean(x.recons$ances==x$ances, na.rm=TRUE) # proportion of correct reconstructions
g <- as.igraph(x)
g
plot(g)
plot(g, vertex.size=0)
}
## End(Not run)
