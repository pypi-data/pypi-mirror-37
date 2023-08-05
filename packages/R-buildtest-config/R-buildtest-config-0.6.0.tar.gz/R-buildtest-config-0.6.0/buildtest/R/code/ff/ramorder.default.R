library(ff)
n <- 50
x <- sample(c(NA, NA, 1:26), n, TRUE)
order(x)
i <- 1:n
ramorder(x, i)
i
x[i]
## Not run:
message("Note how the datatype influences sorting speed")
n <- 1e7
x <- sample(1:26, n, TRUE)
y <- as.double(x)
i <- 1:n
system.time(ramorder(y, i))
y <- as.integer(x)
i <- 1:n
system.time(ramorder(y, i))
y <- as.short(x)
i <- 1:n
system.time(ramorder(y, i))
y <- factor(letters)[x]
i <- 1:n
system.time(ramorder(y, i))
## End(Not run)
