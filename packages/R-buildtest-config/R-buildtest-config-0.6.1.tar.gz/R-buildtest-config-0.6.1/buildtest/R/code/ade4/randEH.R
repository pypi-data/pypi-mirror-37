library(ade4)
data(carni70)
carni70.phy <- newick2phylog(carni70$tre)
mean(randEH(carni70.phy, nbofsp = 7, nbrep = 1000))
## Not run:
# the folowing instructions can last about 2 minutes.
data(carni70)
carni70.phy <- newick2phylog(carni70$tre)
percent <- c(0,0.04,0.07,seq(0.1,1,by=0.1))
pres <- round(percent*70)
topt <- sapply(pres, function(i) optimEH(carni70.phy, nbofsp = i, give = FALSE))
topt <- topt / EH(carni70.phy)
tsam <- sapply(pres, function(i) mean(randEH(carni70.phy, nbofsp = i, nbrep = 1000)))
tsam <- tsam / EH(carni70.phy)
plot(pres, topt, xlab = "nb of species saved", ylab = "Evolutionary history saved", type = "l")
lines(pres, tsam)
## End(Not run)

