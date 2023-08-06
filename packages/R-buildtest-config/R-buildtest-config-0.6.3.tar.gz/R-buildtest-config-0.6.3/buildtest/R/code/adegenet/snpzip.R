library(adegenet)
## Not run:
simpop <- glSim(100, 10000, n.snp.struc = 10, grp.size = c(0.3,0.7),
LD = FALSE, alpha = 0.4, k = 4)
snps <- as.matrix(simpop)
phen <- simpop@pop
outcome <- snpzip(snps, phen, method = "centroid")
outcome
## End(Not run)
## Not run:
simpop <- glSim(100, 10000, n.snp.struc = 10, grp.size = c(0.3,0.7),
LD = FALSE, alpha = 0.4, k = 4)
snps <- as.matrix(simpop)
phen <- simpop@pop
dapc1 <- dapc(snps, phen, n.da = 1, n.pca = 30)
features <- snpzip(dapc1, loading.plot = TRUE, method = "average")
features
## End(Not run)
