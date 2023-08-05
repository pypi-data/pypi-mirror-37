library(adegenet)
## Not run:
## show the example file ##
## this is the path to the file:
system.file("files/exampleSnpDat.snp",package="adegenet")
## show its content:
file.show(system.file("files/exampleSnpDat.snp",package="adegenet"))
## read the file
obj <-
read.snp(system.file("files/exampleSnpDat.snp",package="adegenet"), chunk=2)
obj
as.matrix(obj)
ploidy(obj)
alleles(obj)
locNames(obj)
## End(Not run)

