library(adegenet)
## Not run:
## simulate a toy dataset
x <- glSim(50,4e3, 50, ploidy=2)
x
plot(x)
## perform PCA
pca1 <- glPca(x, nf=2)
## plot eigenvalues
barplot(pca1$eig, main="eigenvalues", col=heat.colors(length(pca1$eig)))
## basic plot
scatter(pca1, ratio=.2)
## plot showing groups
s.class(pca1$scores, pop(x), col=colors()[c(131,134)])
add.scatter.eig(pca1$eig,2,1,2)
## End(Not run)
