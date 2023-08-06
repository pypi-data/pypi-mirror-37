library(ape)
tr <- rcoal(5)
(x <- evonet(tr, 6:7, 8:9))
plot(x)

