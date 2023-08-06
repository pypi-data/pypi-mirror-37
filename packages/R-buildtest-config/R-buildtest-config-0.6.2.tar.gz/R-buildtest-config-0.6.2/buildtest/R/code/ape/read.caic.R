library(ape)
### The same example than in read.tree, without branch lengths.
### An extract from Sibley and Ahlquist (1990)
cat("AAA","Strix_aluco","AAB","Asio_otus",
"AB","Athene_noctua","B","Tyto_alba",
file = "ex.tre", sep = "\n")
tree.owls <- read.caic("ex.tre")
plot(tree.owls)
tree.owls
unlink("ex.tre") # delete the file "ex.tre"

