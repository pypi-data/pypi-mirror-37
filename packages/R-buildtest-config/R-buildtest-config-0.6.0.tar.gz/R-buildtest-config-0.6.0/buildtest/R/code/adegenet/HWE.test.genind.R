library(adegenet)
## Not run:
data(nancycats)
obj <- nancycats
if(require(genetics)){
obj.test <- HWE.test(obj)
# pvalues matrix to have a preview
HWE.test(obj,res.type="matrix")
#more precise view to...
obj.test$fca90$P10
}
## End(Not run)
