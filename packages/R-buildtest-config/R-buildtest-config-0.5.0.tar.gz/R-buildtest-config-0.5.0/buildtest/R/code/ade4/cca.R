library(ade4)
data(rpjdl)
millog <- log(rpjdl$mil + 1)
iv1 <- cca(rpjdl$fau, millog, scan = FALSE)
if(adegraphicsLoaded()) {
G1 <- plot(iv1)
# analysis with c1 - as - li -ls
# projections of inertia axes on PCAIV axes
G2 <- s.corcircle(iv1$as)
# Species positions
g31 <- s.label(iv1$c1, xax = 2, yax = 1, plab.cex = 0.5, xlim = c(-4, 4), plot = FALSE)
# Sites positions at the weighted mean of present species
g32 <- s.label(iv1$ls, xax = 2, yax = 1, plab.cex = 0, plot = FALSE)
G3 <- superpose(g31, g32, plot = TRUE)
# Prediction of the positions by regression on environmental variables
G4 <- s.match(iv1$ls, iv1$li, xax = 2, yax = 1, plab.cex = 0.5)
# analysis with fa - l1 - co -cor
# canonical weights giving unit variance combinations
G5 <- s.arrow(iv1$fa)
# sites position by environmental variables combinations
# position of species by averaging
g61 <- s.label(iv1$l1, xax = 2, yax = 1, plab.cex = 0, ppoi.cex = 1.5, plot = FALSE)
g62 <- s.label(iv1$co, xax = 2, yax = 1, plot = FALSE)
G6 <- superpose(g61, g62, plot = TRUE)
G7 <- s.distri(iv1$l1, rpjdl$fau, xax = 2, yax = 1, ellipseSize = 0, starSize = 0.33)
# coherence between weights and correlations
g81 <- s.corcircle(iv1$cor, xax = 2, yax = 1, plot = FALSE)
g82 <- s.arrow(iv1$fa, xax = 2, yax = 1, plot = FALSE)
G8 <- cbindADEg(g81, g82, plot = TRUE)
} else {
plot(iv1)
# analysis with c1 - as - li -ls
# projections of inertia axes on PCAIV axes
s.corcircle(iv1$as)
# Species positions
s.label(iv1$c1, 2, 1, clab = 0.5, xlim = c(-4, 4))
# Sites positions at the weighted mean of present species
s.label(iv1$ls, 2, 1, clab = 0, cpoi = 1, add.p = TRUE)
# Prediction of the positions by regression on environmental variables
s.match(iv1$ls, iv1$li, 2, 1, clab = 0.5)
# analysis with fa - l1 - co -cor
# canonical weights giving unit variance combinations
s.arrow(iv1$fa)
# sites position by environmental variables combinations
# position of species by averaging
s.label(iv1$l1, 2, 1, clab = 0, cpoi = 1.5)
s.label(iv1$co, 2, 1, add.plot = TRUE)
s.distri(iv1$l1, rpjdl$fau, 2, 1, cell = 0, csta = 0.33)
s.label(iv1$co, 2, 1, clab = 0.75, add.plot = TRUE)
# coherence between weights and correlations
par(mfrow = c(1, 2))
s.corcircle(iv1$cor, 2, 1)
s.arrow(iv1$fa, 2, 1)
par(mfrow = c(1, 1))
}
