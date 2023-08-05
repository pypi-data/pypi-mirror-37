library(ade4)
if(!adegraphicsLoaded()) {
xy <- cbind.data.frame(x = runif(200, -1, 1), y = runif(200, -1, 1))
posi <- factor(xy$x > 0) : factor(xy$y > 0)
coul <- c("black", "red", "green", "blue")
par(mfrow = c(2, 2))
s.class(xy, posi, cpoi = 2)
s.class(xy, posi, cell = 0, cstar = 0.5)
s.class(xy, posi, cell = 2, axesell = FALSE, csta = 0, col = coul)
s.chull(xy, posi, cpoi = 1)
par(mfrow = c(1, 1))
## Not run:
data(banque)
dudi1 <- dudi.acm(banque, scannf = FALSE)
coul = rainbow(length(levels(banque[, 20])))
par(mfrow = c(2, 2))
s.label(dudi1$li, sub = "Factorial map from ACM", csub = 1.5,
possub = "topleft")
s.class(dudi1$li, banque[, 20], sub = names(banque)[20],
possub = "bottomright", cell = 0, cstar = 0.5, cgrid = 0, csub = 1.5)
s.class(dudi1$li, banque[, 20], csta = 0, cell = 2, cgrid = 0,
clab = 1.5)
s.class(dudi1$li, banque[, 20], sub = names(banque)[20],
possub = "topright", cgrid = 0, col = coul)
par(mfrow = c(1, 1))
par(mfrow = n2mfrow(ncol(banque)))
for(i in 1:(ncol(banque)))
s.class(dudi1$li, banque[, i], clab = 1.5, sub = names(banque)[i],
csub = 2, possub = "topleft", cgrid = 0, csta = 0, cpoi = 0)
s.label(dudi1$li, clab = 0, sub = "Common background")
par(mfrow = c(1, 1))
## End(Not run)
}

