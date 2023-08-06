library(ade4)
## Not run:
data(carniherbi49)
par(mfrow=c(1,3))
plot(newick2phylog(carniherbi49$tre1), clabel.leaves = 0,
f.phylog = 2, sub ="article 1")
plot(newick2phylog(carniherbi49$tre2), clabel.leaves = 0,
f.phylog = 2, sub = "article 2")
taxo <- as.taxo(carniherbi49$taxo)
plot(taxo2phylog(taxo), clabel.nodes = 1.2, clabel.leaves = 1.2)
par(mfrow = c(1,1))
## End(Not run)
