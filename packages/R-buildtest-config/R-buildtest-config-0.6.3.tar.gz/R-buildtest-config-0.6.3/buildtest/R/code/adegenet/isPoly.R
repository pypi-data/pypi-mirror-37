library(adegenet)
## Not run:
data(nancycats)
isPoly(nancycats,by="loc", thres=0.1)
isPoly(nancycats[1:3],by="loc", thres=0.1)
genind2df(nancycats[1:3])
## End(Not run)
