library(tm)
data("crude")
writeCorpus(crude, path = ".",
filenames = paste(seq_along(crude), ".txt", sep = ""))
## End(Not run)

