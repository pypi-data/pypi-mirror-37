library(adegenet)
## Not run:
## no structure
x <- glSim(100, 1e3, ploid=2)
plot(x)
## 1,000 non structured SNPs, 100 structured SNPs
x <- glSim(100, 1e3, n.snp.struc=100, ploid=2)
plot(x)
## 1,000 non structured SNPs, 100 structured SNPs, ploidy=4
x <- glSim(100, 1e3, n.snp.struc=100, ploid=4)
plot(x)
## same thing, stronger differences between groups
x <- glSim(100, 1e3, n.snp.struc=100, ploid=2, alpha=0.4)
plot(x)
## same thing, loci with LD structures
x <- glSim(100, 1e3, n.snp.struc=100, ploid=2, alpha=0.4, LD=TRUE, block.minsize=100)
plot(x)
## End(Not run)
