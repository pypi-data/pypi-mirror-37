library(ade4)
data(ours)
if(adegraphicsLoaded()) {
s1d.boxplot(dudi.acm(ours, scan = FALSE)$l1[, 1], ours)
} else {
boxplot(dudi.acm(ours, scan = FALSE))
}
