library(ape)
## Not run:
tr <- rcoal(1000)
plot(tr, show.tip.label = FALSE)
trex(tr) # left-click as many times as you want, then right-click
tr <- makeNodeLabel(tr)
trex(tr, subbg = "lightgreen") # id.
## generate a random colour with control on the darkness:
rRGB <- function(a, b)
rgb(runif(1, a, b), runif(1, a, b), runif(1, a, b))
### with a random pale background:
trex(tr, subbg = rRGB(0.8, 1))
## the above can be called many times...
graphics.off() # close all graphical devices
## End(Not run)
