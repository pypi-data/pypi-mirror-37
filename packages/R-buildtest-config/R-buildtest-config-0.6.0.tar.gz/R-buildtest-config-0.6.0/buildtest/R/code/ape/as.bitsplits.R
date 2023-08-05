library(ape)
tr <- rtree(20)
pp <- prop.part(tr)
as.bitsplits(pp)
## doesn't work for rooted trees...:
countBipartitions(rtree(10), rmtree(100, 10))
## ... but OK with unrooted trees:
countBipartitions(rtree(10, rooted = FALSE), rmtree(100, 10, rooted = FALSE))
