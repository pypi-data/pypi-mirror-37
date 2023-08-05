library(adegenet)
## Not run:
#### H3N2 ####
## LOAD DATA
data(H3N2)
H3N2
## set population to yearly epidemics
pop(H3N2) <- factor(H3N2$other$epid)
## PERFORM DAPC - USE POPULATIONS AS CLUSTERS
## to reproduce exactly analyses from the paper, use "n.pca=1000"
dapc1 <- dapc(H3N2, all.contrib=TRUE, scale=FALSE, n.pca=150, n.da=5)
dapc1
## (see ?dapc for details about the output)
## SCREEPLOT OF EIGENVALUES
barplot(dapc1$eig, main="H3N2 - DAPC eigenvalues")
## SCATTERPLOT (axes 1-2)
scatter(dapc1, posi.da="topleft", cstar=FALSE, cex=2, pch=17:22,
solid=.5, bg="white")
#### usflu.fasta ####
myPath <- system.file("files/usflu.fasta",package="adegenet")
myPath
## extract SNPs from alignments using fasta2genlight
## see ?fasta2genlight for more details
obj <- fasta2genlight(myPath, chunk=10) # process 10 sequences at a time
obj
## End(Not run)
