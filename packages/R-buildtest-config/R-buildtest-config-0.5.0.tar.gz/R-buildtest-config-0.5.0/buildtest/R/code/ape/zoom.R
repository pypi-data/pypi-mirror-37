library(ape)
## Not run:
data(chiroptera)
zoom(chiroptera, 1:20, subtree = TRUE)
zoom(chiroptera, grep("Plecotus", chiroptera$tip.label))
zoom(chiroptera, list(grep("Plecotus", chiroptera$tip.label),
grep("Pteropus", chiroptera$tip.label)))
## End(Not run)
