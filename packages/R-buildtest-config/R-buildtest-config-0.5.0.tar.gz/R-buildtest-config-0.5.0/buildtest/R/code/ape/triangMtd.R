library(ape)
data(woodmouse)
tr <- triangMtd(dist.dna(woodmouse))
plot(tr)
