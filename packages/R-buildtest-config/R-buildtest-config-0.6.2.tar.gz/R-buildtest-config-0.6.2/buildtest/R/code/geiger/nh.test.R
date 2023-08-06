library(geiger)
data(whales)
tmp <- treedata(whales$phy, whales$dat[,1])
phy <- tmp$phy
dat <- tmp$data[,1]
nh.test(phy, dat, regression.type="lm", show.plot=TRUE)
