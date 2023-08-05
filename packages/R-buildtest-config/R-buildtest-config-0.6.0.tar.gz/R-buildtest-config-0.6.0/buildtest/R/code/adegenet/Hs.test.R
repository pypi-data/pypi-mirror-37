library(adegenet)
## Not run:
data(microbov)
Hs(microbov)
test <- Hs.test(microbov[pop="Borgou"],
microbov[pop="Lagunaire"],
n.sim=499)
test
plot(test)
## End(Not run)
