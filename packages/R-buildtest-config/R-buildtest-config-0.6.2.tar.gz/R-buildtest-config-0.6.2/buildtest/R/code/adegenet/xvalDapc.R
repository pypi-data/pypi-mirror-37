library(adegenet)
## Not run:
## CROSS-VALIDATION ##
data(sim2pop)
xval <- xvalDapc(sim2pop@tab, pop(sim2pop), n.pca.max=100, n.rep=3)
xval
## 100 replicates ##
# Serial version (SLOW!)
system.time(xval <- xvalDapc(sim2pop@tab, pop(sim2pop), n.pca.max=100, n.rep=100))
# Parallel version (faster!)
system.time(xval <- xvalDapc(sim2pop@tab, pop(sim2pop), n.pca.max=100, n.rep=100,
parallel = "multicore", ncpus = 2))
## End(Not run)
