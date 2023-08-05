library(ape)
## Not run:
#example 1: simple
tree1 <- rtree(50)
tree2 <- subtreeplot(tree1, wait = TRUE) # on exit, tree2 will be a subtree of tree1
#example 2: more than one zoom
tree1 <- rtree(60)
tree2 <- subtreeplot(subtreeplot(subtreeplot(tree1))) # allow three succssive zooms
## End(Not run)
