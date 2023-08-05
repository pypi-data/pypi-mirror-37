library(adegenet)
## Not run:
data(woodmouse)
## mutations between first 3 sequences
findMutations(woodmouse[1:3,])
## mutations from the first to sequences 2 and 3
findMutations(woodmouse[1:3,], from=1)
## same, graphical display
g <- graphMutations(woodmouse[1:3,], from=1)
## some manual checks
as.character(woodmouse)[1:3,35]
as.character(woodmouse)[1:3,36]
as.character(woodmouse)[1:3,106]
## End(Not run)

