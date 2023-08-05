library(ade4)
data(ardeche)
dudi1 <- dudi.coa(ardeche$tab, scan = FALSE)
s.class(dudi1$co, ardeche$dat.fac)
if(adegraphicsLoaded()) {
s.label(dudi1$co, plab.cex = 0.5, add = TRUE)
} else {
s.label(dudi1$co, clab = 0.5, add.p = TRUE)
}
