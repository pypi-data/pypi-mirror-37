library(ape)
## Not run:
tr <- rtree(20)
f <- function(col) {
o <- identify(tr)
nodelabels(node=o$nodes, pch = 19, col = col)
}
plot(tr)
f("red") # click close to a node
f("green")
## End(Not run)

