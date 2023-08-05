library(ff)
x <- data.frame(log=rep(c(FALSE, TRUE), length.out=26), int=1:26, dbl=1:26 + 0.1
, fac=factor(letters), ord=ordered(LETTERS), dct=Sys.time()+1:26
, dat=seq(as.Date("1910/1/1"), length.out=26, by=1))
ffx <- as.ffdf(x)
csvfile <- tempPathFile(path=getOption("fftempdir"), extension="csv")
write.csv.ffdf(ffx, file=csvfile)
write.csv.ffdf(ffx, file=csvfile, append=TRUE)
ffy <- read.csv.ffdf(file=csvfile, header=TRUE
, colClasses=c(ord="ordered", dct="POSIXct", dat="Date"))
rm(ffx, ffy); gc()
unlink(csvfile)
## Not run:
# Attention, this takes very long
vmodes <- c(log="boolean", int="byte", dbl="single"
, fac="short", ord="short", dct="single", dat="single")
message("create a ffdf with 7 columns and 78 mio rows")
system.time({
x <- data.frame(log=rep(c(FALSE, TRUE), length.out=26), int=1:26, dbl=1:26 + 0.1
, fac=factor(letters), ord=ordered(LETTERS), dct=Sys.time()+1:26
, dat=seq(as.Date("1910/1/1"), length.out=26, by=1))
x <- do.call("rbind", rep(list(x), 10))
x <- do.call("rbind", rep(list(x), 10))
x <- do.call("rbind", rep(list(x), 10))
x <- do.call("rbind", rep(list(x), 10))
ffx <- as.ffdf(x, vmode = vmodes)
for (i in 2:300){
message(i, "\n")
last <- nrow(ffx) + nrow(x)
first <- last - nrow(x) + 1L
nrow(ffx) <- last
ffx[first:last,] <- x
}
})
csvfile <- tempPathFile(path=getOption("fftempdir"), extension="csv")
write.csv.ffdf(ffx, file=csvfile, VERBOSE=TRUE)
ffy <- read.csv.ffdf(file=csvfile, header=TRUE
, colClasses=c(ord="ordered", dct="POSIXct", dat="Date")
, asffdf_args=list(vmode = vmodes), VERBOSE=TRUE)
rm(ffx, ffy); gc()
unlink(csvfile)
## End(Not run)
