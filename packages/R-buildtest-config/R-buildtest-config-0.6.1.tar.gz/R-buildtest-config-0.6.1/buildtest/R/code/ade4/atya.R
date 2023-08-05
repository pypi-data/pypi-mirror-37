library(ade4)
## Not run:
data(atya)
if(requireNamespace("pixmap", quietly = TRUE)) {
atya.digi <- pixmap::read.pnm(system.file("pictures/atyadigi.pnm",
package = "ade4"))
atya.carto <- pixmap::read.pnm(system.file("pictures/atyacarto.pnm",
package = "ade4"))
par(mfrow = c(1, 2))
pixmap:::plot(atya.digi)
pixmap:::plot(atya.carto)
points(atya$xy, pch = 20, cex = 2)
}
if(requireNamespace("maptools", quietly = TRUE) & requireNamespace("spdep", quietly = TRUE)) {
plot(neig2nb(atya$neig), atya$xy, col = "red", add = TRUE, lwd = 2)
par(mfrow = c(1,1))
}
## End(Not run)

