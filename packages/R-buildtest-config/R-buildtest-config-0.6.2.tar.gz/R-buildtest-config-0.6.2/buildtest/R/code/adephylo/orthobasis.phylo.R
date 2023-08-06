library(adephylo)
if(require(ape) && require(phylobase)){
## SIMPLE EXAMPLE ##
## make a tree
x <- rtree(50)
## compute Moran's eigenvectors
ME <- me.phylo(x, met="Abouheif")
ME
## plot the 10 first vectors
obj <- phylo4d(x, as.data.frame(ME[,1:10]))
table.phylo4d(obj, cex.sym=.7, cex.lab=.7)
## Not run:
## REMOVING PHYLOGENETIC AUTOCORRELATION IN A MODEL ##
## use example in ungulates dataset
data(ungulates)
tre <- read.tree(text=ungulates$tre)
plot(tre)
## look at two traits
afbw <- log(ungulates$tab[,1])
neonatw <- log((ungulates$tab[,2]+ungulates$tab[,3])/2)
names(afbw) <- tre$tip.label
names(neonatw) <- tre$tip.label
plot(afbw, neonatw) # relationship between traits
lm1 <- lm(neonatw~afbw)
abline(lm1)
lm1
resid1 <- residuals(lm1)
orthogram(resid1, tre) # residuals are autocorrelated
## compute Moran's eigenvectors (ME)
myME <- me.phylo(tre, method="Abou")
lm2 <- lm(neonatw ~ myME[,1] + afbw) # use for ME as covariable
resid2 <- residuals(lm2)
orthogram(resid2, tre) # there is no longer phylogenetic autocorrelation
## see the difference
table.phylo4d(phylo4d(tre, cbind.data.frame(resid1, resid2)))
## End(Not run)
}
