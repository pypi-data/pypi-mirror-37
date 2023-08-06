library(adephylo)
## Not run:
if(require(ape) & require(phylobase)){
## make a tree
x <- as(rtree(20),"phylo4")
plot(x,show.node=TRUE)
## get shortest path between tip 1 and all other tips.
sp.tips(x, "t1", "t2")
sp.tips(x, 1, 2:20, TRUE)
}
## End(Not run)
