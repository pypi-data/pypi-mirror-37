library(geiger)
geo <- get(data(geospiza))
treedata(geo$phy, geo$dat, sort=TRUE, warnings=TRUE)
