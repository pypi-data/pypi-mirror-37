library(ape)
data(carnivora)
plot(as.phylo(~SuperFamily/Family/Genus/Species, data=carnivora))
