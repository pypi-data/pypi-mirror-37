library(ape)
data(bird.orders)
hc <- as.hclust(bird.orders)
tr <- as.phylo(hc)
all.equal(bird.orders, tr) # TRUE
### shows the three plots for tree objects:
dend <- as.dendrogram(hc)
layout(matrix(c(1:3, 3), 2, 2))
plot(bird.orders, font = 1)
plot(hc)
par(mar = c(8, 0, 0, 0)) # leave space for the labels
plot(dend)
### how to get identical plots with
### plot.phylo and plot.dendrogram:
layout(matrix(1:2, 2, 1))
plot(bird.orders, font = 1, no.margin = TRUE, label.offset = 0.4)
par(mar = c(0, 0, 0, 8))
plot(dend, horiz = TRUE)
layout(1)
## Not run:
### convert into networks:
if (require(network)) {
x <- as.network(rtree(10))
print(x)
plot(x, vertex.cex = 1:4)
plot(x, displaylabels = TRUE)
}
tr <- rtree(5)
if (require(igraph)) {
print((x <- as.igraph(tr)))
plot(x)
print(as.igraph(tr, TRUE, FALSE))
print(as.igraph(tr, FALSE, FALSE))
}
## End(Not run)

