library(ape)
## Not run:
tr <- rcoal(30)
### Five traits, one observation per species:
x <- replicate(5, rTraitCont(tr, sigma = 1))
varCompPhylip(x, tr) # varE is small
x <- replicate(5, rnorm(30))
varCompPhylip(x, tr) # varE is large
### Five traits, ten observations per species:
x <- replicate(30, replicate(5, rnorm(10)), simplify = FALSE)
varCompPhylip(x, tr)
## End(Not run)
