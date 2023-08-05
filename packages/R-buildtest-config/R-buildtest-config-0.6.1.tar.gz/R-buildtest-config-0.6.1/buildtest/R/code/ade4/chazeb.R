library(ade4)
data(chazeb)
if(!adegraphicsLoaded())
plot(discrimin(dudi.pca(chazeb$tab, scan = FALSE),
chazeb$cla, scan = FALSE))
