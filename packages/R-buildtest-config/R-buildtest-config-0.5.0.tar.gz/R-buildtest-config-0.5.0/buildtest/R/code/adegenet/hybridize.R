library(adegenet)
## Not run:
## Let's make some cattle hybrids
data(microbov)
## first, isolate each breed
temp <- seppop(microbov)
names(temp)
salers <- temp$Salers
zebu <- temp$Zebu
## let's make some... Zeblers
zebler <- hybridize(salers, zebu, n=40,
pop="Zebler")
## now let's merge all data into a single genind
newDat <- repool(microbov, zebler)
## make a correspondance analysis
## and see where hybrids are placed
X <- genind2genpop(newDat, quiet=TRUE)
coa1 <- dudi.coa(tab(X),scannf=FALSE,nf=3)
s.label(coa1$li)
add.scatter.eig(coa1$eig,2,1,2)
## End(Not run)
