library(ade4)
## Not run:
# figure 130 in Percival and Walden (2000)
if (requireNamespace("waveslim") == TRUE) {
data(ecg)
ecg.level <- haar2level(ecg)
ecg.haar <- orthobasis.haar(length(ecg))
ecg.mld <- mld(ecg, ecg.haar, ecg.level, plot = FALSE)
res <- cbind.data.frame(apply(ecg.mld[,1:5],1,sum), ecg.mld[,6:11])
par(mfrow = c(8,1))
par(mar = c(2, 5, 1.5, 0.6))
plot(as.ts(ecg), ylab = "ECG")
apply(res, 2, function(x) plot(as.ts(x), ylim = range(res),
ylab = ""))
par(mfrow = c(1,1))
}
## End(Not run)
