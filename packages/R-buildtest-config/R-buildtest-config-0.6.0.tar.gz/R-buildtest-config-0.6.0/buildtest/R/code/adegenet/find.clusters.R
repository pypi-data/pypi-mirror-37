library(adegenet)
## Not run:
## THIS ONE TAKES A FEW MINUTES TO RUN ##
data(eHGDP)
## here, n.clust is specified, so that only on K value is used
grp <- find.clusters(eHGDP, max.n=30, n.pca=200, scale=FALSE,
n.clust=4) # takes about 2 minutes
names(grp)
grp$Kstat
grp$stat
## to try different values of k (interactive)
grp <- find.clusters(eHGDP, max.n=50, n.pca=200, scale=FALSE)
## and then, to plot BIC values:
plot(grp$Kstat, type="b", col="blue")
## ANOTHER SIMPLE EXAMPLE ##
data(sim2pop) # this actually contains 2 pop
## DETECTION WITH BIC (clear result)
foo.BIC <- find.clusters(sim2pop, n.pca=100, choose=FALSE)
plot(foo.BIC$Kstat, type="o", xlab="number of clusters (K)", ylab="BIC",
col="blue", main="Detection based on BIC")
points(2, foo.BIC$Kstat[2], pch="x", cex=3)
mtext(3, tex="'X' indicates the actual number of clusters")
## DETECTION WITH AIC (less clear-cut)
foo.AIC <- find.clusters(sim2pop, n.pca=100, choose=FALSE, stat="AIC")
plot(foo.AIC$Kstat, type="o", xlab="number of clusters (K)",
ylab="AIC", col="purple", main="Detection based on AIC")
points(2, foo.AIC$Kstat[2], pch="x", cex=3)
mtext(3, tex="'X' indicates the actual number of clusters")
## DETECTION WITH WSS (less clear-cut)
foo.WSS <- find.clusters(sim2pop, n.pca=100, choose=FALSE, stat="WSS")
plot(foo.WSS$Kstat, type="o", xlab="number of clusters (K)", ylab="WSS
(residual variance)", col="red", main="Detection based on WSS")
points(2, foo.WSS$Kstat[2], pch="x", cex=3)
mtext(3, tex="'X' indicates the actual number of clusters")
## TOY EXAMPLE FOR GENLIGHT OBJECTS ##
x <- glSim(100,500,500)
x
plot(x)
grp <- find.clusters(x, n.pca=100, choose=FALSE, stat="BIC")
plot(grp$Kstat, type="o", xlab="number of clusters (K)",
ylab="BIC",main="find.clusters on a genlight object\n(two groups)")
## End(Not run)

