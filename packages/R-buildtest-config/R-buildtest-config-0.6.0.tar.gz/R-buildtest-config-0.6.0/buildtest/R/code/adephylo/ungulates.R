library(adephylo)
## Not run:
if(require(ape) && require(phylobase)){
## load data
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
x <- phylo4d(tre, cbind.data.frame(afbw, neonatw)) # traits on the phylogeny
## test phylogenetic inertia in residuals
orthogram(residuals(lm1), x)
}
## End(Not run)
