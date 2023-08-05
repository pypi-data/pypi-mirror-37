library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
data(carni19)
tre <- read.tree(text=carni19$tre)
x <- phylo4d(tre, data.frame(carni19$bm))
table.phylo4d(x, ratio=.5, center=FALSE)
}
## End(Not run)
