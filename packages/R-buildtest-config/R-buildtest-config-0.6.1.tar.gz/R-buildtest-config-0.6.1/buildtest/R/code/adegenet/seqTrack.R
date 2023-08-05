library(adegenet)
## Not run:
if(require(ape && require(igraph))){
## ANALYSIS OF SIMULATED DATA ##
## SIMULATE A GENEALOGY
dat <- haploGen(seq.l=1e4, repro=function(){sample(1:4,1)}, gen.time=1, t.max=3)
plot(dat, main="Simulated data")
## SEQTRACK ANALYSIS
res <- seqTrack(dat, mu=0.0001, haplo.length=1e4)
plot(res, main="seqTrack reconstruction")
## PROPORTION OF CORRECT RECONSTRUCTION
mean(dat$ances==res$ances,na.rm=TRUE)
## ANALYSIS OF PANDEMIC A/H1N1 INFLUENZA DATA ##
## note:
## this is for reproduction purpose only
## seqTrack is best kept for the analysis
## of densely sampled outbreaks, which
## is not the case of this dataset.
##
dat <- read.csv(system.file("files/pdH1N1-data.csv",package="adegenet"))
ha <- read.dna(system.file("files/pdH1N1-HA.fasta",package="adegenet"), format="fa")
na <- read.dna(system.file("files/pdH1N1-NA.fasta",package="adegenet"), format="fa")
## COMPUTE NUCLEOTIDIC DISTANCES
nbNucl <- ncol(as.matrix(ha)) + ncol(as.matrix(na))
D <- dist.dna(ha,model="raw")*ncol(as.matrix(ha)) +
dist.dna(na,model="raw")*ncol(as.matrix(na))
D <- round(as.matrix(D))
## MATRIX OF SPATIAL CONNECTIVITY
## (to promote local transmissions)
xy <- cbind(dat$lon, dat$lat)
temp <- as.matrix(dist(xy))
M <- 1* (temp < 1e-10)
## SEQTRACK ANALYSIS
dat$date <- as.POSIXct(dat$date)
res <- seqTrack(D, rownames(dat), dat$date, prox.mat=M, mu=.00502/365, haplo.le=nbNucl)
## COMPUTE GENETIC LIKELIHOOD
p <- get.likelihood(res, mu=.00502/365, haplo.length=nbNucl)
# (these could be shown as colors when plotting results)
# (but mutations will be used instead)
## EXAMINE RESULTS
head(res)
tail(res)
range(res$weight, na.rm=TRUE)
barplot(table(res$weight)/sum(!is.na(res$weight)), ylab="Frequency",
xlab="Mutations between inferred ancestor and descendent", col="orange")
## DISPLAY SPATIO-TEMPORAL DYNAMICS
if(require(maps)){
myDates <- as.integer(difftime(dat$date, as.POSIXct("2009-01-21"), unit="day"))
myMonth <- as.POSIXct(
c("2009-02-01", "2009-03-01","2009-04-01","2009-05-01","2009-06-01","2009-07-01"))
x.month <- as.integer(difftime(myMonth, as.POSIXct("2009-01-21"), unit="day"))
## FIRST STAGE:
## SPREAD TO THE USA AND CANADA
curRange <- as.POSIXct(c("2009-03-29","2009-04-25"))
par(bg="deepskyblue")
map("world", fill=TRUE, col="grey")
opal <- palette()
palette(rev(heat.colors(10)))
plotSeqTrack(res, round(xy), add=TRUE,annot=FALSE,lwd=2,date.range=curRange,
col=res$weight+1)
title(paste(curRange, collapse=" to "))
legend("bottom", lty=1, leg=0:8, title="number of mutations", col=1:9,
lwd=2, horiz=TRUE)
## SECOND STAGE:
## SPREAD WITHIN AMERICA, FIRST SEEDING OUTSIDE AMERICA
curRange <- as.POSIXct(c("2009-04-30","2009-05-07"))
par(bg="deepskyblue")
map("world", fill=TRUE, col="grey")
opal <- palette()
palette(rev(heat.colors(10)))
plotSeqTrack(res, round(xy), add=TRUE,annot=FALSE,lwd=2,
date.range=curRange, col=res$weight+1)
title(paste(curRange, collapse=" to "))
legend("bottom", lty=1, leg=0:8, title="number of mutations",
col=1:9,lwd=2, horiz=TRUE)
## THIRD STAGE:
## PANDEMIC
curRange <- as.POSIXct(c("2009-05-15","2009-05-25"))
par(bg="deepskyblue")
map("world", fill=TRUE, col="grey")
opal <- palette()
palette(rev(heat.colors(10)))
plotSeqTrack(res, round(xy), add=TRUE,annot=FALSE,lwd=2, date.range=curRange,
col=res$weight+1)
title(paste(curRange, collapse=" to "))
legend("bottom", lty=1, leg=0:8, title="number of mutations",
col=1:9,lwd=2, horiz=TRUE)
}
}
## End(Not run)

