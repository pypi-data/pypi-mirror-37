library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
data(maples)
## see the tree
tre <- read.tree(text=maples$tre)
plot(tre)
axisPhylo()
## look at two variables
dom <- maples$tab$Dom
bif <- maples$tab$Bif
plot(bif,dom,pch = 20)
abline(lm(dom~bif)) # a strong negative correlation ?
summary(lm(dom~bif))
cor.test(bif,dom)
## look at the two variables onto the phylogeny
temp <- phylo4d(tre, data.frame(dom,bif, row.names=tre$tip.label))
table.phylo4d(temp) # correlation is strongly linked to phylogeny
## use ape's PIC (phylogenetic independent contrasts)
pic.bif <- pic(bif, tre)
pic.dom <- pic(dom, tre)
cor.test(pic.bif, pic.dom) # correlation is no longer significant
}
## End(Not run)
