library(ape)
# Oribatid mite data from Borcard and Legendre (1994)
## Not run:
if (require(vegan)) {
data(mite) # Community composition data, 70 peat cores, 35 species
# Select rows 1:30. Species 35 is absent from these rows. Transform to log
mite.log <- log(mite[1:30,-35]+1) # Equivalent: log1p(mite[1:30,-35])
# Principal coordinate analysis and simple ordination plot
mite.D <- vegdist(mite.log, "bray")
res <- pcoa(mite.D)
res$values
biplot(res)
# Project unstandardized and standardized species on the PCoA ordination plot
mite.log.st = apply(mite.log, 2, scale, center=TRUE, scale=TRUE)
par(mfrow=c(1,2))
biplot(res, mite.log)
biplot(res, mite.log.st)
# Reverse the ordination axes in the plot
par(mfrow=c(1,2))
biplot(res, mite.log, dir.axis1=-1, dir.axis2=-1)
biplot(res, mite.log.st, dir.axis1=-1, dir.axis2=-1)
}
## End(Not run)
