library(adephylo)
## Not run:
if(require(ape) & require(phylobase)){
## make a tree
x <- as(rtree(10),"phylo4")
partition <- treePart(x)
partition
## plot the dummy vectors with the tree
temp <- phylo4d(x, partition)
table.phylo4d(temp, cent=FALSE, scale=FALSE)
}
## End(Not run)

