library(adegenet)
## Not run:
#### HAPLOID EXAMPLE ####
## create a genotype of 100,000 SNPs
dat <- sample(c(0,1,NA), 1e5, prob=c(.495, .495, .01), replace=TRUE)
dat[1:10]
x <- new("SNPbin", dat)
x
x[1:10] # subsetting
as.integer(x[1:10])
## try a few accessors
ploidy(x)
nLoc(x)
head(x$snp[[1]]) # internal bit-level coding
## check that conversion is OK
identical(as(x, "integer"),as.integer(dat)) # SHOULD BE TRUE
## compare the size of the objects
print(object.size(dat), unit="auto")
print(object.size(x), unit="auto")
object.size(dat)/object.size(x) # EFFICIENCY OF CONVERSION
#### TETRAPLOID EXAMPLE ####
## create a genotype of 100,000 SNPs
dat <- sample(c(0:4,NA), 1e5, prob=c(rep(.995/5,5), 0.005), replace=TRUE)
x <- new("SNPbin", dat)
identical(as(x, "integer"),as.integer(dat)) # MUST BE TRUE
## compare the size of the objects
print(object.size(dat), unit="auto")
print(object.size(x), unit="auto")
object.size(dat)/object.size(x) # EFFICIENCY OF CONVERSION
#### c, cbind ####
a <- new("SNPbin", c(1,1,1,1,1))
b <- new("SNPbin", c(0,0,0,0,0))
a
b
ab <- c(a,b)
ab
identical(c(a,b),cbind(a,b))
as.integer(ab)
## End(Not run)

