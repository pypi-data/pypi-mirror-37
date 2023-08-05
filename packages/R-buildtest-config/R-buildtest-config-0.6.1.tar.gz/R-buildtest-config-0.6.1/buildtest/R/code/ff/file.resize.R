library(ff)
x <- tempfile()
newsize <- 23 # resize and size to 23 bytes.
file.resize(x, newsize)
file.info(x)$size == newsize
## Not run:
newsize <- 8*(2^30) # create new file and size to 8 GB.
file.resize(x, newsize)
file.info(x)$size == newsize
## End(Not run)
y <- tempfile()
file.move(x,y)
file.remove(y)
