library(ff)
message("Let's create a factor with little levels")
x <- ff(letters[4:6], levels=letters[4:6])
message("Let's interpret the same ff file without levels in order to see the codes")
y <- x
levels(y) <- NULL
levels(x)
data.frame(factor=x[], codes=y[])
levels(x) <- appendLevels(levels(x), letters)
levels(x)
data.frame(factor=x[], codes=y[])
x <- sortLevels(x) # implicit recoding is chunked were necessary
levels(x)
data.frame(factor=x[], codes=y[])
message("NEVER forget to reassign the result of recodeLevels or sortLevels,
look at the following mess")
recodeLevels(x, rev(levels(x)))
message("NOW the codings have changed, but not the levels, the result is wrong data")
levels(x)
data.frame(factor=x[], codes=y[])
rm(x);gc()
## Not run:
n <- 5e7
message("reading a factor from a file ist as fast ...")
system.time(
fx <- ff(factor(letters[1:25]), length=n)
)
system.time(x <- fx[])
str(x)
rm(x); gc()
message("... as creating it in-RAM (R-2.11.1) which is theoretically impossible ...")
system.time({
x <- integer(n)
x[] <- 1:25
levels(x) <- letters[1:25]
class(x) <- "factor"
})
str(x)
rm(x); gc()
message("... but is possible if we avoid some unnecessary copying that is triggered
by assignment functions")
system.time({
x <- integer(n)
x[] <- 1:25
setattr(x, "levels", letters[1:25])
setattr(x, "class", "factor")
})
str(x)
rm(x); gc()
rm(n)
## End(Not run)

