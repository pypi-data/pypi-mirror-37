library(adegenet)
## Not run:
## simulate data
x <- glSim(100, 1e3, n.snp.struc=100, ploid=2)
## default plot
glPlot(x)
plot(x) # identical plot
## disable legend
plot(x, leg=FALSE)
## use other colors
plot(x, col=heat.colors(3), bg="white")
## End(Not run)

