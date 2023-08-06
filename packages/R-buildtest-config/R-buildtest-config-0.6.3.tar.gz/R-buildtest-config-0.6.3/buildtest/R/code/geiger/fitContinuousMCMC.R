library(geiger)
## Not run:
data(caniformia)
phy <- caniformia$phy
d <- caniformia$dat
node.priors <- caniformia$node.priors
root.prior <- caniformia$root.prior
## as an example, we will run a very short (too short!) analysis,
##fitting BM and Trend to the caniform data
fitContinuousMCMC(phy, d, model = "BM", Ngens = 1000, sampleFreq =100,
printFreq = 100, node.priors = node.priors, root.prior = root.prior,
outputName ="BM_caniforms")
fitContinuousMCMC(phy, d, model = "Trend", Ngens = 1000, sampleFreq=100,
printFreq = 100, node.priors = node.priors, root.prior = root.prior,
outputName ="Trend_caniforms")
bm.res <- read.table("BM_caniforms_model_params.txt", header= TRUE)
head(bm.res)
trend.res <- read.table("Trend_caniforms_model_params.txt", header= TRUE)
head(trend.res)
### produce trace plots of logLk scores
plot(bm.res$generation, bm.res$logLk, type = "l",
ylim = c(min(bm.res$logLk), max = max(trend.res$logLk)))
lines(trend.res$generation, trend.res$logLk, col = "red")
legend("bottomleft", c("bm", "trend"), lwd = 3, col = c("black", "red"))
## End(Not run)
