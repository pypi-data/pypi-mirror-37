library(ape)
data(woodmouse)
x <- as.character(woodmouse)
x[, 1:20]
str(as.alignment(x))
identical(as.DNAbin(x), woodmouse)
### conversion from BioConductor:
## Not run:
if (require(Biostrings)) {
data(phiX174Phage)
X <- as.DNAbin(phiX174Phage)
## base frequencies:
base.freq(X) # from ape
alphabetFrequency(phiX174Phage) # from Biostrings
### for objects of class "DNAStringSetList"
X <- lapply(x, as.DNAbin) # a list of lists
### to put all sequences in a single list:
X <- unlist(X, recursive = FALSE)
class(X) <- "DNAbin"
}
## End(Not run)
