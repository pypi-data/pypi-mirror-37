library(ade4)
if(!adegraphicsLoaded()) {
if(requireNamespace("pixmap", quietly = TRUE)) {
data(ggtortoises)
a1 <- ggtortoises$area
area.plot(a1)
rect(min(a1$x), min(a1$y), max(a1$x), max(a1$y), col = "lightblue")
invisible(lapply(split(a1, a1$id), function(x) polygon(x[, -1],col = "white")))
s.label(ggtortoises$misc, grid = FALSE, include.ori = FALSE, addaxes = FALSE, add.p = TRUE)
listico <- ggtortoises$ico[as.character(ggtortoises$pop$carap)]
s.logo(ggtortoises$pop, listico, add.p = TRUE)
data(capitales)
index <- pmatch(tolower(attr(capitales$dist, "Labels")), names(capitales$logo))
w1 <- capitales$area
area.plot(w1)
rect(min(w1$x), min(w1$y), max(w1$x), max(w1$y), col = "lightblue")
invisible(lapply(split(w1, w1$id), function(x) polygon(x[, -1],col = "white")))
s.logo(capitales$xy, capitales$logo, klogo = index, add.plot = TRUE, clogo = 1)
# depends on pixmap
}
}
