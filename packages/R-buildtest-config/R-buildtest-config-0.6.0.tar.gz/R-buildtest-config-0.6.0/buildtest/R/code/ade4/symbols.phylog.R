library(ade4)
data(mjrochet)
mjrochet.phy <- newick2phylog(mjrochet$tre)
tab0 <- data.frame(scalewt(log(mjrochet$tab)))
par(mfrow=c(3,2))
for (j in 1:6) {
w <- tab0[,j]
symbols.phylog(phylog = mjrochet.phy, w, csi = 1.5, cleg = 1.5,
sub = names(tab0)[j], csub = 3)
}
par(mfrow=c(1,1))

