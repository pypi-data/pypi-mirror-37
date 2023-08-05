library(adegenet)
## Not run:
x <- new("genlight", list(c(0,0,1,1,0), c(1,1,1,0,0,1), c(2,1,1,1,1,NA)))
x
as.matrix(x)
ploidy(x)
## compute statistics - allele as unit ##
glNA(x)
glSum(x)
glMean(x)
## compute statistics - individual as unit ##
glNA(x, FALSE)
glSum(x, FALSE)
glMean(x, FALSE)
## explanation: data are taken as relative frequencies
temp <- as.matrix(x)/ploidy(x)
apply(temp,2, function(e) sum(is.na(e))) # NAs
apply(temp,2,sum, na.rm=TRUE) # sum
apply(temp,2,mean, na.rm=TRUE) # mean
## End(Not run)

