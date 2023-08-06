library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
data(tithonia)
tre <- read.tree(text=tithonia$tre)
traits <- log(tithonia$tab + 1)
rownames(traits) <- gsub("_", ".", rownames(traits))
## build a phylo4d object
x <- phylo4d(tre, traits)
par(mar=rep(.1,4))
table.phylo4d(x)
}
## End(Not run)
