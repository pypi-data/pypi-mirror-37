library(adegenet)
## Not run:
data(dapcIllus)
attach(dapcIllus)
a # this is a genind object, like b, c, and d.
## FINS CLUSTERS EX NIHILO
clust.a <- find.clusters(a, n.pca=100, n.clust=6)
clust.b <- find.clusters(b, n.pca=100, n.clust=6)
clust.c <- find.clusters(c, n.pca=100, n.clust=12)
clust.d <- find.clusters(d, n.pca=100, n.clust=24)
## examin outputs
names(clust.a)
lapply(clust.a, head)
## PERFORM DAPCs
dapc.a <- dapc(a, pop=clust.a$grp, n.pca=100, n.da=5)
dapc.b <- dapc(b, pop=clust.b$grp, n.pca=100, n.da=5)
dapc.c <- dapc(c, pop=clust.c$grp, n.pca=100, n.da=11)
dapc.d <- dapc(d, pop=clust.d$grp, n.pca=100, n.da=23)
## LOOK AT ONE RESULT
dapc.a
summary(dapc.a)
## FORM A LIST OF RESULTS FOR THE 4 DATASETS
lres <- list(dapc.a, dapc.b, dapc.c, dapc.d)
## DRAW 4 SCATTERPLOTS
par(mfrow=c(2,2))
lapply(lres, scatter)
# detach data
detach(dapcIllus)
## End(Not run)

