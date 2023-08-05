library(ape)
data(woodmouse)
alview(woodmouse[, 1:50])
alview(woodmouse[, 1:50], uppercase = FALSE)
## Not run:
alview(woodmouse, file = "woodmouse.txt")
## End(Not run)
