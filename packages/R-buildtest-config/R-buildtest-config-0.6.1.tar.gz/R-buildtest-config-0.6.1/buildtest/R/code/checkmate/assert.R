library(checkmate)
x = 1:10
assert(checkNull(x), checkInteger(x, any.missing = FALSE))
## Not run:
x = 1
assert(checkChoice(x, c("a", "b")), checkDataFrame(x))
## End(Not run)
