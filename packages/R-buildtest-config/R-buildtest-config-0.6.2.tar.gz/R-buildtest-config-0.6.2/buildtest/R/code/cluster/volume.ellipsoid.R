library(cluster)
## example(ellipsoidhull) # which defines `ellipsoid' object <namefoo>
myEl <- structure(list(cov = rbind(c(3,1),1:2), loc = c(0,0), d2 = 10),
class = "ellipsoid")
volume(myEl)# i.e. "area" here (d = 2)
myEl # also mentions the "volume"

