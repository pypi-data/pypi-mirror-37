library(adegenet)
if(require(ape)){
data(woodmouse)
g <- gengraph(woodmouse, cutoff=5)
g
plot(g$graph)
}
