library(adegenet)
showClass("genind")
obj <- read.genetix(system.file("files/nancycats.gtx",package="adegenet"))
obj
validObject(obj)
summary(obj)
## Not run:
# test inter-colonies structuration
if(require(hierfstat)){
gtest <- gstat.randtest(obj,nsim=99)
gtest
plot(gtest)
}
# perform a between-class PCA
pca1 <- dudi.pca(scaleGen(obj, NA.method="mean"),scannf=FALSE,scale=FALSE)
pcabet1 <- between(pca1,obj@pop,scannf=FALSE)
pcabet1
s.class(pcabet1$ls,obj@pop,sub="Inter-class PCA",possub="topleft",csub=2)
add.scatter.eig(pcabet1$eig,2,xax=1,yax=2)
## End(Not run)
