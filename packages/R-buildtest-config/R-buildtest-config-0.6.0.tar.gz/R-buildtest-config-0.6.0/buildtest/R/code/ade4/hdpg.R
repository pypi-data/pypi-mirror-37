library(ade4)
## Not run:
data(hdpg)
freq <- char2genet(hdpg$tab, hdpg$ind$population)
vec <- apply(freq$tab, 2, function(c) mean(c, na.rm = TRUE))
for (j in 1:4492){
freq$tab[is.na(freq$tab[,j]),j] = vec[j]}
pcatot <- dudi.pca(freq$tab, center = TRUE, scale = FALSE, scannf = FALSE, nf = 4)
if(adegraphicsLoaded()) {
s.label(pcatot$li, xax = 1, yax = 2, psub.text = "1-2", lab = freq$pop.names)
} else {
s.label(pcatot$li, xax = 1, yax = 2, sub = "1-2", lab = freq$pop.names)
}
## End(Not run)

