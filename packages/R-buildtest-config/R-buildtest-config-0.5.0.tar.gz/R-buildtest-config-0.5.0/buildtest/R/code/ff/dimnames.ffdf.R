library(ff)
ffd <- as.ffdf(data.frame(a=1:26, b=letters))
dimnames(ffd)
row.names(ffd) <- letters
dimnames(ffd)
ffd
rm(ffd); gc()
