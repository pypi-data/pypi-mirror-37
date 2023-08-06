library(adegenet)
obj1 <- import2genind(system.file("files/nancycats.gen",
package="adegenet"))
obj1
obj2 <- genind2genpop(obj1)
obj2
## Not run:
data(microsatt)
# use as.genpop to convert convenient count tab to genpop
obj3 <- as.genpop(microsatt$tab)
obj3
all(obj3@tab==microsatt$tab)
# perform a correspondance analysis
obj4 <- genind2genpop(obj1,missing="chi2")
ca1 <- dudi.coa(as.data.frame(obj4@tab),scannf=FALSE)
s.label(ca1$li,sub="Correspondance Analysis",csub=2)
add.scatter.eig(ca1$eig,2,xax=1,yax=2,posi="top")
## End(Not run)
