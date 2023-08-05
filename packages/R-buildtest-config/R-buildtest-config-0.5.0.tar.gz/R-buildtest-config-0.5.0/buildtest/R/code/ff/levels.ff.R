library(ff)
message("--- create an ff factor including NA as last level")
x <- ff("a", levels=c(letters, NA), length=99)
message(' we expect a warning because "A" is an unknown level')
x[] <- c("a", NA,"A")
x
levels(x)
message("--- create an ff ordered factor")
x <- ff(letters, levels=letters, ramclass=c("ordered","factor"), length=260)
x
levels(x)
message(" make it a non-ordered factor")
virtual(x)$ramclass <- "factor"
x
rm(x); gc()
## Not run:
message("--- create an unsigned quad factor")
x <- ff(c("A","T","G","C"), levels=c("A","T","G","C"), vmode="quad", length=100)
x
message(" 0:3 coding usually invisible to the user")
unclass(x[1:4])
message(" after removing levels, the 0:3 coding becomes visible to the user")
message(" we expect a warning here")
levels(x) <- NULL
x[1:4]
rm(x); gc()
## End(Not run)
