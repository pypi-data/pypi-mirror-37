library(adegenet)
## Not run:
data(nancycats)
propTyped(nancycats,by="loc")
propTyped(genind2genpop(nancycats),by="both")
## End(Not run)
