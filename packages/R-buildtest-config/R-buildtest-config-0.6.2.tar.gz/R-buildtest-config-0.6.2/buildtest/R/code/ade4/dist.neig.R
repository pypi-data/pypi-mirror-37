library(ade4)
data(elec88)
d0 <- dist.neig(elec88$neig)
plot(dist(elec88$xy),d0)
