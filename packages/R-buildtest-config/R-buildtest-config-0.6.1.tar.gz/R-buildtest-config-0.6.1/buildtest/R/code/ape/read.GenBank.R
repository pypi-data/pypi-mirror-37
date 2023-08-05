library(ape)
## This won't work if your computer is not connected
## to the Internet
## Get the 8 sequences of tanagers (Ramphocelus)
## as used in Paradis (1997)
ref <- c("U15717", "U15718", "U15719", "U15720",
"U15721", "U15722", "U15723", "U15724")
## Copy/paste or type the following commands if you
## want to try them.
## Not run:
Rampho <- read.GenBank(ref)
## get the species names:
attr(Rampho, "species")
## build a matrix with the species names and the accession numbers:
cbind(attr(Rampho, "species"), names(Rampho))
## print the first sequence
## (can be done with `Rampho$U15717' as well)
Rampho[[1]]
## the description from each FASTA sequence:
attr(Rampho, "description")
## End(Not run)

