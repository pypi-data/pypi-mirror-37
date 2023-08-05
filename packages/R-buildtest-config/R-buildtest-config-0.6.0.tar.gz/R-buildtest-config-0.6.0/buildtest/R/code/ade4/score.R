library(ade4)
## Not run:
par(mar = c(1, 1, 1, 1))
ade4:::scoreutil.base (runif(20, 3, 7), xlim = NULL, grid = TRUE, cgrid = 0.8,
include.origin = TRUE, origin = 0, sub = "Uniform", csub = 1)
## End(Not run)
# returns the value of the user coordinate of the low line.
# The user window id defined with c(0,1) in ordinate.
# box()
