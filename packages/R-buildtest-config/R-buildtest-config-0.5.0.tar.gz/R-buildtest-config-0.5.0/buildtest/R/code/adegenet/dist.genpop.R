library(adegenet)
## Not run:
data(microsatt)
obj <- as.genpop(microsatt$tab)
listDist <- lapply(1:5, function(i) cailliez(dist.genpop(obj,met=i)))
for(i in 1:5) {attr(listDist[[i]],"Labels") <- popNames(obj)}
listPco <- lapply(listDist, dudi.pco,scannf=FALSE)
par(mfrow=c(2,3))
for(i in 1:5) {scatter(listPco[[i]],sub=paste("Dist:", i))}
## End(Not run)

