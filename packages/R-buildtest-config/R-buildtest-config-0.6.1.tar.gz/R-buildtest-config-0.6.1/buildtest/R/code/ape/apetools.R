library(ape)
## Not run:
x <- Xplorefiles()
x # all data files on your disk
bydir(x) # sorted by directories
bydir(x["fasta"]) # only the FASTA files
Xplorefiles(getwd(), recursive = FALSE) # look only in current dir
## End(Not run)
