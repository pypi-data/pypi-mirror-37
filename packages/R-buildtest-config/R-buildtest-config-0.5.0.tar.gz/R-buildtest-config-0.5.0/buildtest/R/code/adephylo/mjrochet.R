library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
data(mjrochet)
tre <- read.tree(text=mjrochet$tre) # make a tree
traits <- log((mjrochet$tab))
## build a phylo4d
mjr <- phylo4d(tre, traits)
## see data
table.phylo4d(mjr,cex.lab=.5,show.node=FALSE,symb="square")
## perform Abouheif's test for each trait
mjr.tests <- abouheif.moran(mjr, nrep=499)
mjr.tests
}
## End(Not run)
