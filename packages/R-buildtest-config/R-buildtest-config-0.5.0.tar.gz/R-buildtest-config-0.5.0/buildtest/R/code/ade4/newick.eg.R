library(ade4)
data(newick.eg)
newick2phylog(newick.eg[[11]])
radial.phylog(newick2phylog(newick.eg[[7]]), circ = 1,
clabel.l = 0.75)
