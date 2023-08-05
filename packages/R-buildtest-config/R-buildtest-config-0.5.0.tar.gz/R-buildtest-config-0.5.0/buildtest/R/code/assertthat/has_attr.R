library(assertthat)
has_attr(has_attr, "fail")
x <- 10
x %has_attr% "a"
y <- list(a = 1, b = 2)
see_if(y %has_name% "c")

