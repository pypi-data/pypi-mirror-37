library(adephylo)
if(require(ape) & require(phylobase)){
## make a tree
x <- as(rtree(20),"phylo4")
plot(x,show.node=TRUE)
listTips(x)
}
