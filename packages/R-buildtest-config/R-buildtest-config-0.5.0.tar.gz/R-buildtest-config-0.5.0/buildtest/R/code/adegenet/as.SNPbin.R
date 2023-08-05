library(adegenet)
## Not run:
## data to be converted
dat <- c(1,0,0,2,1,1,1,2,2,1,1,0,0,1)
## using the constructor
x1 <- new("SNPbin", dat)
x1
## using 'as' methods
x2 <- as.SNPbin(dat)
x3 <- as(dat, "SNPbin")
identical(x1,x2)
identical(x1,x3)
## End(Not run)
