library(adegenet)
## Not run:
## LOAD DATA
data(eHGDP)
eHGDP
## PERFORM DAPC - USE POPULATIONS AS CLUSTERS
## to reproduce exactly analyses from the paper, use "n.pca=1000"
dapc1 <- dapc(eHGDP, all.contrib=TRUE, scale=FALSE,
n.pca=200, n.da=80) # takes 2 minutes
dapc1
## (see ?dapc for details about the output)
## SCREEPLOT OF EIGENVALUES
barplot(dapc1$eig, main="eHGDP - DAPC eigenvalues",
col=c("red","green","blue", rep("grey", 1000)))
## SCATTERPLOTS
## (!) Note: colors may be inverted with respect to [5]
## as signs of principal components are arbitrary
## and change from one computer to another
##
## axes 1-2
s.label(dapc1$grp.coord[,1:2], clab=0, sub="Axes 1-2")
par(xpd=T)
colorplot(dapc1$grp.coord[,1:2], dapc1$grp.coord, cex=3, add=TRUE)
add.scatter.eig(dapc1$eig,10,1,2, posi="bottomright", ratio=.3, csub=1.25)
## axes 2-3
s.label(dapc1$grp.coord[,2:3], clab=0, sub="Axes 2-3")
par(xpd=T)
colorplot(dapc1$grp.coord[,2:3], dapc1$grp.coord, cex=3, add=TRUE)
add.scatter.eig(dapc1$eig,10,1,2, posi="bottomright", ratio=.3, csub=1.25)
## MAP DAPC1 RESULTS
if(require(maps)){
xy <- cbind(eHGDP$other$popInfo$Longitude, eHGDP$other$popInfo$Latitude)
par(mar=rep(.1,4))
map(fill=TRUE, col="lightgrey")
colorplot(xy, -dapc1$grp.coord, cex=3, add=TRUE, trans=FALSE)
}
## LOOK FOR OTHER CLUSTERS
## to reproduce results of the reference paper, use :
## grp <- find.clusters(eHGDP, max.n=50, n.pca=200, scale=FALSE)
## and then
## plot(grp$Kstat, type="b", col="blue")
grp <- find.clusters(eHGDP, max.n=30, n.pca=200,
scale=FALSE, n.clust=4) # takes about 2 minutes
names(grp)
## (see ?find.clusters for details about the output)
## PERFORM DAPC - USE POPULATIONS AS CLUSTERS
## to reproduce exactly analyses from the paper, use "n.pca=1000"
dapc2 <- dapc(eHGDP, pop=grp$grp, all.contrib=TRUE,
scale=FALSE, n.pca=200, n.da=80) # takes around a 1 minute
dapc2
## PRODUCE SCATTERPLOT
scatter(dapc2) # axes 1-2
scatter(dapc2,2,3) # axes 2-3
## MAP DAPC2 RESULTS
if(require(maps)){
xy <- cbind(eHGDP$other$popInfo$Longitude,
eHGDP$other$popInfo$Latitude)
myCoords <- apply(dapc2$ind.coord, 2, tapply, pop(eHGDP), mean)
par(mar=rep(.1,4))
map(fill=TRUE, col="lightgrey")
colorplot(xy, myCoords, cex=3, add=TRUE, trans=FALSE)
}
## End(Not run)
