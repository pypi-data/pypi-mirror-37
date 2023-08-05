library(ade4)
data(humDNAm)
dpcoahum <- dpcoa(data.frame(t(humDNAm$samples)), sqrt(humDNAm$distances), scan = FALSE, nf = 2)
dpcoahum
if(adegraphicsLoaded()) {
g1 <- plot(dpcoahum)
} else {
plot(dpcoahum)
}
## Not run:
data(ecomor)
dtaxo <- dist.taxo(ecomor$taxo)
dpcoaeco <- dpcoa(data.frame(t(ecomor$habitat)), dtaxo, scan = FALSE, nf = 2)
dpcoaeco
if(adegraphicsLoaded()) {
g1 <- plot(dpcoaeco)
} else {
plot(dpcoaeco)
}
## End(Not run)
