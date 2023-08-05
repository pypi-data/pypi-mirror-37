library(ade4)
data(bf88)
fou1 <- foucart(bf88, scann = FALSE, nf = 3)
if(adegraphicsLoaded()) {
g <- kplot(fou1, row.plab.cex = 0, psub.cex = 2)
} else {
kplot(fou1, clab.c = 2, clab.r = 0, csub = 3)
}
