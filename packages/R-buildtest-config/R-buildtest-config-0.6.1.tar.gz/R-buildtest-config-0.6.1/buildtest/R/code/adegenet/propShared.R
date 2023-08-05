library(adegenet)
## Not run:
## make a small object
data(microbov)
obj <- microbov[1:5, loc = locNames(microbov)[1:2]]
## verify results
propShared(obj)
genind2df(obj,sep="|")
## Use this similarity measure inside a PCoA
## ! This is for illustration only !
## the distance should be rendered Euclidean before
## (e.g. using cailliez from package ade4).
matSimil <- propShared(microbov)
matDist <- exp(-matSimil)
D <- cailliez(as.dist(matDist))
pcoa1 <- dudi.pco(D,scannf=FALSE,nf=3)
s.class(pcoa1$li,microbov$pop,lab=popNames(microbov))
## End(Not run)

