library(adegenet)
## Not run:
data(sim2pop)
if(require(spdep)){
cn <- chooseCN(sim2pop@other$xy,ask=FALSE,type=1,plot=FALSE,res="listw")
# global test
Gtest <- global.rtest(sim2pop@tab,cn)
Gtest
# local test
Ltest <- local.rtest(sim2pop@tab,cn)
Ltest
}
## End(Not run)

