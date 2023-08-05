library(adegenet)
data(microbov)
strata(microbov) <- data.frame(other(microbov))
# Currently set on just
head(pop(microbov))
# setting the strata to both Pop and Subpop
setPop(microbov) <- ~coun/breed
head(pop(microbov))
## Not run:
# Can be used to create objects as well.
microbov.old <- setPop(microbov, ~spe)
head(pop(microbov.old))
## End(Not run)

