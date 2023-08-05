library(adegenet)
## Not run:
## data to be converted
dat <- list(toto=c(1,1,0,0,2,2,1,2,NA), titi=c(NA,1,1,0,1,1,1,0,0), tata=c(NA,0,3, NA,1,1,1,0,0))
## using the constructor
x1 <- new("genlight", dat)
x1
## using 'as' methods
x2 <- as.genlight(dat)
x3 <- as(dat, "genlight")
identical(x1,x2)
identical(x1,x3)
## End(Not run)

