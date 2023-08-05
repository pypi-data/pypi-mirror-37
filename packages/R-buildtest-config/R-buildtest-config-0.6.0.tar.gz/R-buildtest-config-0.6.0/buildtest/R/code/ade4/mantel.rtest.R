library(ade4)
data(yanomama)
gen <- quasieuclid(as.dist(yanomama$gen))
geo <- quasieuclid(as.dist(yanomama$geo))
plot(r1 <- mantel.rtest(geo,gen), main = "Mantel's test")
r1

