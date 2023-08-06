library(adegenet)
## Not run:
## load data
data(microbov)
obj <- genind2genpop(microbov)
## compare different scaling
X1 <- scaleGen(obj)
X2 <- scaleGen(obj,met="bin")
## compute PCAs
pcaObj <- dudi.pca(obj,scale=FALSE,scannf=FALSE) # pca with no scaling
pcaX1 <- dudi.pca(X1,scale=FALSE,scannf=FALSE,nf=100) # pca with usual scaling
pcaX2 <- dudi.pca(X2,scale=FALSE,scannf=FALSE,nf=100) # pca with scaling for binomial variance
## get the loadings of alleles for the two scalings
U1 <- pcaX1$c1
U2 <- pcaX2$c1
## find an optimal plane to compare loadings
## use a procustean rotation of loadings tables
pro1 <- procuste(U1,U2,nf=2)
## graphics
par(mfrow=c(2,2))
# eigenvalues
barplot(pcaObj$eig,main="Eigenvalues\n no scaling")
barplot(pcaX1$eig,main="Eigenvalues\n usual scaling")
barplot(pcaX2$eig,main="Eigenvalues\n 'binomial' scaling")
# differences between loadings of alleles
s.match(pro1$scor1,pro1$scor2,clab=0,sub="usual -> binom (procustean rotation)")
## End(Not run)

