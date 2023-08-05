library(adegenet)
## Not run:
data(woodmouse)
x <- DNAbin2genind(woodmouse)
x
genind2df(x)
## End(Not run)
if(require(seqinr)){
mase.res <- read.alignment(file=system.file("sequences/test.mase",package="seqinr"),
format = "mase")
mase.res
x <- alignment2genind(mase.res)
x
locNames(x) # list of polymorphic sites
genind2df(x)
## look at Euclidean distances
D <- dist(tab(x))
D
## summarise with a PCoA
pco1 <- dudi.pco(D, scannf=FALSE,nf=2)
scatter(pco1, posi="bottomright")
title("Principal Coordinate Analysis\n-based on proteic distances-")
}
