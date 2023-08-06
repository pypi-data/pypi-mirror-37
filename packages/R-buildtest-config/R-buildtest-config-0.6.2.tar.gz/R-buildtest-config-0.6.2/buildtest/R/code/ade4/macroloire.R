library(ade4)
data(macroloire)
apqe.Equi <- apqe(macroloire$fau, , macroloire$morphoregions)
apqe.Equi
#test.Equi <- randtest.apqe(apqe.Equi, method = "aggregated", 99)
#plot(test.Equi)
## Not run:
m.phy <- taxo2phylog(macroloire$taxo)
apqe.Tax <- apqe(macroloire$fau, m.phy$Wdist, macroloire$morphoregions)
apqe.Tax
#test.Tax <- randtest.apqe(apqe.Tax, method = "aggregated", 99)
#plot(test.Tax)
dSize <- sqrt(dist.prop(macroloire$traits[ ,1:4], method = 2))
apqe.Size <- apqe(macroloire$fau, dSize, macroloire$morphoregions)
apqe.Size
#test.Size <- randtest.apqe(apqe.Size, method = "aggregated", 99)
#plot(test.Size)
dFeed <- sqrt(dist.prop(macroloire$traits[ ,-(1:4)], method = 2))
apqe.Feed <- apqe(macroloire$fau, dFeed, macroloire$morphoregions)
apqe.Feed
#test.Feed <- randtest.apqe(apqe.Feed, method = "aggregated", 99)
#plot(test.Size)
## End(Not run)

