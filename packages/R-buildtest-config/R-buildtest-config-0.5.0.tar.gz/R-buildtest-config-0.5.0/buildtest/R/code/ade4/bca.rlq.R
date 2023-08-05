library(ade4)
data(piosphere)
afcL <- dudi.coa(log(piosphere$veg + 1), scannf = FALSE)
acpR <- dudi.pca(piosphere$env, scannf = FALSE, row.w = afcL$lw)
acpQ <- dudi.hillsmith(piosphere$traits, scannf = FALSE, row.w =
afcL$cw)
rlq1 <- rlq(acpR, afcL, acpQ, scannf = FALSE)
brlq1 <- bca(rlq1, fac = piosphere$habitat, scannf = FALSE)
brlq1
plot(brlq1)
