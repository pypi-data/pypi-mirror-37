library(geiger)
sal <- get(data(caudata))
print(head(sal$tax))
nphy <- subset(sal$phy, sal$tax, "genus", ncores=1)
plot(nphy, type="fan", cex=0.15)

