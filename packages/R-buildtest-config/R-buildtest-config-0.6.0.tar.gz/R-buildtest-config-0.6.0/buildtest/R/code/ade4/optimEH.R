library(ade4)
data(carni70)
carni70.phy <- newick2phylog(carni70$tre)
optimEH(carni70.phy, nbofsp = 7, give.list = TRUE)

