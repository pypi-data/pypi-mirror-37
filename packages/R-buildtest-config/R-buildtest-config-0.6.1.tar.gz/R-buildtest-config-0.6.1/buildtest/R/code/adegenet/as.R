library(adegenet)
## Not run:
data(microbov)
x <- tab(microbov,NA.method="mean")
as(x[1:3],"data.frame")
## dudi functions attempt to convert their first argument
## to a data.frame; so they can be used on genind/genpop objects.
## perform a PCA
pca1 <- dudi.pca(x, scale=FALSE, scannf=FALSE)
pca1
x <- genind2genpop(microbov,miss="chi2")
x <- as(x,"ktab")
class(x)
## perform a STATIS analysis
statis1 <- statis(x, scannf=FALSE)
statis1
plot(statis1)
## End(Not run)
