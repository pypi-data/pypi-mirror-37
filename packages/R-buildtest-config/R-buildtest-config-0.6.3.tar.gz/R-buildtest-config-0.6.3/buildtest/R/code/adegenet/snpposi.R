library(adegenet)
if(require(ape)){
data(woodmouse)
snpposi.plot(woodmouse, codon=FALSE)
snpposi.plot(woodmouse)
## Not run:
snpposi.test(c(1,3,4,5), 100)
snpposi.test(woodmouse)
## End(Not run)
}
