library(adegenet)
## Not run:
## cattle breed microsatellite data
data(microbov)
## isolate Lagunaire breed
lagun <- seppop(microbov)$Lagunaire
## estimate inbreeding - return sample of F values
Fsamp <- inbreeding(lagun, N=30)
## plot the first 10 results
invisible(sapply(Fsamp[1:10], function(e) plot(density(e), xlab="F",
xlim=c(0,1), main="Density of the sampled F values")))
## compute means for all individuals
Fmean=sapply(Fsamp, mean)
hist(Fmean, col="orange", xlab="mean value of F",
main="Distribution of mean F across individuals")
## estimate inbreeding - return proba density functions
Fdens <- inbreeding(lagun, res.type="function")
## view function for the first individual
Fdens[[1]]
## plot the first 10 functions
invisible(sapply(Fdens[1:10], plot, ylab="Density",
main="Density of probability of F values"))
## estimate inbreeding - return maximum likelihood estimates
Fest <- inbreeding(lagun, res.type = "estimate")
mostInbred <- which.max(Fest)
plot(Fdens[[mostInbred]], ylab = "Density", xlab = "F",
main = paste("Probability density of F values\nfor", names(mostInbred)))
abline(v = Fest[mostInbred], col = "red", lty = 2)
legend("topright", legend = "MLE", col = "red", lty = 2)
## note that estimates and average samples are likely to be different.
plot(Fest, ylab = "F", col = "blue",
main = "comparison of MLE and average sample estimates of F")
points(Fmean, pch = 2, col = "red")
arrows(x0 = 1:length(Fest), y0 = Fest,
y1 = Fmean, x1 = 1:length(Fest), length = 0.125)
legend("topleft", legend = c("estimate", "sample"), col = c("blue", "red"),
pch = c(1, 2), title = "res.type")
## End(Not run)
