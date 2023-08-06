library(ade4)
## Not run:
data(palm)
palm.phy <- newick2phylog(palm$tre)
radial.phylog(palm.phy,clabel.l=1.25)
orthogram(palm$traits[,4],palm.phy$Bscores)
dotchart.phylog(palm.phy,palm$traits[,4], clabel.l = 1,
labels.n = palm.phy$Blabels, clabel.n = 0.75)
w <- cbind.data.frame(palm.phy$Bscores[,c(3,4,6,13,21)],
scalewt((palm$traits[,4])))
names(w)[6] <- names(palm$traits[4])
table.phylog(w, palm.phy, clabel.r = 0.75, f = 0.5)
gearymoran(palm.phy$Amat, palm$traits[,-c(1,3)])
## End(Not run)

