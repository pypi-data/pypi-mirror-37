library(ape)
data(woodmouse)
d <- dist.dna(woodmouse)
delta.plot(d)
layout(1)
delta.plot(d, 40, which = 1)

