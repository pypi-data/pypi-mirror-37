library(ade4)
## Not run:
## First example of Dray et al (2015) paper
con <- url("ftp://pbil.univ-lyon1.fr/pub/datasets/dray/MER2014/soilmicrob.rda")
load(con)
close(con)
## Partial CCA
coa <- dudi.coa(soilmicrob$OTU, scannf = FALSE)
wcoa <- wca(coa, soilmicrob$env$pH, scannf = FALSE)
wbcoa <- bca(wcoa,soilmicrob$env$VegType, scannf = FALSE)
## Classical DPCoA
dp <- dpcoa(soilmicrob$OTU, soilmicrob$dphy, RaoDecomp = FALSE, scannf = FALSE)
## Between DPCoA (focus on the effect of vegetation type)
bdp <- bca(dp, fac = soilmicrob$env$VegType , scannf = FALSE)
bdp$ratio ## 0.2148972
randtest(bdp) ## p = 0.001
## Within DPCoA (remove the effect of pH)
wdp <- wca(dp, fac = soilmicrob$env$pH, scannf = FALSE)
wdp$ratio ## 0.5684348
## Between Within-DPCoA (remove the effect of pH and focus on vegetation type)
wbdp <- bwca.dpcoa(dp, fac = soilmicrob$env$VegType, cofac = soilmicrob$env$pH, scannf = FALSE)
wbdp$ratio ## 0.05452813
randtest(wbdp) ## p = 0.001
## End(Not run)

