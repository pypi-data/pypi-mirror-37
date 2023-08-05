library(ade4)
data(elec88)
par(mfrow = c(2, 2))
area.plot(elec88$area, cpoint = 1)
area.plot(elec88$area, lab = elec88$lab$dep, clab = 0.75)
area.plot(elec88$area, clab = 0.75)
# elec88$neig <- neig(area = elec88$area)
area.plot(elec88$area, graph = elec88$neig, sub = "Neighbourhood graph", possub = "topright")
par(mfrow = c(1, 1))
## Not run:
par(mfrow = c(3, 3))
for(i in 1:9) {
x <- elec88$tab[,i]
area.plot(elec88$area, val = x, sub = names(elec88$tab)[i], csub = 3, cleg = 1.5)
}
par(mfrow = c(1, 1))
if(adegraphicsLoaded()) {
if(requireNamespace("sp", quietly = TRUE)) {
s.value(elec88$xy, elec88$tab, Sp = elec88$Spatial,
method = "color", psub.text = names(elec88$tab), psub.cex = 3,
pSp.col = "white", pgrid.draw = FALSE, porigin.include = FALSE)
}
} else {
par(mfrow = c(3, 3))
for(i in 1:9) {
x <- elec88$tab[, i]
s.value(elec88$xy, elec88$tab[, i], contour = elec88$contour,
meth = "greylevel", sub = names(elec88$tab)[i], csub = 3,
cleg = 1.5, incl = FALSE)
}
par(mfrow = c(1, 1))
}
if(!adegraphicsLoaded()) {
data(irishdata)
par(mfrow = c(2, 2))
w <- ade4:::area.util.contour(irishdata$area)
xy <- ade4:::area.util.xy(irishdata$area)
area.plot(irishdata$area, cpoint = 1)
apply(w, 1, function(x) segments(x[1], x[2], x[3], x[4], lwd = 3))
area.plot(irishdata$area, clabel = 1)
s.label(xy, area = irishdata$area, incl = FALSE, clab = 0,
cpoi = 3, addax = FALSE, contour = w)
s.label(xy, area = irishdata$area, incl = FALSE,
addax = FALSE, contour = w)
if(requireNamespace("maptools", quietly = TRUE) & requireNamespace("spdep", quietly = TRUE)) {
data(columbus, package = "spdep")
par(mfrow = c(2, 2))
plot(col.gal.nb, coords, pch = 20, cex = 2)
col.gal.neig <- nb2neig(col.gal.nb)
s.label(data.frame(coords), neig = col.gal.neig,
inc = FALSE, addax = FALSE, clab = 0, cneig = 1, cpo = 2)
maptools:::plot.polylist(polys, bbs)
area.plot(poly2area(polys))
# 1
crime.f <- as.ordered(cut(columbus$CRIME,
breaks = quantile(columbus$CRIME, probs = seq(0, 1, 0.2)),
include.lowest = TRUE))
colours <- c("salmon1", "salmon2", "red3", "brown", "black")
plot(bbs[, 1], bbs[, 4], xlab = "", ylab = "", asp = 1, type = "n",
xlim = range(c(bbs[, 1], bbs[, 3])), ylim = range(c(bbs[, 2],
bbs[, 4])))
for(i in 1:length(polys))
polygon(polys[[i]], col = colours[unclass(crime.f[i])])
legend(x = c(6, 7.75), y = c(13.5, 15), legend = levels(crime.f),
fill = colours, cex = 0.7)
title(sub = paste("Columbus OH: residential burglaries and ",
"vehicle\nthefts", "per thousand households, 1980"))
# 2
area1 <- poly2area(polys)
w <- ade4:::area.util.contour(area1)
wxy <- ade4:::area.util.xy(area1)
area.plot(area1, values = columbus$CRIME, sub = paste("Columbus ",
"OH: residential burglaries and vehicle\nthefts", "per thousand households, 1980"))
apply(w, 1, function(x) segments(x[1], x[2], x[3], x[4], lwd = 2))
# 3
data(elec88)
fr.area <- elec88$area
fr.xy <- ade4:::area.util.xy(fr.area)
fr.neig <- elec88$neig # neig(area = fr.area)
# 4
fr.poly <- area2poly(fr.area)
fr.nb <- neig2nb(fr.neig)
maptools:::plot.polylist(fr.poly, attr(fr.poly, "region.rect"), border = "grey")
plot(fr.nb, fr.xy, add = TRUE)
s.label(fr.xy, clab = 0, area = fr.area, neig = fr.neig,
cneig = 1, cpo = 2, inc = FALSE, addax = FALSE)
par(mfrow = c(1, 1))
}
par(mfrow = c(1, 1))
}
## End(Not run)
data(irishdata)
w <- irishdata$area[c(42:53, 18:25), ]
w
w$poly <- as.factor(as.character(w$poly))
area.plot(w, clab = 2)
points(68, 59, pch = 20, col = "red", cex = 3)
points(68, 35, pch = 20, col = "red", cex = 3)
points(45, 12, pch = 20, col = "red", cex = 3)
sqrt((59 - 35) ^ 2) + sqrt((68 - 45) ^ 2 + (35 - 12) ^ 2)
area2link(w)
