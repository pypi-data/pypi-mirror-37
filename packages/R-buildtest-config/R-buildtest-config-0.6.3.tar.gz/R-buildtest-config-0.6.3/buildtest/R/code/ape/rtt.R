library(ape)
t <- rtree(100)
tip.date <- rnorm(t$tip.label)^2
rtt(t, tip.date)
