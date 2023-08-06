library(ade4)
data(lascaux)
if(adegraphicsLoaded()) {
plot(dudi.acm(lascaux$ornem, sca = FALSE))
} else {
scatter(dudi.acm(lascaux$ornem, sca = FALSE), csub = 3)
}
