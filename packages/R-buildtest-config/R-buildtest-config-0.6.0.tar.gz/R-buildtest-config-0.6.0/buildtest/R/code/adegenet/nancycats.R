library(adegenet)
## Not run:
data(nancycats)
nancycats
# summary's results are stored in x
x <- summary(nancycats)
# some useful graphics
barplot(x$loc.n.all,ylab="Alleles numbers",main="Alleles numbers
per locus")
plot(x$pop.eff,x$pop.nall,type="n",xlab="Sample size",ylab="Number of alleles")
text(x$pop.eff,y=x$pop.nall,lab=names(x$pop.nall))
par(las=3)
barplot(table(nancycats@pop),ylab="Number of genotypes",main="Number of genotypes per colony")
# are cats structured among colonies ?
if(require(hierfstat)){
gtest <- gstat.randtest(nancycats,nsim=99)
gtest
plot(gtest)
dat <- genind2hierfstat(nancycats)
Fstat <- varcomp.glob(dat$pop,dat[,-1])
Fstat
}
## End(Not run)
