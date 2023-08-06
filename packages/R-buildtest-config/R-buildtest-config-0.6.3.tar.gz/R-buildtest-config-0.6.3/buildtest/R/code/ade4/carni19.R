library(ade4)
data(carni19)
carni19.phy <- newick2phylog(carni19$tre)
par(mfrow = c(1,2))
symbols.phylog(carni19.phy,carni19$bm-mean(carni19$bm))
dotchart.phylog(carni19.phy, carni19$bm, clabel.l=0.75)
par(mfrow = c(1,1))

