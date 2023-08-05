library(ff)
x <- ff(1:12)
is.open(x)
close(x)
is.open(x)
rm(x); gc()

