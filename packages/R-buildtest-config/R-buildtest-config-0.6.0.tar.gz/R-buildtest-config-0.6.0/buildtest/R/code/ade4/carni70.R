library(ade4)
## Not run:
data(carni70)
carni70.phy <- newick2phylog(carni70$tre)
plot(carni70.phy)
size <- scalewt(log(carni70$tab))[,1]
names(size) <- row.names(carni70$tab)
symbols.phylog(carni70.phy,size)
orthogram(size, phylog = carni70.phy)
yrange <- scalewt(carni70$tab[,2])
names(yrange) <- row.names(carni70$tab)
symbols.phylog(carni70.phy,yrange)
orthogram(yrange, phylog = carni70.phy)
if(adegraphicsLoaded()) {
g1 <- s.label(cbind.data.frame(size, yrange), plabel.cex = 0)
g2 <- addhist(g1)
} else {
s.hist(cbind.data.frame(size, yrange), clabel = 0)
}
## End(Not run)
