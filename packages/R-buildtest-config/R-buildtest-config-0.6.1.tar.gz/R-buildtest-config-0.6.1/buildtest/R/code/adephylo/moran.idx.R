library(adephylo)
## Not run:
## use maples dataset
data(maples)
tre <- read.tree(text=maples$tre)
dom <- maples$tab$Dom
bif <- maples$tab$Bif
## get a proximity matrix between tips
W <- proxTips(tre, met="Abouheif")
## compute Moran's I for two traits (dom and bif)
moran.idx(dom, W)
moran.idx(bif, W)
moran.idx(rnorm(nTips(tre)), W)
## build a simple permutation test for 'bif'
sim <- replicate(499, moran.idx(sample(bif), W)) # permutations
sim <- c(moran.idx(bif, W), sim)
pval <- mean(sim>=sim[1]) # right-tail p-value
pval
hist(sim, col="grey", main="Moran's I Monte Carlo test for 'bif'") # plot
mtext("Histogram of permutations and observation (in red)")
abline(v=sim[1], col="red", lwd=3)
## End(Not run)
