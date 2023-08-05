library(ape)
data(chiroptera)
str(chiroptera)
op <- par()
par(cex = 0.3)
plot(chiroptera, type = "c")
par(op)

