library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
## load data, make a tree and a phylo4d object
data(palm)
tre <- read.tree(text=palm$tre)
rord <- as.integer(palm$traits$rord) # just use this for plotting purpose
traits <- data.frame(rord, palm$traits[,-1])
x <- phylo4d(tre, traits)
## plot data
par(mar=rep(.1,4))
table.phylo4d(x, cex.lab=.6)
## test phylogenetic autocorrelation
if(require(ade4)){
prox <- proxTips(x, method="sumDD")
phylAutoTests <- gearymoran(prox, traits[,-3], nrep=499)
plot(phylAutoTests)
}
}
## End(Not run)

