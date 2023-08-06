library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
## load data, make tree and phylo4d object
data(procella)
tre <- read.tree(text=procella$tre)
x <- phylo4d(tre, procella$traits)
par(mar=rep(.1,4))
table.phylo4d(x,cex.lab=.7)
}
## End(Not run)
