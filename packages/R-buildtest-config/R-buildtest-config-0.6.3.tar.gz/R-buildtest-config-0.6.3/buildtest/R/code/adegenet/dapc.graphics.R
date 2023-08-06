library(adegenet)
## Not run:
data(H3N2)
dapc1 <- dapc(H3N2, pop=H3N2$other$epid, n.pca=30,n.da=6)
## defautl plot ##
scatter(dapc1)
## label individuals at the periphery
# air = 2 is a measure of how much space each label needs
# pch = NA suppresses plotting of points
scatter(dapc1, label.inds = list(air = 2, pch = NA))
## showing different scatter options ##
## remove internal segments and ellipses, different pch, add MStree
scatter(dapc1, pch=18:23, cstar=0, mstree=TRUE, lwd=2, lty=2, posi.da="topleft")
## only ellipse, custom labels, use insets
scatter(dapc1, cell=2, pch="", cstar=0, posi.pca="topleft", posi.da="topleft", scree.pca=TRUE,
inset.pca=c(.01,.3), label=paste("year\n",2001:2006), axesel=FALSE, col=terrain.colors(10))
## without ellipses, use legend for groups
scatter(dapc1, cell=0, cstar=0, scree.da=FALSE, clab=0, cex=3,
solid=.4, bg="white", leg=TRUE, posi.leg="topleft")
## only one axis
scatter(dapc1,1,1,scree.da=FALSE, legend=TRUE, solid=.4,bg="white")
## example using genlight objects ##
## simulate data
x <- glSim(50,4e3-50, 50, ploidy=2)
x
plot(x)
## perform DAPC
dapc2 <- dapc(x, n.pca=10, n.da=1)
dapc2
## plot results
scatter(dapc2, scree.da=FALSE, leg=TRUE, txt.leg=paste("group",
c('A','B')), col=c("red","blue"))
## SNP contributions
loadingplot(dapc2$var.contr)
loadingplot(tail(dapc2$var.contr, 100), main="Loading plot - last 100 SNPs")
## assignplot / compoplot ##
assignplot(dapc1, only.grp=2006)
data(microbov)
dapc3 <- dapc(microbov, n.pca=20, n.da=15)
compoplot(dapc3, lab="")
## End(Not run)
