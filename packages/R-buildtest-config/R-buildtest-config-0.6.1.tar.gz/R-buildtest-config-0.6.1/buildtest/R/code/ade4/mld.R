library(ade4)
## Not run:
# decomposition of a time serie
data(co2)
x <- log(co2)
orthobas <- orthobasis.line(length(x))
level<-rep("D", 467)
level[1:3]<-rep("A", 3)
level[c(77,78,79,81)]<-rep("B", 4)
level[156]<-"C"
level<-as.factor(level)
res <- mld(x, orthobas, level)
sum(scale(x, scale = FALSE) - apply(res, 1, sum))
## End(Not run)
# decomposition of a biological trait on a phylogeny
data(palm)
vfruit<-palm$traits$vfruit
vfruit<-scalewt(vfruit)
palm.phy<-newick2phylog(palm$tre)
level <- rep("F", 65)
level[c(4, 21, 3, 6, 13)] <- LETTERS[1:5]
level <- as.factor(level)
res <- mld(as.vector(vfruit), palm.phy$Bscores, level,
phylog = palm.phy, clabel.nod = 0.7, f.phylog=0.8,
csize = 2, clabel.row = 0.7, clabel.col = 0.7)
