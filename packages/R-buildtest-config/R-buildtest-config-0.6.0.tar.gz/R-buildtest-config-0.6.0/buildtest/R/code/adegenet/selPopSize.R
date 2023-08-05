library(adegenet)
## Not run:
data(microbov)
table(pop(microbov))
obj <- selPopSize(microbov, n=50)
obj
table(pop(obj))
## End(Not run)
