library(adephylo)
## Not run:
if(require(ape)){
#### SIMPLE SIMULATED DATA ####
## 50 variables, 2 groups, 30 indiv
dat <- simDatGroups(k=2, p=50, n=c(15,15), mu=c(0,1))
names(dat)
## make a tree
tre <- nj(dist(dat$dat))
plot(tre,type="unr", tip.col=c("blue","red")[as.integer(dat$grp)],
main="simulated data - tree")
## use dibas method
res <- dibas(tre, dat$grp, metric="nNodes")
res
barplot(t(res$prob), main="group membership probabilities")
#### NON-PARAMETRIC TEST BASED ON MEAN SUCCESSFUL ASSIGNMENT ####
## use dibas method
distHo <- replicate(100,
dibas(tre, sample(dat$grp), metric="patristic")$mean.ok)
pval <- mean(res$mean.ok<=c(distHo,res$mean.ok))
pval
hist(c(distHo,res$mean.ok), col="grey",
main="Mean successful assignement - permuted values")
abline(v=res$mean.ok, col="red")
mtext(side=3, text="Observed value in red")
#### HAND FAN SYNDROME ####
## 50 variables, 2 groups, 30 indiv
dat <- simDatGroups(k=2, p=50, n=c(15,15), mu=c(0,1), sigma=c(2,4))
names(dat)
## make a tree
tre <- nj(dist(dat$dat))
plot(tre,type="unr", tip.col=c("blue","red")[as.integer(dat$grp)],
main="simulated data - tree")
mtext(side=3, text="hand-fan syndrome")
## use dibas method
res.patri <- dibas(tre, dat$grp, metric="patristic")
res.patri$grp.tab # poor results
plot(table(res.patri$groups), main="Group assignment - dibas patristic")
res <- dibas(tre, dat$grp, metric="nNodes")
res$grp.tab # results OK
plot(table(res$groups), main="Group assignment - dibas nNodes")
#### MORE COMPLEX DATASET ####
if(require(adegenet)){
dat <- simDatGroups(k=5, p=50, n=c(5,10,10,30,60), mu=sample(1:5, 5,
replace=TRUE), sigma=sample(1:5)/2)
names(dat)
## make a tree
tre <- nj(dist(dat$dat))
plot(tre,type="unr", tip.col=fac2col(dat$grp),main="simulated data - tree")
## use dibas method
res <- dibas(tre, dat$grp, metric="Abouheif")
res
plot(table(res$groups), main="Group assignment - dibas Abouheif")
}
}
## End(Not run)



