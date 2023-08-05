library(ade4)
## Not run:
data(newick.eg)
w.phy <- newick2phylog(newick.eg[[9]])
w.tab <- data.frame(matrix(rnorm(620), 31, 20))
row.names(w.tab) <- sort(names(w.phy$leaves))
table.phylog(w.tab, w.phy, csi = 1.5, f = 0.5,
clabel.n = 0.75, clabel.c = 0.5)
## End(Not run)

