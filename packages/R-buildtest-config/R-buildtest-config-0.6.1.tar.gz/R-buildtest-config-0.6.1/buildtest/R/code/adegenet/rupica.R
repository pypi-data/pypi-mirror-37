library(adegenet)
data(rupica)
rupica
## Not run:
if(require(adehabitat)){
## see the sampling area
showBauges <- rupica$other$showBauges
showBauges()
points(rupica$other$xy,col="red")
## perform a sPCA
spca1 <- spca(rupica,type=5,d1=0,d2=2300,plot=FALSE,scannf=FALSE,nfposi=2,nfnega=0)
barplot(spca1$eig,col=rep(c("black","grey"),c(2,100)),main="sPCA eigenvalues")
screeplot(spca1,main="sPCA eigenvalues: decomposition")
## data visualization
showBauges(,labcex=1)
s.value(spca1$xy,spca1$ls[,1],add.p=TRUE,csize=.5)
add.scatter.eig(spca1$eig,1,1,1,posi="topleft",sub="Eigenvalues")
showBauges(,labcex=1)
s.value(spca1$xy,spca1$ls[,2],add.p=TRUE,csize=.5)
add.scatter.eig(spca1$eig,2,2,2,posi="topleft",sub="Eigenvalues")
rupica$other$showBauges()
colorplot(spca1$xy,spca1$li,cex=1.5,add.plot=TRUE)
## global and local tests
Gtest <- global.rtest(rupica@tab,spca1$lw,nperm=999)
Gtest
plot(Gtest)
Ltest <- local.rtest(rupica@tab,spca1$lw,nperm=999)
Ltest
plot(Ltest)
}
## End(Not run)

