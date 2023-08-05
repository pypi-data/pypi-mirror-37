library(adegenet)
## Not run:
## show the example file ##
## this is the path to the file:
myPath <- system.file("files/usflu.fasta",package="adegenet")
myPath
## read the file
obj <- fasta2genlight(myPath, chunk=10) # process 10 sequences at a time
obj
## look at extracted information
position(obj)
alleles(obj)
locNames(obj)
## plot positions of polymorphic sites
temp <- density(position(obj), bw=10)
plot(temp, xlab="Position in the alignment", lwd=2, main="Location of the SNPs")
points(position(obj), rep(0, nLoc(obj)), pch="|", col="red")
## End(Not run)

