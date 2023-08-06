library(ape)
data(woodmouse)
d <- dist.dna(woodmouse)
dm <- d
dm[sample(length(dm), size = 3)] <- NA
dist.topo(njs(dm), nj(d)) # often 0
dm[sample(length(dm), size = 10)] <- NA
dist.topo(njs(dm), nj(d)) # sometimes 0
