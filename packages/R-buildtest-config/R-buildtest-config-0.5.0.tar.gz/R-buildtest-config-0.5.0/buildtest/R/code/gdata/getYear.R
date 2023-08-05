library(gdata)
## --- Date class ---
tmp <- Sys.Date()
tmp
getYear(tmp)
getMonth(tmp)
getDay(tmp)
## --- POSIXct class ---
tmp <- as.POSIXct(tmp)
getYear(tmp)
getMonth(tmp)
getDay(tmp)
## --- POSIXlt class ---
tmp <- as.POSIXlt(tmp)
getYear(tmp)
getMonth(tmp)
getDay(tmp)
