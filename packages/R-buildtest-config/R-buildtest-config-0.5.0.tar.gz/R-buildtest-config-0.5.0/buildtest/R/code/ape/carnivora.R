library(ape)
data(carnivora);
# This is figure 1 of Gittleman 1986:
library(lattice)
trellis.device(color=FALSE)
xyplot(BW ~ FW, groups=Family, data=carnivora, auto.key=TRUE, xlog=TRUE,
scale=list(log=TRUE), ylim=c(1, 2000))
trellis.device(color=FALSE)
xyplot(BW ~ FB, groups=Family, data=carnivora, auto.key=TRUE, xlog=TRUE,
scale=list(log=TRUE), ylim=c(1, 2000))
