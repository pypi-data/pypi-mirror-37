library(ade4)
if(!adegraphicsLoaded()) {
if(requireNamespace("splancs", quietly = TRUE)) {
wxy <- data.frame(expand.grid(-3:3, -3:3))
names(wxy) <- c("x", "y")
z <- (1 / sqrt(2)) * exp(-(wxy$x ^ 2 + wxy$y ^ 2) / 2)
par(mfrow = c(2, 2))
s.value(wxy, z)
s.image(wxy, z)
s.image(wxy, z, kgrid = 5)
s.image(wxy, z, kgrid = 15)
par(mfrow = c(1, 1))
}
## Not run:
data(t3012)
if(requireNamespace("splancs", quietly = TRUE)) {
par(mfrow = c(3, 4))
for(k in 1:12)
s.image(t3012$xy, scalewt(t3012$temp[, k]), kgrid = 3)
par(mfrow = c(1, 1))
}
data(elec88)
if(requireNamespace("splancs", quietly = TRUE)) {
par(mfrow = c(3,4))
for(k in 1:12)
s.image(t3012$xy, scalewt(t3012$temp[, k]), kgrid = 3, sub = names(t3012$temp)[k],
csub = 3, area = elec88$area)
par(mfrow = c(1, 1))
}
## End(Not run)
}
