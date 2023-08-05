library(geiger)
## Not run:
data(carnivores)
phy <- carnivores$phy
data <- carnivores$dat
richness <- data[,1]
names(richness) <- rownames(data)
priors <- list(priorSigma = c(-4.5, 4.5), priorMean = c(-5, 2))
## CALIBRATION (far too short for a real analysis)
Cal <- calibrate.mecca(phy, richness, model = "BM", prior.list = priors, Ncalibrations = 1000)
params <- Cal$trait[, c(1,2)] ## extract the calibration BM parameters
stats <- Cal$trait[, -c(1,2)] ## extract the calibration summary stats
## now we run pls, determining combinations of summaries that explain variation in our parameters
## For BM, 2 components is sufficient. For more complex models, more componenets will be required.
require(pls)
myPlsr<-pls::plsr(as.matrix(params) ~ as.matrix(stats), scale=F, ncomp = 2)
plot(RMSEP(myPlsr)) ## Look at Root Mean Square error plots
summary(myPlsr) ## take a look at
plsdat <- myPlsr$loadings
## extract means and variances from the carnivore data ##
cladeMean<-data[,2]
names(cladeMean)<-rownames(data)
cladeVariance<-data[,3]
names(cladeVariance)<-rownames(data)
## STARTING POINT
## And now we can compute starting values for the ABC-MCMC
start <- startingpt.mecca(Cal, phy, cladeMean, cladeVariance,
tolerance = 0.05, plsdat, BoxCox = TRUE)
## MECCA (far too short for a real analysis)
mecca(phy, richness, cladeMean, cladeVariance, model = "BM", prior.list = priors, start = start,
Ngens = 1000, printFreq = 100, sigmaPriorType = "uniform", rootPriorType = "uniform",
SigmaBounds = c(-4.5, 4.5), divPropWidth = 0.1, scale = 2, divSampleFreq = 0, BoxCox = TRUE,
outputName ="MeccaBM.txt")
## PASTE UNCOMMENTED FOLLOWING LINE TO DROP FILES CREATED BY MECCA
# unlink(dir(pattern=paste(r)),recursive=TRUE)
## End(Not run)
