library(adegenet)
## Not run:
## use a subset of influenza data
data(H3N2)
set.seed(1)
dat <- H3N2[sample(1:nInd(H3N2), 100)]
## get pairwise distances
temp <- pairDistPlot(dat, other(dat)$epid)
## see raw data
head(temp$data)
## see plots
temp$boxplot
temp$violin
temp$jitter
## End(Not run)

