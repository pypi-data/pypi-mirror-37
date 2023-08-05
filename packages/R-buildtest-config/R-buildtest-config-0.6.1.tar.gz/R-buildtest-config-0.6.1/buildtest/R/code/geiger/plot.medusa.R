library(geiger)
dat=get(data(whales))
phy=dat$phy
richness=dat$richness
res <- medusa(phy, richness)
# select best model based on AICc (showing the third model as best)
plot(res, cex=0.5, label.offset=1) # using plot.medusa()
title("AICc-chosen model")
