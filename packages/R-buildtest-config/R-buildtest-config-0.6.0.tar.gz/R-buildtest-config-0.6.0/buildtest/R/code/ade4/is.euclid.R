library(ade4)
w <- matrix(runif(10000), 100, 100)
w <- dist(w)
summary(w)
is.euclid (w) # TRUE
w <- quasieuclid(w) # no correction need in: quasieuclid(w)
w <- lingoes(w) # no correction need in: lingoes(w)
w <- cailliez(w) # no correction need in: cailliez(w)
rm(w)
