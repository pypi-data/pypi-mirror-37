library(ape)
data(woodmouse)
X <- trans(woodmouse) # not correct
X2 <- trans(woodmouse, 2) # using the correct code
identical(X, X2)
alview(X[1:2, 1:60]) # some codon Stop (*)
alview(X2[, 1:60])
X2
