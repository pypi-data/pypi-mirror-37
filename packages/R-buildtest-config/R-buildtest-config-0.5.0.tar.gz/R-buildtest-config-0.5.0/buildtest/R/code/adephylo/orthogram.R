library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
## a phylogenetic example
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
resid <- residuals(lm1)
abline(lm1)
## plot the two traits and the residuals of lm1
x <- phylo4d(tre, cbind.data.frame(afbw, neonatw, residuals=resid))
table.phylo4d(x) # residuals are surely not independant
## default orthogram for residuals of lm1
orthogram(resid, tre)
## using another orthonormal basis (derived from Abouheif's proximity)
myOrthoBasis <- orthobasis.phylo(tre, method="oriAbouheif") # Abouheif's proximities
orthogram(resid, ortho=myOrthoBasis) # significant phylog. signal
## Abouheif's test
W <- proxTips(tre, method="oriAbouheif") # proximity matrix
abouheif.moran(resid, W)
}
## End(Not run)
