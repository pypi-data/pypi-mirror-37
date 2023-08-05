library(ade4)
# a 2D spatial orthobasis
w <- gridrowcol(8, 8)
if(adegraphicsLoaded()) {
g1 <- s.value(w$xy, w$orthobasis[, 1:16], pleg.drawKey = FALSE, pgri.text.cex = 0,
ylim = c(0, 10), porigin.include = FALSE, paxes.draw = FALSE)
g2 <- s1d.barchart(attr(w$orthobasis, "values"), p1d.horizontal = FALSE,
labels = names(attr(w$orthobasis, "values")), plabels.cex = 0.7)
} else {
par(mfrow = c(4, 4))
for(k in 1:16)
s.value(w$xy, w$orthobasis[, k], cleg = 0, csi = 2, incl = FALSE,
addax = FALSE, sub = k, csub = 4, ylim = c(0, 10), cgri = 0)
par(mfrow = c(1, 1))
barplot(attr(w$orthobasis, "values"))
}
# Haar 1D orthobasis
w <- orthobasis.haar(32)
par(mfrow = c(8, 4))
par(mar = c(0.1, 0.1, 0.1, 0.1))
for (k in 1:31) {
plot(w[, k], type = "S", xlab = "", ylab = "", xaxt = "n",
yaxt = "n", xaxs = "i", yaxs = "i", ylim = c(-4.5, 4.5))
points(w[, k], type = "p", pch = 20, cex = 1.5)
}
# a 1D orthobasis
w <- orthobasis.line(n = 33)
par(mfrow = c(8, 4))
par(mar = c(0.1, 0.1, 0.1, 0.1))
for (k in 1:32) {
plot(w[, k], type = "l", xlab = "", ylab = "", xaxt = "n",
yaxt = "n", xaxs = "i", yaxs = "i", ylim = c(-1.5, 1.5))
points(w[, k], type = "p", pch = 20, cex = 1.5)
}
if(adegraphicsLoaded()) {
s1d.barchart(attr(w, "values"), p1d.horizontal = FALSE, labels = names(attr(w, "values")),
plab.cex = 0.7)
} else {
par(mfrow = c(1, 1))
barplot(attr(w, "values"))
}
w <- orthobasis.circ(n = 26)
#par(mfrow = c(5, 5))
#par(mar = c(0.1, 0.1, 0.1, 0.1))
# for (k in 1:25)
# dotcircle(w[, k], xlim = c(-1.5, 1.5), cleg = 0)
par(mfrow = c(1, 1))
#barplot(attr(w, "values"))
## Not run:
# a spatial orthobasis
data(mafragh)
w <- orthobasis.neig(mafragh$neig)
if(adegraphicsLoaded()) {
s.value(mafragh$xy, w[, 1:8], plegend.drawKey = FALSE)
s1d.barchart(attr(w, "values"), p1d.horizontal = FALSE)
} else {
par(mfrow = c(4, 2))
for(k in 1:8)
s.value(mafragh$xy, w[, k], cleg = 0, sub = as.character(k), csub = 3)
par(mfrow = c(1, 1))
barplot(attr(w, "values"))
}
# a phylogenetic orthobasis
data(njplot)
phy <- newick2phylog(njplot$tre)
wA <- phy$Ascores
wW <- phy$Wscores
table.phylog(phylog = phy, wA, clabel.row = 0, clabel.col = 0.5)
table.phylog(phylog = phy, wW, clabel.row = 0, clabel.col = 0.5)
## End(Not run)
