library(ade4)
## Not run:
data(avimedi)
coa1 <- dudi.coa(avimedi$fau, scan = FALSE, nf = 3)
bet1 <- bca(coa1, avimedi$plan$str, scan = FALSE)
wit1 <- wca(coa1, avimedi$plan$reg, scan=FALSE)
pcaiv1 <- pcaiv(coa1, avimedi$plan, scan = FALSE)
if(adegraphicsLoaded()) {
g1 <- s.class(coa1$li, avimedi$plan$str:avimedi$plan$reg,
psub.text = "Correspondences Analysis", plot = FALSE)
g2 <- s.class(bet1$ls, avimedi$plan$str, psub.text = "Between Analysis", plot = FALSE)
g3 <- s.class(wit1$li, avimedi$plan$str, psub.text = "Within Analysis", plot = FALSE)
g41 <- s.match(pcaiv1$li, pcaiv1$ls, plabels.cex = 0,
psub.text = "Canonical Correspondences Analysis", plot = FALSE)
g42 <- s.class(pcaiv1$li, avimedi$plan$str:avimedi$plan$reg, plot = FALSE)
g4 <- superpose(g41, g42, plot = FALSE)
G <- ADEgS(list(g1, g2, g3, g4), layout = c(2, 2))
} else {
par(mfrow = c(2,2))
s.class(coa1$li,avimedi$plan$str:avimedi$plan$reg,
sub = "Correspondences Analysis")
s.class(bet1$ls, avimedi$plan$str,
sub = "Between Analysis")
s.class(wit1$li, avimedi$plan$str,
sub = "Within Analysis")
s.match(pcaiv1$li, pcaiv1$ls, clab = 0,
sub = "Canonical Correspondences Analysis")
s.class(pcaiv1$li, avimedi$plan$str:avimedi$plan$reg,
add.plot = TRUE)
par(mfrow=c(1,1))
}
## End(Not run)
