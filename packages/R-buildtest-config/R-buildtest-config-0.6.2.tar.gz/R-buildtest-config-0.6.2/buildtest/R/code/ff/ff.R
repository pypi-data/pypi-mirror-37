library(ff)
message("make sure you understand the following ff options
before you start using the ff package!!")
oldoptions <- options(fffinalizer="deleteIfOpen", fffinonexit="TRUE", fftempdir=tempdir())
message("an integer vector")
ff(1:12)
message("a double vector of length 12")
ff(0, 12)
message("a 2-bit logical vector of length 12 (vmode='boolean' has 1 bit)")
ff(vmode="logical", length=12)
message("an integer matrix 3x4 (standard colwise physical layout)")
ff(1:12, dim=c(3,4))
message("an integer matrix 3x4 (rowwise physical layout, but filled in standard colwise order)")
ff(1:12, dim=c(3,4), dimorder=c(2,1))
message("an integer matrix 3x4 (standard colwise physical layout, but filled in rowwise order
aka matrix(, byrow=TRUE))")
ff(1:12, dim=c(3,4), bydim=c(2,1))
gc()
options(oldoptions)
if (ffxtensions()){
message("a 26-dimensional boolean array using 1-bit representation
(file size 8 MB compared to 256 MB int in ram)")
a <- ff(vmode="boolean", dim=rep(2, 26))
dimnames(a) <- dummy.dimnames(a)
rm(a); gc()
}
## Not run:
message("This 2GB biglm example can take long, you might want to change
the size in order to define a size appropriate for your computer")
require(biglm)
b <- 1000
n <- 100000
k <- 3
memory.size(max = TRUE)
system.time(
x <- ff(vmode="double", dim=c(b*n,k), dimnames=list(NULL, LETTERS[1:k]))
)
memory.size(max = TRUE)
system.time(
ffrowapply({
l <- i2 - i1 + 1
z <- rnorm(l)
x[i1:i2,] <- z + matrix(rnorm(l*k), l, k)
}, X=x, VERBOSE=TRUE, BATCHSIZE=n)
)
memory.size(max = TRUE)
form <- A ~ B + C
first <- TRUE
system.time(
ffrowapply({
if (first){
first <- FALSE
fit <- biglm(form, as.data.frame(x[i1:i2,,drop=FALSE]))
}else
fit <- update(fit, as.data.frame(x[i1:i2,,drop=FALSE]))
}, X=x, VERBOSE=TRUE, BATCHSIZE=n)
)
memory.size(max = TRUE)
first
fit
summary(fit)
rm(x); gc()
## End(Not run)
