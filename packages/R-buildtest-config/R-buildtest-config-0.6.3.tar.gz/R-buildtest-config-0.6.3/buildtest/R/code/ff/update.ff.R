library(ff)
x <- ff(1:100)
y <- ff(-(1:100))
message("You should make it a habit to re-assign the return value
of update although this is not needed currently.")
x <- update(x, from=y)
x
y
x[] <- 1:100
x <- update(x, from=y, delete=NA)
x
y
x <- update(x, from=y, delete=TRUE)
x
y
x
rm(x,y); gc()
## Not run:
message("timings")
x <- ff(1:10000000)
y <- ff(-(1:10000000))
system.time(update(x, from=y))
system.time(update(y, from=x, delete=NA))
system.time(update(x, from=y, delete=TRUE))
rm(x,y); gc()
## End(Not run)

