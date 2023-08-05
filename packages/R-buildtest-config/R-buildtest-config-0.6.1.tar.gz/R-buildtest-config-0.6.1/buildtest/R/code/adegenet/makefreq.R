library(adegenet)
## Not run:
data(microbov)
obj1 <- microbov
obj2 <- genind2genpop(obj1)
# perform a correspondance analysis on counts data
Xcount <- tab(obj2, NA.method="zero")
ca1 <- dudi.coa(Xcount,scannf=FALSE)
s.label(ca1$li,sub="Correspondance Analysis",csub=1.2)
add.scatter.eig(ca1$eig,nf=2,xax=1,yax=2,posi="topleft")
# perform a principal component analysis on frequency data
Xfreq <- makefreq(obj2, missing="mean")
Xfreq <- tab(obj2, NA.method="mean") # equivalent to line above
pca1 <- dudi.pca(Xfreq,scale=FALSE,scannf=FALSE)
s.label(pca1$li,sub="Principal Component Analysis",csub=1.2)
add.scatter.eig(pca1$eig,nf=2,xax=1,yax=2,posi="top")
## End(Not run)

