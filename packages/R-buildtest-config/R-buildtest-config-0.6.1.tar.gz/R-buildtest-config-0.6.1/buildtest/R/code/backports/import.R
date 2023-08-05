library(backports)
## Not run:
# This imports all functions implemented in backports while the package is loaded
.onLoad <- function(libname, pkgname) {
backports::import(pkgname)
}
# This only imports the function "trimws"
.onLoad <- function(libname, pkgname) {
backports::import(pkgname, "trimws")
}
## End(Not run)
