library(ape)
ta <- rtree(30)
tb <- rtree(30)
dist.topo(ta, ta) # 0
dist.topo(ta, tb) # unlikely to be 0
