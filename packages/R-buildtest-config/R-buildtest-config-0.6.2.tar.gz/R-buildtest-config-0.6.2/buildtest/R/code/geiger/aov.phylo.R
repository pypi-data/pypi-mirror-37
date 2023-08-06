library(geiger)
geo=get(data(geospiza))
dat=geo$dat
d1=dat[,1]
grp<-as.factor(c(rep(0, 7), rep(1, 6)))
names(grp)=rownames(dat)
## MANOVA
x=aov.phylo(dat~grp, geo$phy, nsim=50, test="Wilks")
print(attributes(x)$summary) # summary table
## ANOVA
x1=aov.phylo(d1~grp, geo$phy, nsim=50)
