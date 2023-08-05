library(ade4)
data(ours)
summary(ours)
if(adegraphicsLoaded()) {
g1 <- s1d.boxplot(dudi.acm(ours, scan = FALSE)$li[, 1], ours)
} else {
boxplot(dudi.acm(ours, scan = FALSE))
}
## Not run:
data(banque)
banque.acm <- dudi.acm(banque, scann = FALSE, nf = 3)
if(adegraphicsLoaded()) {
g2 <- adegraphics:::scatter.dudi(banque.acm)
} else {
scatter(banque.acm)
}
apply(banque.acm$cr, 2, mean)
banque.acm$eig[1:banque.acm$nf] # the same thing
if(adegraphicsLoaded()) {
g3 <- s1d.boxplot(banque.acm$li[, 1], banque)
g4 <- scatter(banque.acm)
} else {
boxplot(banque.acm)
scatter(banque.acm)
}
s.value(banque.acm$li, banque.acm$li[,3])
bb <- acm.burt(banque, banque)
bbcoa <- dudi.coa(bb, scann = FALSE)
plot(banque.acm$c1[,1], bbcoa$c1[,1])
# mca and coa of Burt table. Lebart & coll. section 1.4
bd <- acm.disjonctif(banque)
bdcoa <- dudi.coa(bd, scann = FALSE)
plot(banque.acm$li[,1], bdcoa$li[,1])
# mca and coa of disjonctive table. Lebart & coll. section 1.4
plot(banque.acm$co[,1], dudi.coa(bd, scann = FALSE)$co[,1])
## End(Not run)

