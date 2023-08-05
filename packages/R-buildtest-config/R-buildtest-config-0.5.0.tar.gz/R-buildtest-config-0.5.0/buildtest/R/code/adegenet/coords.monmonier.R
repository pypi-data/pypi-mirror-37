library(adegenet)
## Not run:
if(require(spdep)){
load(system.file("files/mondata1.rda",package="adegenet"))
cn1 <- chooseCN(mondata1$xy,type=2,ask=FALSE)
mon1 <- monmonier(mondata1$xy,dist(mondata1$x1),cn1,threshold=2,nrun=3)
mon1$run1
mon1$run2
mon1$run3
path.coords <- coords.monmonier(mon1)
path.coords
}
## End(Not run)
