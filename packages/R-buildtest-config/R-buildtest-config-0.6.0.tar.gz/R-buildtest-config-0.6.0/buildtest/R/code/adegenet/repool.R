library(adegenet)
## Not run:
## use the cattle breeds dataset
data(microbov)
temp <- seppop(microbov)
names(temp)
## hybridize salers and zebu -- nasty cattle
zebler <- hybridize(temp$Salers, temp$Zebu, n=40)
zebler
## now merge zebler with other cattle breeds
nastyCattle <- repool(microbov, zebler)
nastyCattle
## End(Not run)
