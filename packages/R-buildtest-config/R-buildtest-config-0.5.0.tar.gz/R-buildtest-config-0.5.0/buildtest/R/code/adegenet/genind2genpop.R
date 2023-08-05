library(adegenet)
## simple conversion
data(nancycats)
nancycats
catpop <- genind2genpop(nancycats)
catpop
summary(catpop)
## processing the @other slot
data(sim2pop)
sim2pop$other$foo <- letters
sim2pop
dim(sim2pop$other$xy) # matches the number of genotypes
sim2pop$other$foo # does not match the number of genotypes
obj <- genind2genpop(sim2pop, process.other=TRUE)
obj$other # the new xy is the populations' centre
pch <- as.numeric(pop(sim2pop))
col <- pop(sim2pop)
levels(col) <- c("blue","red")
col <- as.character(col)
plot(sim2pop$other$xy, pch=pch, col=col)
text(obj$other$xy, lab=row.names(obj$other$xy), col=c("blue","red"), cex=2, font=2)
## Not run:
data(microbov)
strata(microbov) <- data.frame(other(microbov))
summary(genind2genpop(microbov)) # Conversion based on population factor
summary(genind2genpop(microbov, ~coun)) # Conversion based on country
summary(genind2genpop(microbov, ~coun/spe)) # Conversion based on country and species
## End(Not run)

