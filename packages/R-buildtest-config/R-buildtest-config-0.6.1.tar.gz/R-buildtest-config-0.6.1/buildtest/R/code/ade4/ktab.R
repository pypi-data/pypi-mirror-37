library(ade4)
data(friday87)
wfri <- data.frame(scale(friday87$fau, scal = FALSE))
wfri <- ktab.data.frame(wfri, friday87$fau.blo)
wfri[2:4, 1:5, 1:3]
c(wfri[2:4], wfri[5])
data(meaudret)
wit1 <- withinpca(meaudret$env, meaudret$design$season, scan = FALSE,
scal = "partial")
kta1 <- ktab.within(wit1, colnames = rep(c("S1","S2","S3","S4","S5"), 4))
kta2 <- t(kta1)
if(adegraphicsLoaded()) {
kplot(sepan(kta2), row.plab.cex = 1.5, col.plab.cex = 0.75)
} else {
kplot(sepan(kta2), clab.r = 1.5, clab.c = 0.75)
}
