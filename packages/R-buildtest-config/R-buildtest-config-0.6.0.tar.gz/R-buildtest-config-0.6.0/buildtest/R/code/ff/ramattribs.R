library(ff)
x <- ff(as.POSIXct(as.POSIXlt(Sys.time(), "GMT")), length=12)
x
ramclass(x)
ramattribs(x)
class(x[])
attributes(x[])
virtual(x)$ramattribs$tzone = NULL
attributes(x[])
rm(x); gc()
