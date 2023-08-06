library(ade4)
# a phylogenetic example
data(ungulates)
ung.phy <- newick2phylog(ungulates$tre)
FemBodyMass <- log(ungulates$tab[,1])
NeonatBodyMass <- log((ungulates$tab[,2]+ungulates$tab[,3])/2)
plot(FemBodyMass,NeonatBodyMass, pch = 20, cex = 2)
abline(lm(NeonatBodyMass~FemBodyMass))
z <- residuals(lm(NeonatBodyMass~FemBodyMass))
dotchart.phylog(ung.phy,val = z, clabel.n = 1,
labels.n = ung.phy$Blabels, cle = 1.5, cdot = 2)
table.phylog(ung.phy$Bscores, ung.phy,clabel.n = 1,
labels.n = ung.phy$Blabels)
orthogram(z, ung.phy$Bscores)
orthogram(z, phylog=ung.phy) # the same thing
# a spatial example
data(irishdata)
neig1 <- neig(mat01 = 1*(irishdata$link > 0))
sco1 <- scores.neig(neig1)
z <- scalewt(irishdata$tab$cow)
orthogram(z, sco1)
# a temporal example
data(arrival)
w <- orthobasis.circ(24)
orthogram(arrival$hours, w)
par(mfrow = c(1,2))
dotcircle(arrival$hours)
dotcircle(w[,2])
par(mfrow = c(1,1))
data(lynx)
ortho <- orthobasis.line(114)
orthogram(lynx,ortho)
attributes(lynx)$tsp
par(mfrow = c(2,1))
par(mar = c(4,4,2,2))
plot.ts(lynx)
plot(ts(ortho[,23], start = 1821, end = 1934, freq = 1), ylab = "score 23")
par(mfrow = c(1,1))

