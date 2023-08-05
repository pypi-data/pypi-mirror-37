library(adegenet)
## Not run:
## LOAD DATA
data(nancycats)
## COMPUTE ALLELE FREQUENCIES
x <- nancycats
apply(tab(x, freq=TRUE),2,mean, na.rm=TRUE)
## GET MINOR ALLELE FREQUENCY
m.freq <- minorAllele(x)
m.freq
## End(Not run)

