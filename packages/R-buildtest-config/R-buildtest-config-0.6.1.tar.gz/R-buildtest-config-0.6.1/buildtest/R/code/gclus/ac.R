library(gclus)
x <- runif(20)
y <- runif(20)
g <- rep(c("a","b"),10)
ac(x,y)
sil(x,y,g)

