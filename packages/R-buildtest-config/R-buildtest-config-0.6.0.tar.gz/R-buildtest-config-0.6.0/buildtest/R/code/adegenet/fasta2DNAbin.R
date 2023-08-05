library(adegenet)
## Not run:
## show the example file ##
## this is the path to the file:
myPath <- system.file("files/usflu.fasta",package="adegenet")
myPath
## read the file
obj <- fasta2DNAbin(myPath, chunk=10) # process 10 sequences at a time
obj
## End(Not run)
