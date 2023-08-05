library(ade4)
data(chazeb)
dis1 <- discrimin(dudi.pca(chazeb$tab, scan = FALSE), chazeb$cla,
scan = FALSE)
dis1
if(!adegraphicsLoaded())
plot(dis1)
data(skulls)
plot(discrimin(dudi.pca(skulls, scan = FALSE), gl(5,30),
scan = FALSE))
