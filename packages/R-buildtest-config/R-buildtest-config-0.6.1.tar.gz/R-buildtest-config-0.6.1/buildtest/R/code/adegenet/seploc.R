library(adegenet)
## Not run:
## example on genind objects
data(microbov)
# separate all markers
obj <- seploc(microbov)
names(obj)
obj$INRA5
## example on genlight objects
x <- glSim(100, 1000, 0, ploidy=2) # simulate data
x <- x[,order(glSum(x))] # reorder loci by frequency of 2nd allele
glPlot(x, main="All data") # plot data
foo <- seploc(x, n.block=3) # form 3 blocks
foo
glPlot(foo[[1]], main="1st block") # plot 1st block
glPlot(foo[[2]], main="2nd block") # plot 2nd block
glPlot(foo[[3]], main="3rd block") # plot 3rd block
foo <- seploc(x, block.size=600, random=TRUE) # split data, randomize loci
foo # note the different block sizes
glPlot(foo[[1]])
## End(Not run)
