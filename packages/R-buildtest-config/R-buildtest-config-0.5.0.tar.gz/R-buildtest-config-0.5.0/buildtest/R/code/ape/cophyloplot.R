library(ape)
#two random trees
tree1 <- rtree(40)
tree2 <- rtree(20)
#creation of the association matrix:
association <- cbind(tree2$tip.label, tree2$tip.label)
cophyloplot(tree1, tree2, assoc = association,
length.line = 4, space = 28, gap = 3)
#plot with rotations
## Not run:
cophyloplot(tree1, tree2, assoc=association, length.line=4, space=28, gap=3, rotate=TRUE)
## End(Not run)

