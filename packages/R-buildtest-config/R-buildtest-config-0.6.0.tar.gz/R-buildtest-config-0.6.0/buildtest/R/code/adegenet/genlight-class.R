library(adegenet)
## Not run:
## TOY EXAMPLE ##
## create and convert data
dat <- list(toto=c(1,1,0,0), titi=c(NA,1,1,0), tata=c(NA,0,3, NA))
x <- new("genlight", dat)
x
## examine the content of the object
names(x)
x@gen
x@gen[[1]]@snp # bit-level coding for first individual
## conversions
as.list(x)
as.matrix(x)
## round trips - must return TRUE
identical(x, new("genlight", as.list(x))) # list
identical(x, new("genlight", as.matrix(x))) # matrix
identical(x, new("genlight", as.data.frame(x))) # data.frame
## test subsetting
x[c(1,3)] # keep individuals 1 and 3
as.list(x[c(1,3)])
x[c(1,3), 1:2] # keep individuals 1 and 3, loci 1 and 2
as.list(x[c(1,3), 1:2])
x[c(TRUE,FALSE), c(TRUE,TRUE,FALSE,FALSE)] # same, using logicals
as.list(x[c(TRUE,FALSE), c(TRUE,TRUE,FALSE,FALSE)])
## REAL-SIZE EXAMPLE ##
## 50 genotypes of 1,000,000 SNPs
dat <- lapply(1:50, function(i) sample(c(0,1,NA), 1e6, prob=c(.5, .49, .01), replace=TRUE))
names(dat) <- paste("indiv", 1:length(dat))
print(object.size(dat), unit="aut") # size of the original data
x <- new("genlight", dat) # conversion
x
print(object.size(x), unit="au") # size of the genlight object
object.size(dat)/object.size(x) # conversion efficiency
#### cbind, rbind ####
a <- new("genlight", list(toto=rep(1,10), tata=rep(c(0,1), each=5), titi=c(NA, rep(1,9)) ))
ara <- rbind(a,a)
ara
as.matrix(ara)
aca <- cbind(a,a)
aca
as.matrix(aca)
#### subsetting @other ####
x <- new("genlight", list(a=1,b=0,c=1), other=list(1:3, letters,data.frame(2:4)))
x
other(x)
x[2:3]
other(x[2:3])
other(x[2:3, treatOther=FALSE])
#### seppop ####
pop(x) # no population info
pop(x) <- c("pop1","pop1", "pop2") # set population memberships
pop(x)
seppop(x)
## End(Not run)
