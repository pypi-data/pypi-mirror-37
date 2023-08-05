library(akima)
data(akima)
# linear interpolation at points (1,2), (5,6) and (10,12)
akima.lip<-interpp(akima$x, akima$y, akima$z,c(1,5,10),c(2,6,12))
akima.lip$z
# spline interpolation
akima.sip<-interpp(akima$x, akima$y, akima$z,c(1,5,10),c(2,6,12),
linear=FALSE)
akima.sip$z
## Not run:
## interaction with sp objects:
library(sp)
## take 30 sample points out of meuse grid:
data(meuse.grid)
m0 <- meuse.grid[sample(1:3103,30),]
coordinates(m0) <- ~x+y
## interpolate on this 30 points:
## note: both "meuse" and "m0" are sp objects
## (SpatialPointsDataFrame) !!
## arguments z and xo have to named, y has to be omitted!
ipp <- interpp(meuse,z="zinc",xo=m0)
spplot(ipp)
## End(Not run)
