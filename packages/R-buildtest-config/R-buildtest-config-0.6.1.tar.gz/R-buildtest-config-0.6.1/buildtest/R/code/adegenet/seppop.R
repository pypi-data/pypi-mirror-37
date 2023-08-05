library(adegenet)
## Not run:
data(microbov)
strata(microbov) <- data.frame(other(microbov))
obj <- seppop(microbov)
names(obj)
obj$Salers
### example using strata
obj2 <- seppop(microbov, ~coun/spe)
names(obj2)
obj2$AF_BI
#### example for genlight objects ####
x <- new("genlight", list(a=rep(1,1e3),b=rep(0,1e3),c=rep(1, 1e3)))
x
pop(x) # no population info
pop(x) <- c("pop1","pop2", "pop1") # set population memberships
pop(x)
seppop(x)
as.matrix(seppop(x)$pop1)[,1:20]
as.matrix(seppop(x)$pop2)[,1:20,drop=FALSE]
## End(Not run)
