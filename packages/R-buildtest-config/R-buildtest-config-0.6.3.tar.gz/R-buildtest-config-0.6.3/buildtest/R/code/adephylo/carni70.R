library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
data(carni70)
rownames(carni70$tab) <- gsub("_", ".", rownames(carni70$tab))
tre <- read.tree(text=carni70$tre)
x <- phylo4d(tre, carni70$tab)
table.phylo4d(x)
par(mar=rep(.1,4))
table.phylo4d(x,cex.lab=.5, show.n=FALSE, ratio=.5)
## transform size in log and test for a phylogenetic signal
size <- log(carni70$tab)[,1]
names(size) <- row.names(carni70$tab)
orthogram(size, tre)
## transform range and test for a phylogenetic signal
yrange <- scale(carni70$tab)[,2]
names(yrange) <- row.names(carni70$tab)
orthogram(yrange, tre)
}
## End(Not run)
