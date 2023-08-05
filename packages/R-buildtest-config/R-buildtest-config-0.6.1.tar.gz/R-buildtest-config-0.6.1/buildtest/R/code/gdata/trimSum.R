library(gdata)
x <- 1:10
trimSum(x, n=5)
trimSum(x, n=5, right=FALSE)
x[9] <- NA
trimSum(x, n=5)
trimSum(x, n=5, na.rm=TRUE)

