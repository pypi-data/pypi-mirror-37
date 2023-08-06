library(adegenet)
# a toy example
xy <- expand.grid(1:10,1:10)
df <- data.frame(x=1:100, y=100:1, z=runif(100,0,100))
colorplot(xy,df,cex=10,main="colorplot: toy example")
## Not run:
# a genetic example using a sPCA
if(require(spdep)){
data(spcaIllus)
dat3 <- spcaIllus$dat3
spca3 <- spca(dat3,xy=dat3$other$xy,ask=FALSE,type=1,plot=FALSE,scannf=FALSE,nfposi=1,nfnega=1)
colorplot(spca3, cex=4, main="colorplot: a sPCA example")
text(spca3$xy[,1], spca3$xy[,2], dat3$pop)
mtext("P1-P2 in cline\tP3 random \tP4 local repulsion")
}
## End(Not run)
