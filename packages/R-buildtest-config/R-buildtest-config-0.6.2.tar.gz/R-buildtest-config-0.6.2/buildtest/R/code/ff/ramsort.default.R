library(ff)
n <- 50
x <- sample(c(NA, NA, 1:26), n, TRUE)
sort(x)
ramsort(x)
x
## Not run:
message("Note how the datatype influences sorting speed")
n <- 5e6
x <- sample(1:26, n, TRUE)
y <- as.double(x)
system.time(ramsort(y))
y <- as.integer(x)
system.time(ramsort(y))
y <- as.short(x)
system.time(ramsort(y))
y <- as.factor(letters)[x]
system.time(ramsort(y))
## End(Not run)

