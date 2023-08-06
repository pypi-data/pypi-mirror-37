library(akima)
data(akima)
plot(y ~ x, data = akima, main = "akima example data")
with(akima, text(x, y, formatC(z,dig=2), adj = -0.1))
## linear interpolation
akima.li <- interp(akima$x, akima$y, akima$z)
li.zmin <- min(akima.li$z,na.rm=TRUE)
li.zmax <- max(akima.li$z,na.rm=TRUE)
breaks <- pretty(c(li.zmin,li.zmax),10)
colors <- heat.colors(length(breaks)-1)
with(akima.li, image (x,y,z, breaks=breaks, col=colors))
with(akima.li,contour(x,y,z, levels=breaks, add=TRUE))
points (akima, pch = 3)
## increase smoothness (using finer grid):
akima.smooth <-
with(akima, interp(x, y, z, nx=100, ny=100))
si.zmin <- min(akima.smooth$z,na.rm=TRUE)
si.zmax <- max(akima.smooth$z,na.rm=TRUE)
breaks <- pretty(c(si.zmin,si.zmax),10)
colors <- heat.colors(length(breaks)-1)
image (akima.smooth, main = "interp(<akima data>, *) on finer grid",
breaks=breaks, col=colors)
contour(akima.smooth, add = TRUE, levels=breaks, col = "thistle")
points(akima, pch = 3, cex = 2, col = "blue")
## use triangulation package to show underlying triangulation:
## Not run:
if(library(tripack, logical.return=TRUE))
plot(tri.mesh(akima), add=TRUE, lty="dashed")
## End(Not run)
## use only 15 points (interpolation only within convex hull!)
akima.part <- with(akima, interp(x[1:15], y[1:15], z[1:15]))
p.zmin <- min(akima.part$z,na.rm=TRUE)
p.zmax <- max(akima.part$z,na.rm=TRUE)
breaks <- pretty(c(p.zmin,p.zmax),10)
colors <- heat.colors(length(breaks)-1)
image(akima.part, breaks=breaks, col=colors)
title("interp() on subset of only 15 points")
contour(akima.part, levels=breaks, add=TRUE)
points(akima$x[1:15],akima$y[1:15], col = "blue")
## spline interpolation
akima.spl <- with(akima, interp(x, y, z, nx=100, ny=100, linear=FALSE))
contour(akima.spl, main = "smooth interp(*, linear = FALSE)")
points(akima)
full.pal <- function(n) hcl(h = seq(340, 20, length = n))
cool.pal <- function(n) hcl(h = seq(120, 0, length = n) + 150)
warm.pal <- function(n) hcl(h = seq(120, 0, length = n) - 30)
filled.contour(akima.spl, color.palette = full.pal,
plot.axes = { axis(1); axis(2);
title("smooth interp(*, linear = FALSE)");
points(akima, pch = 3, col= hcl(c=100, l = 20))})
## no extrapolation!
## Not run:
## interp can handle spatial point dataframes created by the sp package:
library(sp)
data(meuse)
coordinates(meuse) <- ~x+y
## argument z has to be named, y has to be omitted!
z <- interp(meuse,z="zinc",nx=100,ny=150)
spplot(z,"zinc")
z <- interp(meuse,z="zinc",nx=100,ny=150,linear=FALSE)
spplot(z,"zinc")
## End(Not run)
## Not run:
### An example demonstrating the problems that occur for rectangular
### gridded data.
###
require(tripack)
### Create irregularly spaced sample data on even values of x and y
### (the "14" makes it irregular spacing).
x <- c(seq(2,10,2),14)
nx <- length(x)
y <- c(seq(2,10,2),14)
ny <- length(y)
nxy <- nx*ny
xy <- expand.grid(x,y)
colnames(xy) <- c("x","y")
### prepare a dataframe for interp
df <- cbind(xy,z=rnorm(nxy))
### and a matrix for bicubic and bilinear
z <- matrix(df$z,nx,ny)
old.par <- par(mfrow=c(2,2))
### First: bicubic spline interpolation:
### This is Akimas bicubic spline implementation for regular gridded
### data:
iRbic <- bicubic.grid(x,y,z,nx=250,ny=250)
### Note that this interpolation tends to extreme values in large cells.
### Therefore zmin and zmax are taken from here to generate the same
### color scheme for the next plots.
zmin <- min(iRbic$z, na.rm=TRUE)
zmax <- max(iRbic$z, na.rm=TRUE)
breaks <- pretty(c(zmin,zmax),10)
colors <- heat.colors(length(breaks)-1)
image(iRbic,breaks=breaks,col = colors)
contour(iRbic,col="black",levels=breaks,add=TRUE)
points(xy$x,xy$y)
title(main="bicubic interpolation",
xlab="bcubic.grid(...)",
sub="Akimas regular grid version, ACM 760")
### Now Akima splines with accurracy of bicubic polynomial
### for irregular gridded data:
iRspl <- with(df,interp(x,y,z,linear=FALSE,nx=250,ny=250))
### Note that the triangulation is created by adding small amounts
### of jitter to the coordinates, resulting in an unique triangulation.
### This jitter is not randomly choosen to get reproducable results.
### tri.mesh() from package tripack uses the same code and so produces the
### same triangulation.
image(iRspl,breaks=breaks,col = colors)
contour(iRspl,col="black",levels=breaks,add=TRUE)
plot(tri.mesh(xy$x,xy$y),col="white",add=TRUE)
title(main="bicubic* interpolation",
xlab="interp(...,linear=FALSE)",
ylab="*: accuracy of bicubic polynomial"
sub="Akimas irregular grid version, ACM 761")
### Just for comparison an implementation of bilinear interpolation,
### only applicable to regular gridded data:
iRbil <- bilinear.grid(x,y,z,nx=250,ny=250)
### Note the lack of differentiability at grid cell borders.
image(iRbil,breaks=breaks,col = colors)
contour(iRbil,col="black",levels=breaks,add=TRUE)
points(xy$x,xy$y)
title(main="bilinear interpolation",
xlab="bilinear.grid(...)",
sub="only works for regular grid")
### Linear interpolation using the same triangulation as
### Akima bicubic splines for irregular gridded data.
iRlin <- with(df,interp(x,y,z,linear=TRUE,nx=250,ny=250))
### Note how the triangulation influences the interpolation.
### For this rectangular gridded dataset the triangulation
### in each rectangle is arbitraryly choosen from two possible
### solutions, hence the interpolation would change drastically
### when the triangulation changes. For this reason interp()
### is not meant for regular (rectangular) gridded data!
image(iRlin,breaks=breaks,col = colors)
contour(iRlin,col="black",levels=breaks,add=TRUE)
plot(tri.mesh(xy$x,xy$y),col="white",add=TRUE)
title(main="linear interpolation",
xlab="interp(...,linear=TRUE)",
sub="same triangulation as Akima irregular grid")
### And now four times Akima 761 with random jitter for
### triangulation correction, note that now interp() and tri.mesh()
### need the same random seed to produce identical triangulations!
for(i in 1:4){
set.seed(42+i)
iRspl <- with(df,interp(x,y,z,linear=FALSE,nx=250,ny=250,jitter.random=TRUE))
image(iRspl,breaks=breaks,col = colors)
contour(iRspl,col="black",levels=breaks,add=TRUE)
set.seed(42+i)
plot(tri.mesh(xy$x,xy$y,jitter.random=TRUE),col="white",add=TRUE)
title(main="bicubic* interpolation",
xlab="interp(...,linear=FALSE)",
ylab="random jitter added",
sub="Akimas irregular grid version, ACM 761")
}
par(old.par)
## End(Not run)
### Use all datasets from Franke, 1979:
data(franke)
for(i in 1:5)
for(j in 1:3){
FR <- franke.data(i,j,franke)
IL <- with(FR, interp(x,y,z,linear=FALSE))
image(IL)
contour(IL,add=TRUE)
with(FR,points(x,y))
}
