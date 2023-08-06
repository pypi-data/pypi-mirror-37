library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
## see data
data(lizards)
liz.tr <- read.tree(tex=lizards$hprA) # make a tree
liz <- phylo4d(liz.tr, lizards$traits) # make a phylo4d object
table.phylo4d(liz)
## compute and plot principal components
if(require(ade4)){
liz.pca1 <- dudi.pca(lizards$traits, cent=TRUE,
scale=TRUE, scannf=FALSE, nf=2) # PCA of traits
myPC <- phylo4d(liz.tr, liz.pca1$li) # store PC in a phylo4d object
varlab <- paste("Principal \ncomponent", 1:2) # make labels for PCs
table.phylo4d(myPC, ratio=.8, var.lab=varlab) # plot the PCs
add.scatter.eig(liz.pca1$eig,2,1,2,posi="topleft", inset=c(0,.15))
title("Phylogeny and the principal components")
## compute a pPCA ##
## remove size effect
temp <- lapply(liz.pca1$tab, function(e) residuals(lm(e~-1+liz.pca1$li[,1])) )
temp <- data.frame(temp)
row.names(temp) <- tipLabels(liz)
## build corresponding phylo4d object
liz.noSize <- phylo4d(liz.tr, temp)
ppca1 <- ppca(liz.noSize, method="Abouheif", scale=FALSE, scannf=FALSE)
plot(ppca1)
}
}
## End(Not run)
